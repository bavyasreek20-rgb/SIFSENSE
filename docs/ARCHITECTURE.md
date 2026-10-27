# SIFSense — Architecture

## High-level flow
1. An HSE user submits a report through the React dashboard or the API.
2. FastAPI validates the input using Pydantic.
3. The baseline NLP analyzer normalizes text and searches for configured precursor phrases.
4. Matched phrases are returned as evidence with categories and heuristic weights.
5. The engine calculates a capped severity index and applies a configurable triage threshold.
6. Illustrative Life-Saving Rule hints are attached to matched precursors.
7. The analysis is stored in SQLite and returned to the UI.
8. The dashboard displays the classification, score, evidence, and summary counts.

## Components
- **React/Vite frontend:** report submission, summary cards, result evidence.
- **FastAPI:** REST endpoints and request validation.
- **Analyzer:** transparent phrase lexicon and deterministic scoring.
- **SQLite:** local prototype persistence.
- **Synthetic data:** sample reports for demonstration and testing.

## API
- `GET /health`
- `POST /analyze`
- `GET /reports?limit=50`
- `GET /reports/{report_id}`
- `GET /summary`

## Safety and limitations
The current analyzer is a rule-based baseline. It is not a trained NLP model and does not understand context, negation, sarcasm, or synonyms robustly. The score is not a probability. Rule labels are illustrative mappings and must be validated against the official current IOGP Life-Saving Rules. This prototype must not replace professional HSE judgement.

## Production hardening
Before operational use, add authentication, role-based access, audit logs, retention policies, secure deployment, robust evaluation on approved historical data, model monitoring, and review by qualified HSE experts.
