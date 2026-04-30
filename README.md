# Synapse Flask Example

Example showing how to use [pyrx-synapse](https://pypi.org/project/pyrx-synapse/) with Flask.

## Setup

1. `python -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env`
4. `flask run` or `python app.py`

## Endpoints

- `POST /api/track` — Track an event
- `POST /api/identify` — Identify a contact
- `POST /api/send` — Send email

## Learn more

- [Synapse Documentation](https://synapse.pyrx.tech/developers)
- [Python SDK Reference](https://synapse.pyrx.tech/developers/sdks/python)
