"""
VIDEX Form Automation API
Accepts JSON POST requests and returns generated PDF
"""

import os
import tempfile
import asyncio
from pathlib import Path
from typing import Any
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI, HTTPException
from fastapi.responses import Response

# Add src to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent))

from automation.field_translator import FieldTranslator
from automation.form_filler import VidexFormFiller

app = FastAPI(
    title="VIDEX Form Automation API",
    description="Automate German Schengen visa application form filling",
    version="1.0.0"
)

# Paths
BASE_DIR = Path(__file__).parent.parent
DEFAULTS_PATH = BASE_DIR / "output" / "defaults.json"
SCHEMA_PATH = BASE_DIR / "output" / "fields_schema.json"

# Thread pool for running playwright (sync) in async context
executor = ThreadPoolExecutor(max_workers=2)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "VIDEX Form Automation API",
        "usage": "POST /fill with JSON body containing applicant data",
        "example_fields": [
            "surname", "first_name", "date_of_birth", "nationality",
            "passport_number", "visa_start_date", "visa_end_date"
        ]
    }


@app.get("/health")
async def health():
    """Health check for Railway"""
    return {"status": "healthy"}


@app.post("/fill")
async def fill_form(data: dict[str, Any]):
    """
    Fill VIDEX form with applicant data and return PDF.
    
    Send a JSON body with applicant fields (English names supported).
    Returns the generated PDF file.
    
    Example:
    ```json
    {
        "surname": "Smith",
        "first_name": "John",
        "date_of_birth": "15.03.1985",
        "nationality": "United States",
        ...
    }
    ```
    """
    try:
        # Initialize translator with defaults
        translator = FieldTranslator(DEFAULTS_PATH if DEFAULTS_PATH.exists() else None)
        
        # Translate English field names to German IDs
        translated_data = translator.translate_data(data)
        
        # Get name for filename
        first_name = data.get("first_name", data.get("vorname", "applicant"))
        surname = data.get("surname", data.get("familienname", ""))
        full_name = f"{first_name}_{surname}".strip("_").replace(" ", "_")
        
        # Run form filling in thread pool
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            executor,
            run_form_filler,
            translated_data,
            full_name
        )
        
        if result.get("pdf_content"):
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"videx_{full_name}_{timestamp}.pdf"
            
            return Response(
                content=result["pdf_content"],
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f'attachment; filename="{filename}"'
                }
            )
        else:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": result.get("error", "PDF generation failed"),
                    "fields_filled": result.get("successful", 0),
                    "fields_failed": result.get("failed", 0)
                }
            )
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": str(e)}
        )


def run_form_filler(data: dict[str, Any], name: str) -> dict[str, Any]:
    """Run the form filler synchronously (called from thread pool)"""
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            screenshot_dir = temp_path / "screenshots"
            screenshot_dir.mkdir(exist_ok=True)
            
            # Initialize form filler
            filler = VidexFormFiller(
                applicant_data=data,
                schema_path=SCHEMA_PATH if SCHEMA_PATH.exists() else None,
                headless=True,  # Must be headless on server
                slow_mo=50,
                screenshot_on_error=True,
                screenshot_dir=screenshot_dir,
                output_dir=temp_path
            )
            
            # Fill the form
            result = filler.fill_form(submit=False, save_pdf=True)
            
            # Read PDF content if available
            pdf_path = result.get("pdf_path")
            if pdf_path and Path(pdf_path).exists():
                result["pdf_content"] = Path(pdf_path).read_bytes()
            
            return result
            
    except Exception as e:
        return {"error": str(e), "successful": 0, "failed": 0}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
