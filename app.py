import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from pyrx_synapse import Synapse

load_dotenv()
app = Flask(__name__)

def get_synapse() -> Synapse:
    return Synapse(api_key=os.environ["SYNAPSE_API_KEY"], workspace_id=os.environ["SYNAPSE_WORKSPACE_ID"], base_url=os.environ.get("SYNAPSE_API_URL", "https://synapse-api.pyrx.tech"))

# ── Core ──
@app.post("/api/track")
def track_event():
    b = request.get_json()
    with get_synapse() as c:
        r = c.track(external_id=b["user_id"], event_name=b["event"], attributes=b.get("attributes", {}))
    return jsonify(r)

@app.post("/api/track/batch")
def track_batch():
    with get_synapse() as c:
        r = c.track_batch(events=request.get_json()["events"])
    return jsonify(r)

@app.post("/api/identify")
def identify_contact():
    b = request.get_json()
    with get_synapse() as c:
        r = c.identify(external_id=b["user_id"], email=b["email"], properties=b.get("properties", {}), tags=b.get("tags", []))
    return jsonify(r)

@app.post("/api/identify/batch")
def identify_batch():
    with get_synapse() as c:
        r = c.identify_batch(contacts=request.get_json()["contacts"])
    return jsonify(r)

@app.post("/api/send")
def send_email():
    b = request.get_json()
    with get_synapse() as c:
        r = c.send(template_slug=b["template_slug"], to={"user_id": b["user_id"], "email": b["email"]}, attributes=b.get("attributes", {}))
    return jsonify(r)

# ── Contacts ──
@app.get("/api/contacts")
def list_contacts():
    with get_synapse() as c:
        r = c.contacts.list(page=request.args.get("page", 1, type=int), limit=request.args.get("limit", 20, type=int), tag=request.args.get("tag"), search=request.args.get("search"))
    return jsonify(r)

@app.get("/api/contacts/<contact_id>")
def get_contact(contact_id):
    with get_synapse() as c:
        r = c.contacts.get(contact_id)
    return jsonify(r)

@app.put("/api/contacts/<external_id>")
def update_contact(external_id):
    with get_synapse() as c:
        r = c.contacts.update(external_id, data=request.get_json())
    return jsonify(r)

@app.delete("/api/contacts/<external_id>")
def delete_contact(external_id):
    with get_synapse() as c:
        c.contacts.delete(external_id)
    return jsonify({"success": True})

# ── Templates ──
@app.get("/api/templates")
def list_templates():
    with get_synapse() as c:
        r = c.templates.list()
    return jsonify(r)

@app.post("/api/templates")
def create_template():
    with get_synapse() as c:
        r = c.templates.create(request.get_json())
    return jsonify(r)

@app.get("/api/templates/<slug>")
def get_template(slug):
    with get_synapse() as c:
        r = c.templates.get(slug)
    return jsonify(r)

@app.put("/api/templates/<slug>")
def update_template(slug):
    with get_synapse() as c:
        r = c.templates.update(slug, params=request.get_json())
    return jsonify(r)

@app.delete("/api/templates/<slug>")
def delete_template(slug):
    with get_synapse() as c:
        c.templates.delete(slug)
    return jsonify({"success": True})

@app.post("/api/templates/<slug>/preview")
def preview_template(slug):
    with get_synapse() as c:
        r = c.templates.preview(slug, params={"attributes": request.get_json().get("attributes", {})})
    return jsonify(r)

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 4006)))
