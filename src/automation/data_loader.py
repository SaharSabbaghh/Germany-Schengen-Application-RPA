"""
Data Loader - Loads and validates applicant data from JSON files.
"""

import json
from pathlib import Path
from typing import Any, Optional
from rich.console import Console
from rich.table import Table

console = Console()


class DataValidationError(Exception):
    """Raised when applicant data validation fails."""
    pass


def load_applicant_data(data_path: Path) -> dict[str, Any]:
    """
    Load applicant data from a JSON file.
    
    Args:
        data_path: Path to the applicant data JSON file
    
    Returns:
        Dictionary containing the applicant data
    
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file is not valid JSON
    """
    if not data_path.exists():
        raise FileNotFoundError(f"Applicant data file not found: {data_path}")
    
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    console.print(f"[green]Loaded applicant data from {data_path}[/green]")
    return data


def flatten_applicant_data(data: dict[str, Any]) -> dict[str, Any]:
    """
    Flatten nested applicant data to a simple field_id -> value mapping.
    
    Handles both flat format and nested page format.
    
    Args:
        data: The loaded applicant data (possibly nested)
    
    Returns:
        Flat dictionary mapping field IDs to values
    """
    flat_data = {}
    
    # Check if it's the nested page format
    if "pages" in data:
        for page_key, page_data in data["pages"].items():
            if isinstance(page_data, dict) and "fields" in page_data:
                for field_id, field_info in page_data["fields"].items():
                    if isinstance(field_info, dict) and "value" in field_info:
                        flat_data[field_id] = field_info["value"]
                    else:
                        flat_data[field_id] = field_info
    else:
        # Already flat format - filter out comment keys
        for key, value in data.items():
            if not key.startswith("_"):
                flat_data[key] = value
    
    return flat_data


def validate_required_fields(
    data: dict[str, Any],
    schema_path: Optional[Path] = None,
    required_fields: Optional[list[str]] = None
) -> tuple[bool, list[str]]:
    """
    Validate that all required fields have values.
    
    Args:
        data: Flat applicant data dictionary
        schema_path: Path to the schema file (to get required fields)
        required_fields: List of required field IDs (alternative to schema)
    
    Returns:
        Tuple of (is_valid, list of missing required fields)
    """
    if required_fields is None and schema_path:
        required_fields = _get_required_fields_from_schema(schema_path)
    
    if required_fields is None:
        console.print("[yellow]Warning: No required fields specified, skipping validation[/yellow]")
        return True, []
    
    missing = []
    for field_id in required_fields:
        value = data.get(field_id)
        if value is None or value == "" or (isinstance(value, bool) and value is False):
            # For checkboxes, False might be valid, but for text fields empty is not
            if not isinstance(value, bool):
                missing.append(field_id)
    
    return len(missing) == 0, missing


def _get_required_fields_from_schema(schema_path: Path) -> list[str]:
    """Extract required field IDs from the schema file."""
    if not schema_path.exists():
        return []
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = json.load(f)
    
    required = []
    for page in schema.get("form_pages", []):
        for field in page.get("fields", []):
            if field.get("required", False):
                required.append(field.get("id"))
    
    return required


def display_data_summary(data: dict[str, Any], schema_path: Optional[Path] = None) -> None:
    """
    Display a summary of the applicant data.
    
    Args:
        data: Flat applicant data dictionary
        schema_path: Optional path to schema for field labels
    """
    # Load labels from schema if available
    labels = {}
    if schema_path and schema_path.exists():
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        for page in schema.get("form_pages", []):
            for field in page.get("fields", []):
                labels[field.get("id")] = field.get("label", field.get("id"))
    
    table = Table(title="Applicant Data Summary")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")
    table.add_column("Status", style="yellow")
    
    filled_count = 0
    empty_count = 0
    
    for field_id, value in data.items():
        label = labels.get(field_id, field_id)
        
        # Truncate long values
        display_value = str(value)
        if len(display_value) > 50:
            display_value = display_value[:47] + "..."
        
        if value is None or value == "":
            status = "Empty"
            empty_count += 1
        else:
            status = "Filled"
            filled_count += 1
        
        table.add_row(label[:40], display_value, status)
    
    console.print(table)
    console.print(f"\n[bold]Summary:[/bold] {filled_count} filled, {empty_count} empty")


def merge_data_with_defaults(
    user_data: dict[str, Any],
    template_path: Path
) -> dict[str, Any]:
    """
    Merge user data with template defaults.
    
    Args:
        user_data: User-provided data
        template_path: Path to the template file
    
    Returns:
        Merged data dictionary
    """
    if not template_path.exists():
        return user_data
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template = json.load(f)
    
    template_flat = flatten_applicant_data(template)
    
    # User data takes precedence
    merged = {**template_flat, **user_data}
    
    return merged


class ApplicantDataLoader:
    """
    High-level class for loading and managing applicant data.
    Supports English field names and default values.
    """
    
    def __init__(
        self,
        data_path: Path,
        schema_path: Optional[Path] = None,
        defaults_path: Optional[Path] = None,
        use_english: bool = True
    ):
        self.data_path = data_path
        self.schema_path = schema_path
        self.defaults_path = defaults_path
        self.use_english = use_english
        self.raw_data: dict = {}
        self.flat_data: dict = {}
        self._loaded = False
        self._translator = None
        
        # Initialize translator if using English
        if use_english:
            from .field_translator import FieldTranslator
            self._translator = FieldTranslator(defaults_path)
    
    def load(self) -> "ApplicantDataLoader":
        """Load the applicant data, translating English names if needed."""
        self.raw_data = load_applicant_data(self.data_path)
        
        # Flatten first
        flat_raw = flatten_applicant_data(self.raw_data)
        
        # Auto-generate other_means_specify from employer data if not provided
        if "other_means_specify" not in flat_raw:
            employer_info = self._build_employer_info(flat_raw)
            if employer_info:
                flat_raw["other_means_specify"] = employer_info
        
        # Translate if using English mode
        if self._translator:
            self.flat_data = self._translator.translate_data(flat_raw)
        else:
            self.flat_data = flat_raw
        
        # Auto-populate sponsor fields from employer fields (Section 22) if other_sponsor_pays is used
        # (do this after translation so defaults are applied)
        self._copy_employer_to_sponsor_translated(self.flat_data)
        
        self._loaded = True
        return self
    
    def _build_employer_info(self, data: dict[str, Any]) -> str:
        """Build employer info string for 'other means specify' field."""
        parts = []
        
        # Employer name
        employer = data.get("employer", "")
        if employer:
            parts.append(employer)
        
        # Address
        address_parts = []
        street = data.get("employer_street", "")
        house_num = data.get("employer_house_number", "")
        if street:
            addr = street
            if house_num:
                addr += f" {house_num}"
            address_parts.append(addr)
        
        postal = data.get("employer_postal_code", "")
        city = data.get("employer_city", "")
        if postal or city:
            address_parts.append(f"{postal} {city}".strip())
        
        country = data.get("employer_country", "")
        if country:
            address_parts.append(country)
        
        if address_parts:
            parts.append(", ".join(address_parts))
        
        # Phone
        phone = data.get("phone", "")
        if phone:
            parts.append(f"Tel: {phone}")
        
        return ", ".join(parts) if parts else ""
    
    def _copy_employer_to_sponsor(self, data: dict[str, Any]) -> None:
        """Copy employer fields (Section 22) to sponsor fields if other_sponsor_pays is used."""
        # Only copy if other_sponsor_pays is set
        if not data.get("other_sponsor_pays", False):
            return
        
        # For company/employer sponsor, use employer data from Section 22
        # The sponsor is a company, so we use employer name as contact name
        employer_to_sponsor = {
            "employer": "sponsor_surname",  # Company name goes in surname field
            "employer_street": "sponsor_street",
            "employer_house_number": "sponsor_house_number",
            "employer_postal_code": "sponsor_postal_code",
            "employer_city": "sponsor_city",
            "employer_country": "sponsor_country",
            "phone": "sponsor_phone",  # Applicant's phone as contact
            "email": "sponsor_email",  # Applicant's email as contact
        }
        
        for employer_field, sponsor_field in employer_to_sponsor.items():
            # Only copy if sponsor field is not already provided
            if sponsor_field not in data or not data[sponsor_field]:
                employer_value = data.get(employer_field, "")
                if employer_value:
                    data[sponsor_field] = employer_value
        
        # Set default sponsor type to "Company" for employer
        if "sponsor_type" not in data or not data["sponsor_type"]:
            data["sponsor_type"] = "Company"
    
    def _copy_employer_to_sponsor_translated(self, data: dict[str, Any]) -> None:
        """Copy employer fields (Section 22) to sponsor fields (using translated German field names)."""
        # Only copy if other_sponsor_pays (organisation) is set
        if not data.get("reisedaten.reisekostenUebernahme.organisation", False):
            return
        
        # Mapping from employer German IDs to sponsor German IDs
        # Employer = Section 22 = antragsteller.personendaten.berufdaten
        employer_to_sponsor = {
            "antragsteller.personendaten.berufdaten.firmenname": "verpflichtungserklaerungsgeber.ansprechpartner.familienname",
            "antragsteller.personendaten.berufdaten.strasse": "verpflichtungserklaerungsgeber.ansprechpartner.anschrift.strasse",
            "antragsteller.personendaten.berufdaten.hausnummer": "verpflichtungserklaerungsgeber.ansprechpartner.anschrift.hausnummer",
            "antragsteller.personendaten.berufdaten.plz": "verpflichtungserklaerungsgeber.ansprechpartner.anschrift.plz",
            "antragsteller.personendaten.berufdaten.ort": "verpflichtungserklaerungsgeber.ansprechpartner.anschrift.ort",
            "antragsteller.personendaten.berufdaten.land": "verpflichtungserklaerungsgeber.ansprechpartner.anschrift.land",
            "antragsteller.personendaten.staendigeAnschrift.kontaktdaten.telefon": "verpflichtungserklaerungsgeber.ansprechpartner.kontaktdaten.telefon",
            "antragsteller.personendaten.staendigeAnschrift.kontaktdaten.email": "verpflichtungserklaerungsgeber.ansprechpartner.kontaktdaten.email",
        }
        
        for employer_field, sponsor_field in employer_to_sponsor.items():
            # Only copy if sponsor field is not already provided
            if sponsor_field not in data or not data[sponsor_field]:
                employer_value = data.get(employer_field, "")
                if employer_value:
                    data[sponsor_field] = employer_value
        
        # Set default sponsor type to "Company" for employer
        if "verpflichtungserklaerungsgeber.art" not in data or not data["verpflichtungserklaerungsgeber.art"]:
            data["verpflichtungserklaerungsgeber.art"] = "Company"
    
    def validate(self) -> tuple[bool, list[str]]:
        """Validate the loaded data."""
        if not self._loaded:
            self.load()
        return validate_required_fields(self.flat_data, self.schema_path)
    
    def get_value(self, field_id: str, default: Any = None) -> Any:
        """Get a field value."""
        if not self._loaded:
            self.load()
        return self.flat_data.get(field_id, default)
    
    def get_all_values(self) -> dict[str, Any]:
        """Get all field values as a flat dictionary."""
        if not self._loaded:
            self.load()
        return self.flat_data.copy()
    
    def display_summary(self) -> None:
        """Display a summary of the data."""
        if not self._loaded:
            self.load()
        display_data_summary(self.flat_data, self.schema_path)


if __name__ == "__main__":
    # Test
    base_path = Path(__file__).parent.parent.parent
    data_path = base_path / "output" / "applicant_template.json"
    schema_path = base_path / "output" / "fields_schema.json"
    
    if data_path.exists():
        loader = ApplicantDataLoader(data_path, schema_path)
        loader.load()
        loader.display_summary()
        
        is_valid, missing = loader.validate()
        if not is_valid:
            console.print(f"[red]Missing required fields: {missing}[/red]")
    else:
        console.print("[yellow]No applicant data file found.[/yellow]")

