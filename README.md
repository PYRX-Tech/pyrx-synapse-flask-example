# Synapse Flask Example

All 16 SDK endpoints with [pyrx-synapse](https://pypi.org/project/pyrx-synapse/) + Flask.

## Setup

1. `python -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env`
4. `flask run` or `python app.py`

## Endpoints

**Core:** POST /api/track, /api/track/batch, /api/identify, /api/identify/batch, /api/send
**Contacts:** GET /api/contacts, GET/PUT/DELETE /api/contacts/<id>
**Templates:** GET/POST /api/templates, GET/PUT/DELETE /api/templates/<slug>, POST /api/templates/<slug>/preview

- [Synapse Docs](https://synapse.pyrx.tech/developers)
