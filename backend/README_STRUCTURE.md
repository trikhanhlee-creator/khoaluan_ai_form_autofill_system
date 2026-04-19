# Backend Folder Structure

This file documents the cleaned backend layout.

## Runtime (do not move)

- `app/`: FastAPI application code
- `run.py`: local server launcher
- `requirements.txt`: Python dependencies
- `.env`, `.env.example`: environment configuration
- `uploads/`: uploaded source files
- `logs/`: application logs

## Scripts

- `scripts/maintenance/`: DB reset/setup and data seed scripts
  - `clean_data.py`
  - `setup_word_db.py`
  - `seed_database.py`
  - `seed_suggestions.py`
  - `drop_database.py`
  - `reconnect_database.py`
- `scripts/diagnostics/`: parser/debug and API diagnostics scripts

## Tests and Fixtures

- `tests_debug/`: development and debugging tests
- `tests_debug/legacy_manual/`: legacy manual test scripts moved from backend root
- `tests_debug/fixtures/excel/`: local Excel test fixtures moved from backend root
- `tests_debug/artifacts/`: generated HTML/JSON/TXT test outputs

## Frequently Used Commands

Run from `backend/`:

```bash
python run.py
python scripts/maintenance/clean_data.py
python scripts/maintenance/setup_word_db.py
python scripts/diagnostics/excel_diagnostics.py
python tests_debug/legacy_manual/test_composer.py
```

## Notes

- Runtime behavior is unchanged; this cleanup only reorganizes non-runtime files.
- If you have old docs using `python clean_data.py` or `python test_*.py`, switch to the new paths above.
