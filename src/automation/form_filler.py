"""
Form Filler - Automates filling the VIDEX visa application form.
"""

import json
import os
from pathlib import Path
from typing import Any, Optional
from datetime import datetime
from playwright.sync_api import sync_playwright, Page, Locator, TimeoutError as PlaywrightTimeout, Download
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console()

VIDEX_URL = "https://videx.diplo.de/videx/visum-erfassung/videx-kurzfristiger-aufenthalt"


class FormFillerError(Exception):
    """Raised when form filling encounters an error."""
    pass


class VidexFormFiller:
    """
    Automates filling the VIDEX visa application form.
    """

    def __init__(
        self,
        applicant_data: dict[str, Any],
        schema_path: Optional[Path] = None,
        headless: bool = False,
        slow_mo: int = 100,
        screenshot_on_error: bool = True,
        screenshot_dir: Optional[Path] = None,
        output_dir: Optional[Path] = None
    ):
        """
        Initialize the form filler.
        
        Args:
            applicant_data: Flat dictionary of field_id -> value
            schema_path: Path to the schema file for field mappings
            headless: Run browser in headless mode
            slow_mo: Slow down operations by this many milliseconds
            screenshot_on_error: Take screenshot when errors occur
            screenshot_dir: Directory to save screenshots
            output_dir: Directory to save the generated PDF
        """
        self.data = applicant_data
        self.schema_path = schema_path
        self.headless = headless
        self.slow_mo = slow_mo
        self.screenshot_on_error = screenshot_on_error
        self.screenshot_dir = screenshot_dir or Path("./screenshots")
        self.output_dir = output_dir or Path("./output")
        
        self.field_mappings: dict[str, dict] = {}
        self.page: Optional[Page] = None
        self.pdf_path: Optional[Path] = None
        self._load_field_mappings()

    def _load_field_mappings(self) -> None:
        """Load field mappings from schema."""
        if not self.schema_path or not self.schema_path.exists():
            console.print("[yellow]No schema file, will use field IDs as selectors[/yellow]")
            return
        
        with open(self.schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        
        # Support both "sections" (new) and "form_pages" (old) structure
        pages_list = schema.get("sections", schema.get("form_pages", []))
        
        for page in pages_list:
            for field in page.get("fields", []):
                field_id = field.get("id")
                if field_id:
                    self.field_mappings[field_id] = {
                        "selector": field.get("selector", f'[id="{field_id}"]'),
                        "type": field.get("field_type", "text"),
                        "required": field.get("required", False),
                        "options": field.get("options", []),
                        "page": page.get("page_number", 1)
                    }
        
        console.print(f"[cyan]Loaded {len(self.field_mappings)} field mappings from schema[/cyan]")

    def _take_screenshot(self, name: str) -> Optional[Path]:
        """Take a screenshot for debugging."""
        if not self.page:
            return None
        
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = self.screenshot_dir / f"{name}_{timestamp}.png"
        
        try:
            self.page.screenshot(path=str(filepath))
            console.print(f"[cyan]Screenshot saved: {filepath}[/cyan]")
            return filepath
        except Exception as e:
            console.print(f"[yellow]Could not save screenshot: {e}[/yellow]")
            return None

    def _switch_to_english(self) -> bool:
        """Switch the form language to English."""
        console.print("[cyan]Switching language to English...[/cyan]")
        
        try:
            # The VIDEX language selector is the first <select> on the page
            lang_selector = self.page.locator("select").first
            if lang_selector.is_visible(timeout=3000):
                try:
                    lang_selector.select_option(label="English")
                    console.print("[green]Language switched to English[/green]")
                    self.page.wait_for_timeout(2000)
                    self.page.wait_for_load_state("networkidle", timeout=10000)
                    return True
                except Exception as e:
                    console.print(f"[yellow]Could not select English: {e}[/yellow]")
            
            console.print("[yellow]Language selector not found, page may already be in English[/yellow]")
            return False
            
        except Exception as e:
            console.print(f"[yellow]Error switching language: {e}[/yellow]")
            return False

    def _get_selector(self, field_id: str) -> str:
        """Get the CSS selector for a field."""
        if field_id in self.field_mappings:
            return self.field_mappings[field_id]["selector"]
        
        # Fallback: use attribute selector (works with IDs containing periods)
        return f'[id="{field_id}"], [name="{field_id}"]'

    def _get_field_type(self, field_id: str) -> str:
        """Get the field type for a field."""
        if field_id in self.field_mappings:
            return self.field_mappings[field_id]["type"]
        return "text"

    def _wait_for_element(self, selector: str, timeout: int = 10000) -> Optional[Locator]:
        """Wait for an element to be visible."""
        try:
            element = self.page.locator(selector).first
            element.wait_for(state="visible", timeout=timeout)
            return element
        except PlaywrightTimeout:
            return None

    def _fill_text_field(self, field_id: str, value: str) -> bool:
        """Fill a text input field."""
        selector = self._get_selector(field_id)
        element = self._wait_for_element(selector)
        
        if not element:
            console.print(f"[yellow]Field not found: {field_id} ({selector})[/yellow]")
            return False
        
        try:
            # Detect element type at runtime
            tag_name = element.evaluate("el => el.tagName.toLowerCase()")
            input_type = element.get_attribute("type") or "text"
            
            if tag_name == "select":
                # This is a select element, use select_option
                return self._fill_select_field(field_id, str(value))
            elif input_type in ["checkbox", "radio"]:
                # Shouldn't be here, but handle gracefully
                return self._fill_checkbox_field(field_id, bool(value))
            
            element.fill(str(value))
            console.print(f"[green]Filled {field_id}: {value[:30]}{'...' if len(str(value)) > 30 else ''}[/green]")
            return True
        except Exception as e:
            console.print(f"[red]Error filling {field_id}: {e}[/red]")
            return False

    def _fill_select_field(self, field_id: str, value: str) -> bool:
        """Fill a select/dropdown field."""
        selector = self._get_selector(field_id)
        element = self._wait_for_element(selector)
        
        if not element:
            console.print(f"[yellow]Select field not found: {field_id}[/yellow]")
            return False
        
        try:
            # Get options mapping from schema to find value code
            options_mapping = self.field_mappings.get(field_id, {}).get("options", [])
            value_code = None  # Start with None to detect if we found a match
            matched_label = None
            
            # Try to find the value code from our mappings
            value_lower = value.lower().strip()
            for opt in options_mapping:
                opt_label = opt.get("label", "") if isinstance(opt, dict) else str(opt)
                opt_value = opt.get("value", opt_label) if isinstance(opt, dict) else str(opt)
                
                # Exact match on label (highest priority)
                if opt_label.lower().strip() == value_lower:
                    value_code = opt_value
                    matched_label = opt_label
                    break
                # Partial match: input contains label or label contains input
                if value_code is None and (value_lower in opt_label.lower() or opt_label.lower() in value_lower):
                    value_code = opt_value
                    matched_label = opt_label
            
            # If no match found in schema, fallback to raw value
            if value_code is None:
                console.print(f"[yellow]Warning: No exact match in schema for {field_id}='{value}', trying raw value[/yellow]")
                value_code = value
            
            # Try to select using label first (Angular uses dynamic indices for values)
            # Then fall back to value code, then partial text match
            selected = False
            try:
                # Try label first - this is most reliable for Angular apps
                element.select_option(label=matched_label or value)
                selected = True
            except Exception as e1:
                try:
                    # Try by value code from schema
                    element.select_option(value=value_code)
                    selected = True
                except Exception as e2:
                    # Last resort: iterate through options on page and match by text
                    page_options = element.locator("option").all()
                    for opt in page_options:
                        opt_text = (opt.text_content() or "").strip()
                        opt_text_lower = opt_text.lower()
                        # Exact match first
                        if opt_text_lower == value_lower:
                            opt_val = opt.get_attribute("value")
                            if opt_val:
                                element.select_option(value=opt_val)
                                value_code = opt_val
                                matched_label = opt_text
                                selected = True
                                break
                    
                    # If no exact match, try partial match
                    if not selected:
                        for opt in page_options:
                            opt_text = (opt.text_content() or "").strip()
                            opt_text_lower = opt_text.lower()
                            if value_lower in opt_text_lower or opt_text_lower in value_lower:
                                opt_val = opt.get_attribute("value")
                                if opt_val:
                                    element.select_option(value=opt_val)
                                    value_code = opt_val
                                    matched_label = opt_text
                                    selected = True
                                    break
                    
                    if not selected:
                        available = [(o.get_attribute('value'), (o.text_content() or '')[:30]) for o in page_options[:5]]
                        console.print(f"[yellow]Debug {field_id}: No match for '{value}'[/yellow]")
                        console.print(f"[yellow]       Available: {available}[/yellow]")
            
            if selected:
                display_label = matched_label or value
                console.print(f"[green]Selected {field_id}: {display_label} (code: {value_code})[/green]")
                # Wait briefly after select in case it triggers UI changes
                try:
                    self.page.wait_for_timeout(300)
                except Exception:
                    pass
                return True
            else:
                console.print(f"[red]Failed to select {field_id}: No matching option for '{value}'[/red]")
                return False
        except Exception as e:
            if "closed" in str(e).lower():
                console.print(f"[red]Browser closed during select {field_id} - page may have navigated[/red]")
            else:
                console.print(f"[red]Error selecting {field_id}: {e}[/red]")
            return False

    def _fill_radio_field(self, field_id: str, value: str) -> bool:
        """Fill a radio button field."""
        # Radio buttons often have the same name but different values
        selector = f"input[name='{field_id}'][value='{value}'], #{field_id}[value='{value}']"
        element = self._wait_for_element(selector)
        
        if not element:
            # Try alternative selector
            selector = self._get_selector(field_id)
            element = self._wait_for_element(selector)
        
        if not element:
            console.print(f"[yellow]Radio field not found: {field_id}[/yellow]")
            return False
        
        try:
            element.check()
            console.print(f"[green]Checked radio {field_id}: {value}[/green]")
            return True
        except Exception as e:
            console.print(f"[red]Error checking radio {field_id}: {e}[/red]")
            return False

    def _fill_checkbox_field(self, field_id: str, value: bool) -> bool:
        """Fill a checkbox field."""
        selector = self._get_selector(field_id)
        element = self._wait_for_element(selector, timeout=2000)
        
        if not element:
            # Checkbox might not exist (dynamic field) - skip silently if value is False
            if not value:
                return True
            console.print(f"[yellow]Checkbox not found: {field_id}[/yellow]")
            return False
        
        try:
            if value:
                element.check()
                console.print(f"[green]Checked checkbox {field_id}[/green]")
            else:
                # Actively uncheck if value is False
                if element.is_checked():
                    element.uncheck()
                    console.print(f"[cyan]Unchecked checkbox {field_id}[/cyan]")
            # Wait briefly for any conditional fields to appear
            self.page.wait_for_timeout(500)
            return True
        except Exception as e:
            console.print(f"[red]Error with checkbox {field_id}: {e}[/red]")
            return False

    def _fill_date_field(self, field_id: str, value: str) -> bool:
        """Fill a date field."""
        selector = self._get_selector(field_id)
        element = self._wait_for_element(selector)
        
        if not element:
            console.print(f"[yellow]Date field not found: {field_id}[/yellow]")
            return False
        
        try:
            # Date fields often need specific format
            element.fill(value)
            console.print(f"[green]Set date {field_id}: {value}[/green]")
            return True
        except Exception as e:
            console.print(f"[red]Error setting date {field_id}: {e}[/red]")
            return False

    def _fill_field(self, field_id: str, value: Any) -> bool:
        """Fill a single field based on its type."""
        field_type = self._get_field_type(field_id)
        
        # Handle checkboxes specially - False means uncheck, True means check
        # Also treat boolean values as checkboxes even if field_type is unknown
        if field_type == "checkbox" or isinstance(value, bool):
            return self._fill_checkbox_field(field_id, bool(value))
        
        # Skip empty values for non-checkbox fields
        if value is None or value == "":
            return True
        
        if field_type == "select":
            return self._fill_select_field(field_id, str(value))
        elif field_type == "radio":
            return self._fill_radio_field(field_id, str(value))
        elif field_type == "date":
            return self._fill_date_field(field_id, str(value))
        else:
            return self._fill_text_field(field_id, str(value))

    def _handle_popup_dialog(self) -> bool:
        """
        Handle any popup dialogs/warnings that appear on the page.
        Returns True if a dialog was handled.
        Only targets actual modal/popup containers, not main form buttons.
        """
        # Look for specific modal content - not just containers
        # The cdk-overlay-container is always present in Angular but empty when no popup
        try:
            # Check for visible dialog with actual content
            dialog = self.page.locator("[role='dialog']:visible, [role='alertdialog']:visible, .modal.show, .modal:visible").first
            if not dialog.is_visible(timeout=300):
                return False
        except Exception:
            return False
        
        # Found a visible dialog - try to close it
        popup_close_selectors = [
            "[role='dialog'] button:has-text('OK')",
            "[role='dialog'] button:has-text('Schließen')",
            "[role='dialog'] button:has-text('Close')",
            "[role='alertdialog'] button:has-text('OK')",
            ".modal button:has-text('OK')",
            ".modal button:has-text('Close')",
            ".modal button.close",
            "button[aria-label='Close']",
        ]
        
        for selector in popup_close_selectors:
            try:
                button = self.page.locator(selector).first
                if button.is_visible(timeout=500):
                    console.print(f"[yellow]Closing popup/dialog: {selector}[/yellow]")
                    button.click()
                    self.page.wait_for_timeout(500)
                    return True
            except Exception:
                continue
        
        # Handle cookie consent banners
        cookie_selectors = [
            "button:has-text('Accept')",
            "button:has-text('Akzeptieren')",
            "button:has-text('Alle akzeptieren')",
            "button:has-text('Accept all')",
            "[class*='cookie'] button",
            "#cookie-accept",
        ]
        
        for selector in cookie_selectors:
            try:
                button = self.page.locator(selector).first
                if button.is_visible(timeout=500):
                    console.print(f"[yellow]Accepting cookies: {selector}[/yellow]")
                    button.click()
                    self.page.wait_for_timeout(500)
                    return True
            except Exception:
                continue
        
        return False

    def _setup_dialog_handler(self) -> None:
        """Set up handler for JavaScript alert/confirm/prompt dialogs."""
        def handle_dialog(dialog):
            console.print(f"[yellow]Dialog appeared: {dialog.type} - {dialog.message}[/yellow]")
            dialog.accept()
        
        self.page.on("dialog", handle_dialog)

    def _navigate_to_next_page(self) -> bool:
        """Try to navigate to the next form page."""
        # First, try to handle any open popups
        self._handle_popup_dialog()
        
        next_button_selectors = [
            "button:has-text('Continue')",
            "button:has-text('Weiter')",
            "button:has-text('Further')",
            "button:has-text('Next')",
            "button:has-text('Fortfahren')",
            "button[type='submit']:not(:has-text('Submit')):not(:has-text('Absenden'))",
            "input[type='submit'][value*='Continue']",
            "input[type='submit'][value*='Weiter']",
            "input[type='submit'][value*='Next']",
            ".next-button",
            "[class*='next']",
            "[class*='weiter']",
        ]
        
        for selector in next_button_selectors:
            try:
                button = self.page.locator(selector).first
                if button.is_visible() and button.is_enabled():
                    button.click()
                    self.page.wait_for_timeout(1000)
                    
                    # Check for and handle any validation popups after clicking
                    self._handle_popup_dialog()
                    
                    self.page.wait_for_load_state("networkidle", timeout=15000)
                    return True
            except Exception:
                continue
        
        return False

    def _get_current_page_fields(self) -> list[str]:
        """Get field IDs that should be on the current page."""
        # If we have mappings with page numbers, filter by current page
        # Otherwise, just try all fields that haven't been filled
        visible_fields = []
        
        for field_id in self.data.keys():
            selector = self._get_selector(field_id)
            try:
                element = self.page.locator(selector).first
                if element.is_visible(timeout=500):
                    visible_fields.append(field_id)
            except Exception:
                continue
        
        return visible_fields

    def fill_form(self, submit: bool = False, save_pdf: bool = True) -> dict[str, Any]:
        """
        Fill the entire form with the applicant data.
        
        Args:
            submit: Whether to submit the form at the end
            save_pdf: Whether to save the form as PDF after filling
        
        Returns:
            Dictionary with 'fields' (field results) and 'pdf_path' (saved PDF path)
        """
        results = {}
        
        console.print("[bold blue]Starting VIDEX form automation...[/bold blue]")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=self.headless,
                slow_mo=self.slow_mo,
                downloads_path=str(self.output_dir)
            )
            context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                locale="en-US",
                accept_downloads=True
            )
            self.page = context.new_page()
            
            # Set up dialog handler for JavaScript alerts/confirms
            self._setup_dialog_handler()
            
            try:
                # Navigate to the form
                console.print(f"[cyan]Navigating to {VIDEX_URL}[/cyan]")
                self.page.goto(VIDEX_URL, timeout=60000)
                
                # Wait for page content to actually load (Angular app needs time)
                console.print(f"[cyan]Waiting for form to load...[/cyan]")
                try:
                    # Wait for a specific form element to appear
                    self.page.wait_for_selector("input[id='antragsteller.familienname']", timeout=30000)
                    console.print(f"[green]Form loaded successfully[/green]")
                except Exception:
                    console.print(f"[yellow]Form elements not found, waiting longer...[/yellow]")
                    self.page.wait_for_timeout(5000)
                
                # Debug: Check what we have on the page
                input_count = self.page.locator("input").count()
                select_count = self.page.locator("select").count()
                console.print(f"[cyan]Found {input_count} inputs and {select_count} selects on page[/cyan]")
                
                # If no inputs found, try waiting more
                if input_count == 0:
                    console.print(f"[yellow]No form elements detected, waiting for Angular to load...[/yellow]")
                    self.page.wait_for_timeout(5000)
                    self.page.wait_for_load_state("networkidle", timeout=30000)
                    input_count = self.page.locator("input").count()
                    select_count = self.page.locator("select").count()
                    console.print(f"[cyan]After wait: Found {input_count} inputs and {select_count} selects[/cyan]")
                
                # Handle any initial popups (cookies, warnings, etc.)
                self._handle_popup_dialog()
                
                # Switch to English
                self._switch_to_english()
                
                # Wait a bit more after language switch
                self.page.wait_for_timeout(1000)
                
                # Take initial screenshot
                self._take_screenshot("initial_page")
                
                page_num = 1
                max_pages = 20
                filled_fields = set()
                
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TextColumn("{task.completed}/{task.total}"),
                    console=console
                ) as progress:
                    task = progress.add_task("Filling form...", total=len(self.data))
                    
                    while page_num <= max_pages:
                        progress.update(task, description=f"Page {page_num}: Filling fields...")
                        
                        # Multiple passes to handle conditional fields
                        max_passes = 3
                        for pass_num in range(max_passes):
                            # Get visible fields on current page
                            current_fields = self._get_current_page_fields()
                            
                            if not current_fields and pass_num == 0:
                                console.print(f"[yellow]No visible fields on page {page_num}[/yellow]")
                            
                            # Count new fields to fill in this pass
                            new_fields = [f for f in current_fields if f not in filled_fields]
                            if not new_fields:
                                break  # No new fields to fill
                            
                            # Fill each visible field
                            for field_id in new_fields:
                                value = self.data.get(field_id)
                                if value is not None and value != "":
                                    try:
                                        success = self._fill_field(field_id, value)
                                        results[field_id] = success
                                    except Exception as fill_err:
                                        console.print(f"[red]Exception filling {field_id}: {fill_err}[/red]")
                                        results[field_id] = False
                                    filled_fields.add(field_id)
                                    progress.advance(task)
                            
                            # Wait briefly for any conditional fields to appear
                            self.page.wait_for_timeout(300)
                        
                        # Take screenshot of completed page
                        self._take_screenshot(f"page_{page_num}_filled")
                        
                        # Check if we've filled all fields
                        if len(filled_fields) >= len([k for k, v in self.data.items() if v]):
                            console.print("[green]All fields filled![/green]")
                            break
                        
                        # Try to go to next page
                        if not self._navigate_to_next_page():
                            console.print("[cyan]No more pages to navigate.[/cyan]")
                            break
                        
                        page_num += 1
                        self.page.wait_for_timeout(1000)
                
                # Handle submission
                if submit:
                    self._submit_form()
                else:
                    console.print("[yellow]Form filled but NOT submitted (--submit flag not set)[/yellow]")
                    self._take_screenshot("final_not_submitted")
                
                # Check if all fields were filled successfully before proceeding to PDF
                success_count = sum(1 for v in results.values() if v)
                total_fields = len(self.data)
                
                if success_count < total_fields:
                    console.print(f"[yellow]Warning: Only {success_count}/{total_fields} fields filled[/yellow]")
                    failed_fields = [k for k, v in results.items() if not v]
                    if failed_fields:
                        console.print(f"[yellow]Failed fields: {failed_fields[:10]}{'...' if len(failed_fields) > 10 else ''}[/yellow]")
                
                # Save PDF only after all fields are filled
                saved_path = None
                if save_pdf:
                    console.print(f"\n[bold cyan]All {success_count} fields filled. Saving form as PDF...[/bold cyan]")
                    saved_path = self._save_pdf()
                
                # Summary
                fail_count = len(results) - success_count
                
                console.print(f"\n[bold]Form Filling Summary:[/bold]")
                console.print(f"  [green]Successful: {success_count}[/green]")
                console.print(f"  [red]Failed: {fail_count}[/red]")
                if saved_path:
                    console.print(f"  [cyan]PDF saved: {saved_path}[/cyan]")
                
            except Exception as e:
                console.print(f"[bold red]Error during form filling: {e}[/bold red]")
                if self.screenshot_on_error:
                    self._take_screenshot("error")
                raise FormFillerError(str(e))
            finally:
                # Keep browser open briefly for debugging if not headless
                if not self.headless:
                    console.print("[cyan]Browser will close in 5 seconds...[/cyan]")
                    self.page.wait_for_timeout(5000)
                browser.close()
        
        return {
            "fields": results,
            "pdf_path": self.pdf_path,
            "success_count": sum(1 for v in results.values() if v),
            "fail_count": len(results) - sum(1 for v in results.values() if v)
        }

    def _submit_form(self) -> None:
        """Submit the form."""
        submit_selectors = [
            "button[type='submit']:has-text('Submit')",
            "button[type='submit']:has-text('Absenden')",
            "button:has-text('Submit')",
            "button:has-text('Absenden')",
            "input[type='submit']",
        ]
        
        for selector in submit_selectors:
            try:
                button = self.page.locator(selector).first
                if button.is_visible() and button.is_enabled():
                    console.print("[bold yellow]Submitting form...[/bold yellow]")
                    button.click()
                    self.page.wait_for_load_state("networkidle", timeout=30000)
                    self._take_screenshot("submitted")
                    console.print("[bold green]Form submitted![/bold green]")
                    return
            except Exception:
                continue
        
        console.print("[red]Could not find submit button[/red]")

    def _navigate_to_print_page(self) -> bool:
        """
        Navigate through the form to reach the final print/summary page.
        Keeps pressing "Further" / "Weiter" until we find the print button or can't continue.
        """
        console.print("[cyan]Navigating to print page by clicking 'Continue'...[/cyan]")
        
        max_attempts = 15
        for attempt in range(max_attempts):
            # Take screenshot at each step for debugging
            self._take_screenshot(f"navigate_step_{attempt}")
            
            # Check if we're on the print page
            print_button_selectors = [
                "button:has-text('Drucken')",
                "button:has-text('Print')",
                "button:has-text('Print application')",
                "button:has-text('Antrag drucken')",
                "button:has-text('PDF')",
                "a:has-text('Drucken')",
                "a:has-text('Print')",
                "a:has-text('PDF')",
                "a:has-text('Print application')",
                "[class*='print']",
            ]
            
            for selector in print_button_selectors:
                try:
                    button = self.page.locator(selector).first
                    if button.is_visible(timeout=1000):
                        console.print(f"[green]Found print page with button: {selector}[/green]")
                        return True
                except Exception:
                    continue
            
            # Check for summary/review page indicators
            summary_indicators = [
                "text=Summary",
                "text=Zusammenfassung",
                "text=Review",
                "text=Überprüfen",
                "text=Application Preview",
                "text=Antragsvorschau",
            ]
            
            for indicator in summary_indicators:
                try:
                    if self.page.locator(indicator).first.is_visible(timeout=500):
                        console.print(f"[green]Found summary/review page: {indicator}[/green]")
                        return True
                except Exception:
                    continue
            
            # Handle any popups/dialogs before clicking
            self._handle_popup_dialog()
            
            # Try to click "Continue" / "Weiter" button
            further_clicked = False
            further_selectors = [
                "button:has-text('Continue')",
                "button:has-text('Weiter')",
                "button:has-text('Further')",
                "button:has-text('Next')",
                "a:has-text('Continue')",
                "a:has-text('Weiter')",
                "input[value*='Continue']",
                "input[value*='Weiter']",
            ]
            
            for selector in further_selectors:
                try:
                    button = self.page.locator(selector).first
                    if button.is_visible(timeout=1000) and button.is_enabled():
                        console.print(f"[cyan]Clicking '{selector}' (attempt {attempt + 1})...[/cyan]")
                        button.click()
                        self.page.wait_for_timeout(2000)
                        
                        # Handle any validation popups
                        self._handle_popup_dialog()
                        
                        try:
                            self.page.wait_for_load_state("networkidle", timeout=10000)
                        except Exception:
                            pass
                        
                        further_clicked = True
                        break
                except Exception as e:
                    console.print(f"[dim]Selector {selector} not found: {e}[/dim]")
                    continue
            
            if not further_clicked:
                console.print("[yellow]Could not find 'Further' button, checking for print options...[/yellow]")
                break
        
        return False

    def _save_pdf(self) -> Optional[Path]:
        """
        Save the generated PDF from VIDEX.
        Clicks Continue -> waits for popup -> clicks Download PDF button.
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Get applicant name for filename if available
        name = self.data.get("antragsteller.familienname", "applicant")
        if not name:
            name = "applicant"
        name = "".join(c if c.isalnum() else "_" for c in str(name))
        
        pdf_filename = f"videx_application_{name}_{timestamp}.pdf"
        pdf_path = self.output_dir / pdf_filename
        
        # Step 1: Click the Continue button to trigger the popup
        console.print("[cyan]Clicking Continue button to open PDF popup...[/cyan]")
        
        continue_selectors = [
            "button:has-text('Continue')",
            "button:has-text('Weiter')",
            "button:has-text('Further')",
        ]
        
        continue_clicked = False
        for selector in continue_selectors:
            try:
                button = self.page.locator(selector).first
                if button.is_visible(timeout=2000) and button.is_enabled():
                    console.print(f"[green]Found Continue button: {selector}[/green]")
                    button.click()
                    continue_clicked = True
                    break
            except Exception:
                continue
        
        if not continue_clicked:
            console.print("[yellow]Could not find Continue button[/yellow]")
        
        # Wait for popup to appear
        self.page.wait_for_timeout(2000)
        self._take_screenshot("after_continue_click")
        
        # Step 2: Find and click "Download PDF" button in the popup
        console.print("[cyan]Looking for Download PDF button in popup...[/cyan]")
        self.page.wait_for_timeout(1000)
        
        # The Download PDF button is in the modal - look for it specifically
        pdf_button = self.page.locator("a:has-text('Download PDF'), button:has-text('Download PDF')").first
        
        if not pdf_button.is_visible(timeout=5000):
            console.print("[yellow]Download PDF button not found in popup[/yellow]")
            return None
        
        console.print("[green]Found 'Download PDF' button in popup[/green]")
        
        # Method 1: Try to capture download event
        try:
            with self.page.expect_download(timeout=10000) as download_info:
                pdf_button.click()
            
            download = download_info.value
            console.print(f"[cyan]Download started: {download.suggested_filename}[/cyan]")
            download.save_as(str(pdf_path))
            console.print(f"[bold green]PDF saved: {pdf_path}[/bold green]")
            self.pdf_path = pdf_path
            return pdf_path
            
        except Exception as e:
            console.print(f"[yellow]Download event not captured: {e}[/yellow]")
        
        # Method 2: The link might open PDF in a new tab/window
        console.print("[cyan]Checking for new window with PDF...[/cyan]")
        
        # Click and wait for new page
        with self.page.context.expect_page(timeout=10000) as new_page_info:
            pdf_button.click()
        
        try:
            new_page = new_page_info.value
            new_page.wait_for_load_state("load", timeout=15000)
            console.print(f"[cyan]New page opened: {new_page.url}[/cyan]")
            
            # Check if the new page is a PDF blob or URL
            if 'blob:' in new_page.url or '.pdf' in new_page.url.lower():
                # Try to get the PDF content from the new page
                console.print("[cyan]Saving PDF from new window...[/cyan]")
                
                # Use JavaScript to get the PDF blob data
                try:
                    # For blob URLs, fetch the blob and save it
                    pdf_content = new_page.evaluate("""
                        async () => {
                            const response = await fetch(window.location.href);
                            const blob = await response.blob();
                            const buffer = await blob.arrayBuffer();
                            return Array.from(new Uint8Array(buffer));
                        }
                    """)
                    
                    # Write the PDF content to file
                    with open(str(pdf_path), 'wb') as f:
                        f.write(bytes(pdf_content))
                    
                    console.print(f"[bold green]PDF saved: {pdf_path}[/bold green]")
                    self.pdf_path = pdf_path
                    new_page.close()
                    return pdf_path
                    
                except Exception as fetch_err:
                    console.print(f"[yellow]Could not fetch PDF blob: {fetch_err}[/yellow]")
            
            new_page.close()
            
        except Exception as page_err:
            console.print(f"[yellow]No new page opened: {page_err}[/yellow]")
        
        # Method 3: Check Downloads folder
        console.print("[cyan]Checking Downloads folder...[/cyan]")
        import os
        import time
        import shutil
        
        downloads_dir = os.path.expanduser("~/Downloads")
        self.page.wait_for_timeout(3000)
        
        for attempt in range(5):
            try:
                recent_pdfs = sorted(
                    [f for f in os.listdir(downloads_dir) if f.lower().endswith('.pdf')],
                    key=lambda x: os.path.getmtime(os.path.join(downloads_dir, x)),
                    reverse=True
                )
                
                if recent_pdfs:
                    latest_pdf = os.path.join(downloads_dir, recent_pdfs[0])
                    if time.time() - os.path.getmtime(latest_pdf) < 30:
                        shutil.copy(latest_pdf, str(pdf_path))
                        console.print(f"[bold green]PDF copied from Downloads: {pdf_path}[/bold green]")
                        self.pdf_path = pdf_path
                        return pdf_path
            except Exception:
                pass
            
            self.page.wait_for_timeout(1000)
        
        # If we got here, the download wasn't captured
        console.print("[red]Could not download the PDF from VIDEX[/red]")
        console.print("[yellow]Please check the Downloads folder manually[/yellow]")
        
        return None

    def _print_form(self) -> None:
        """Trigger the browser print dialog (for manual printing)."""
        try:
            console.print("[cyan]Opening print dialog...[/cyan]")
            self.page.keyboard.press("Control+P")
            self.page.wait_for_timeout(2000)
        except Exception as e:
            console.print(f"[yellow]Could not open print dialog: {e}[/yellow]")


def fill_videx_form(
    data_path: Path,
    schema_path: Optional[Path] = None,
    defaults_path: Optional[Path] = None,
    headless: bool = False,
    submit: bool = False,
    save_pdf: bool = True,
    output_dir: Optional[Path] = None
) -> dict[str, Any]:
    """
    Convenience function to fill the VIDEX form.
    
    Args:
        data_path: Path to applicant data JSON (can use English field names)
        schema_path: Path to schema JSON (for field mappings)
        defaults_path: Path to defaults JSON (applied before user data)
        headless: Run in headless mode
        submit: Actually submit the form
        save_pdf: Save the form as PDF
        output_dir: Directory to save the PDF
    
    Returns:
        Dictionary with field results and PDF path
    """
    from .data_loader import ApplicantDataLoader
    
    loader = ApplicantDataLoader(
        data_path,
        schema_path,
        defaults_path=defaults_path,
        use_english=True
    )
    loader.load()
    
    # Validate data
    is_valid, missing = loader.validate()
    if not is_valid:
        console.print(f"[yellow]Warning: Missing required fields: {missing}[/yellow]")
    
    filler = VidexFormFiller(
        applicant_data=loader.get_all_values(),
        schema_path=schema_path,
        headless=headless,
        output_dir=output_dir or data_path.parent
    )
    
    return filler.fill_form(submit=submit, save_pdf=save_pdf)


if __name__ == "__main__":
    # Test
    base_path = Path(__file__).parent.parent.parent
    data_path = base_path / "output" / "applicant_template.json"
    schema_path = base_path / "output" / "fields_schema.json"
    
    if data_path.exists():
        results = fill_videx_form(data_path, schema_path, headless=False, submit=False)
    else:
        console.print("[red]No applicant data file found. Create one first.[/red]")

