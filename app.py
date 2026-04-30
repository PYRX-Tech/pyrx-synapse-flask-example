import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from pyrx_synapse import Synapse

load_dotenv()
app = Flask(__name__)

def get_synapse():
    return Synapse(api_key=os.environ["SYNAPSE_API_KEY"], workspace_id=os.environ["SYNAPSE_WORKSPACE_ID"], base_url=os.environ.get("SYNAPSE_API_URL", "https://synapse-api.pyrx.tech"))

@app.errorhandler(Exception)
def handle_error(e):
    status = getattr(e, 'status_code', 500) or getattr(e, 'status', 500) or 500
    return jsonify({"error": str(e)}), status

# Core
@app.post("/api/track")
def track_event():
    b = request.get_json()
    with get_synapse() as c: return jsonify(c.track(external_id=b["userId"], event_name=b["event"], attributes=b.get("attributes", {})))

@app.post("/api/track/batch")
def track_batch():
    with get_synapse() as c: return jsonify(c.track_batch(events=request.get_json()["events"]))

@app.post("/api/identify")
def identify():
    b = request.get_json()
    with get_synapse() as c: return jsonify(c.identify(external_id=b["userId"], email=b["email"], properties=b.get("properties", {})))

@app.post("/api/identify/batch")
def identify_batch():
    with get_synapse() as c: return jsonify(c.identify_batch(contacts=request.get_json()["contacts"]))

@app.post("/api/send")
def send():
    b = request.get_json()
    with get_synapse() as c: return jsonify(c.send(template_slug=b["templateSlug"], to={"user_id": b.get("userId",""), "email": b.get("email","")}, attributes=b.get("attributes", {})))

# Contacts
@app.get("/api/contacts")
def list_contacts():
    with get_synapse() as c: return jsonify(c.contacts.list(page=request.args.get("page", 1, type=int), limit=request.args.get("limit", 20, type=int)))

@app.get("/api/contacts/<cid>")
def get_contact(cid):
    with get_synapse() as c: return jsonify(c.contacts.get(cid))

@app.put("/api/contacts/<eid>")
def update_contact(eid):
    with get_synapse() as c: return jsonify(c.contacts.update(eid, data=request.get_json()))

@app.delete("/api/contacts/<eid>")
def delete_contact(eid):
    with get_synapse() as c: c.contacts.delete(eid)
    return jsonify({"success": True})

# Templates
@app.get("/api/templates")
def list_templates():
    with get_synapse() as c: return jsonify(c.templates.list())

@app.post("/api/templates")
def create_template():
    with get_synapse() as c: return jsonify(c.templates.create(request.get_json()))

@app.get("/api/templates/<slug>")
def get_template(slug):
    with get_synapse() as c: return jsonify(c.templates.get(slug))

@app.put("/api/templates/<slug>")
def update_template(slug):
    with get_synapse() as c: return jsonify(c.templates.update(slug, params=request.get_json()))

@app.delete("/api/templates/<slug>")
def delete_template(slug):
    with get_synapse() as c: c.templates.delete(slug)
    return jsonify({"success": True})

@app.post("/api/templates/<slug>/preview")
def preview_template(slug):
    with get_synapse() as c: return jsonify(c.templates.preview(slug, params=request.get_json()))

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 4006)))
