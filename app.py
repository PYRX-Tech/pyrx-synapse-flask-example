import os
import re
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from pyrx_synapse import Synapse

def _to_snake(name: str) -> str:
    return re.sub(r'([a-z])([A-Z])', r'\1_\2', name).lower()

def snake_keys(d):
    if isinstance(d, list):
        return [snake_keys(i) if isinstance(i, dict) else i for i in d]
    if isinstance(d, dict):
        return {_to_snake(k): snake_keys(v) if isinstance(v, (dict, list)) else v for k, v in d.items()}
    return d

load_dotenv()
app = Flask(__name__)

def get_synapse():
    return Synapse(api_key=os.environ["SYNAPSE_API_KEY"], workspace_id=os.environ["SYNAPSE_WORKSPACE_ID"], base_url=os.environ.get("SYNAPSE_API_URL", "https://synapse-api.pyrx.tech"))

@app.errorhandler(Exception)
def handle_error(e):
    status = getattr(e, 'status_code', None) or getattr(e, 'status', None) or 500
    return jsonify({"error": str(e)}), status

# Core
@app.post("/api/track")
def track_event():
    b = request.get_json()
    with get_synapse() as c:
        r = c.track(external_id=b["userId"], event_name=b["event"], attributes=b.get("attributes", {}))
    return jsonify(r)

@app.post("/api/track/batch")
def track_batch():
    b = request.get_json()
    with get_synapse() as c:
        r = c.track_batch(events=snake_keys(b["events"]))
    return jsonify(r)

@app.post("/api/identify")
def identify():
    b = request.get_json()
    with get_synapse() as c:
        r = c.identify(external_id=b["userId"], email=b.get("email"), properties=b.get("properties", {}))
    return jsonify(r)

@app.post("/api/identify/batch")
def identify_batch():
    b = request.get_json()
    with get_synapse() as c:
        r = c.identify_batch(contacts=snake_keys(b["contacts"]))
    return jsonify(r)

@app.post("/api/send")
def send():
    b = snake_keys(request.get_json())
    with get_synapse() as c:
        r = c.send(template_slug=b.get("template_slug", ""), to=b.get("to", {}), attributes=b.get("attributes", {}))
    return jsonify(r)

# Contacts
@app.get("/api/contacts")
def list_contacts():
    with get_synapse() as c:
        r = c.contacts.list(page=request.args.get("page", 1, type=int), per_page=request.args.get("limit", 20, type=int))
    return jsonify(r)

@app.get("/api/contacts/<cid>")
def get_contact(cid):
    with get_synapse() as c:
        r = c.contacts.get(cid)
    return jsonify(r)

@app.put("/api/contacts/<eid>")
def update_contact(eid):
    with get_synapse() as c:
        r = c.contacts.update(eid, data=request.get_json())
    return jsonify(r)

@app.delete("/api/contacts/<eid>")
def delete_contact(eid):
    with get_synapse() as c:
        c.contacts.delete(eid)
    return jsonify({"success": True})

# Templates
@app.get("/api/templates")
def list_templates():
    with get_synapse() as c:
        r = c.templates.list()
    return jsonify([t.__dict__ if hasattr(t, '__dict__') else t for t in r] if isinstance(r, list) else r)

@app.post("/api/templates")
def create_template():
    with get_synapse() as c:
        r = c.templates.create(request.get_json())
    return jsonify(r.__dict__ if hasattr(r, '__dict__') else r)

@app.get("/api/templates/<slug>")
def get_template(slug):
    with get_synapse() as c:
        r = c.templates.get(slug)
    return jsonify(r.__dict__ if hasattr(r, '__dict__') else r)

@app.put("/api/templates/<slug>")
def update_template(slug):
    with get_synapse() as c:
        r = c.templates.update(slug, params=request.get_json())
    return jsonify(r.__dict__ if hasattr(r, '__dict__') else r)

@app.delete("/api/templates/<slug>")
def delete_template(slug):
    with get_synapse() as c:
        c.templates.delete(slug)
    return jsonify({"success": True})

@app.post("/api/templates/<slug>/preview")
def preview_template(slug):
    with get_synapse() as c:
        r = c.templates.preview(slug, params=request.get_json())
    return jsonify(r.__dict__ if hasattr(r, '__dict__') else r)

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 4006)))
