import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from pyrx_synapse import Synapse

load_dotenv()

app = Flask(__name__)

def get_synapse() -> Synapse:
    return Synapse(
        api_key=os.environ["SYNAPSE_API_KEY"],
        workspace_id=os.environ["SYNAPSE_WORKSPACE_ID"],
    )

@app.post("/api/track")
def track_event():
    body = request.get_json()
    with get_synapse() as client:
        client.track(
            external_id=body["user_id"],
            event_name=body["event"],
            attributes=body.get("attributes", {}),
        )
    return jsonify({"success": True})

@app.post("/api/identify")
def identify_contact():
    body = request.get_json()
    with get_synapse() as client:
        client.identify(
            external_id=body["user_id"],
            email=body["email"],
            properties=body.get("properties", {}),
        )
    return jsonify({"success": True})

@app.post("/api/send")
def send_email():
    body = request.get_json()
    with get_synapse() as client:
        client.send(
            template_slug=body["template_slug"],
            to={"user_id": body["user_id"], "email": body["email"]},
            attributes=body.get("attributes", {}),
        )
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
