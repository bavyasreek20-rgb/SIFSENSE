# SIFSense
**AI-Powered SIF Precursor Detection Engine for OIL Safety Reports**  
Team: **INFRON** | Seva First Innovation Challenge 2026 | Theme: Surakshit Bharat

## Overview
SIFSense is a prototype that analyzes unsafe-act, unsafe-condition, and near-miss report text to flag possible Serious Injury and Fatality (SIF) precursors. It uses a transparent, configurable keyword/phrase lexicon, severity scoring, evidence highlighting, and illustrative Life-Saving Rule mappings.

> **Prototype notice:** This repository is a demonstration starter project. It has not been validated against OIL's operational dataset, and its scores are heuristic—not calibrated probabilities or professional safety determinations. A qualified HSE professional must review flagged reports. Rule mappings are illustrative and should be checked against the current official IOGP guidance before operational use.

## Features
- FastAPI REST API with interactive docs
- Explainable phrase detection and severity score
- SIF-potential / non-SIF-potential triage label
- Illustrative Life-Saving Rule mapping
- SQLite persistence for analyzed reports
- React dashboard for entering and viewing reports
- Synthetic sample data and automated backend tests

## Tech stack
Python, FastAPI, Pydantic, SQLite, React, Vite, JavaScript, Recharts.

## Repository layout
```text
SIFSense/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── schemas.py
│   │   └── analyzer.py
│   ├── tests/test_analyzer.py
│   └── requirements.txt
├── frontend/
│   ├── package.json
│   ├── index.html
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       └── styles.css
├── data/sample_reports.json
├── docs/ARCHITECTURE.md
├── .gitignore
└── LICENSE
```

## Run the backend (Python 3.10+ recommended)
Open a terminal in the `backend` folder:
```bash
python -m venv .venv
```
Windows:
```bash
.venv\Scripts\activate
```
macOS/Linux:
```bash
source .venv/bin/activate
```
Install and run:
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Backend API: http://127.0.0.1:8000  
Interactive API docs: http://127.0.0.1:8000/docs

## Run the frontend
Install Node.js (LTS), then open a second terminal in `frontend`:
```bash
npm install
npm run dev
```
Open the local URL printed by Vite (normally http://localhost:5173).

## API endpoints
- `GET /` – service status
- `GET /health` – health check
- `POST /analyze` – analyze and save a report
- `GET /reports` – list saved reports
- `GET /reports/{report_id}` – retrieve a saved report
- `GET /summary` – dashboard summary

Example request:
```json
{
  "report_text": "Worker entered a confined space without a gas test.",
  "site": "Demo Site",
  "activity": "Confined space work"
}
```

## Data
`data/sample_reports.json` contains synthetic demonstration reports. Do not upload confidential company, worker, medical, or incident data to a public repository.

## Testing
From `backend/`:
```bash
pip install -r requirements.txt
pytest
```

## Limitations and next steps
- The current analyzer is a transparent rule/lexicon baseline, not a trained machine-learning model.
- Severity scores are heuristic and should not be interpreted as probability.
- Life-Saving Rule mapping is illustrative; verify against official current guidance.
- Before deployment: conduct HSE review, evaluate false negatives/positives, test with authorized historical data, add authentication/authorization, audit logging, privacy controls, and production database configuration.
