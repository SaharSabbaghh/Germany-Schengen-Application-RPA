# VIDEX Form Automation API

Automate the German VIDEX Schengen visa application form. Deploy as an API or run locally.

## 🚀 API Usage (Deployed)

Send a POST request with applicant data in JSON, receive the filled form as PDF:

```bash
curl -X POST https://your-railway-url.railway.app/fill \
  -H "Content-Type: application/json" \
  -d '{
    "surname": "Smith",
    "first_name": "John",
    "date_of_birth": "15.03.1985",
    "place_of_birth": "New York",
    "country_of_birth": "United States",
    "gender": "Male",
    "nationality": "United States",
    "passport_number": "AB1234567",
    "visa_start_date": "01.06.2026",
    "visa_end_date": "15.06.2026"
  }' \
  --output videx_Smith_John.pdf
```

## 📋 Available Fields

All fields use English-friendly names:

| Category | Fields |
|----------|--------|
| Personal | `surname`, `first_name`, `birth_name`, `date_of_birth`, `place_of_birth`, `country_of_birth`, `gender`, `marital_status`, `nationality`, `nationality_at_birth` |
| Occupation | `occupation`, `employer`, `employer_street`, `employer_house_number`, `employer_postal_code`, `employer_city`, `employer_country` |
| Address | `street`, `house_number`, `apartment`, `postal_code`, `city`, `country`, `phone`, `email` |
| Passport | `passport_type`, `passport_number`, `national_id`, `passport_issue_date`, `passport_expiry_date`, `passport_issuing_country`, `passport_issued_by`, `passport_issue_place` |
| Travel | `purpose_of_visit`, `first_entry_country`, `main_destination`, `number_of_entries`, `visa_start_date`, `visa_end_date` |
| Inviter | `inviter_surname`, `inviter_first_name`, `inviter_gender`, `inviter_date_of_birth`, `inviter_nationality`, `inviter_street`, `inviter_city`, `inviter_country`, `inviter_phone`, `inviter_email` |

See `output/complete_template.json` for all available fields with descriptions.

## ⚙️ Default Values

These fields have default values (override by including in your JSON):

- `passport_type`: "Ordinary passport"
- `number_of_entries`: "Single entry"
- `reference_type`: "Inviting person"
- Cost coverage: Third party + inviting person pays
- Support: Accommodation + transport prepaid, all expenses covered

## 🛠 Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Run API locally
python -m src.api
# API available at http://localhost:8000

# Or run CLI
python -m src.main fill --data output/sample_english.json
```

## 🚂 Deploy to Railway

1. Push to GitHub
2. Connect repo to Railway
3. Railway will auto-detect the Dockerfile
4. Set environment variables if needed
5. Deploy!

The API will be available at your Railway URL.

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| POST | `/fill` | Submit JSON, get PDF |

## 📁 Project Structure

```
videx/
├── Dockerfile            # Railway deployment
├── railway.json          # Railway config
├── requirements.txt
├── output/
│   ├── defaults.json         # Default field values
│   ├── fields_schema.json    # Form field schema
│   ├── complete_template.json # All available fields
│   └── sample_english.json   # Example input
├── src/
│   ├── api.py               # FastAPI server
│   ├── main.py              # CLI entry point
│   ├── automation/
│   │   ├── form_filler.py   # Form automation
│   │   ├── field_translator.py # English→German field mapping
│   │   └── data_loader.py
│   └── scraper/
│       ├── form_scraper.py
│       └── schema_generator.py
└── README.md
```
