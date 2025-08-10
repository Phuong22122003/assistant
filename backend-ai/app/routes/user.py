# routes/users.py
from flask import Blueprint, jsonify, request
from app.core import inject
from app.service import AgentService
import requests
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
bp = Blueprint('users', __name__)

@bp.route('/chat', methods=['POST'])
@inject
def chat(agent_service: AgentService):
    data = request.get_json()
    conversation = data.get('conversation')
    keycloak_id  = data.get('keycloakId')
    
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        jwt = auth_header.split(" ")[1]
        r.set(keycloak_id,jwt)
    if conversation is None:
        return jsonify({'error': 'Missing "conversation" field in request body'}), 400

    ai_message = agent_service.chat(conversation,keycloak_id)

    # Gửi kết quả tới Spring Boot
    try:
        callback_url = f"http://localhost:8080/ai-agent/sse/callback?keycloakId={keycloak_id}"
        response = requests.post(callback_url, json={"aiMessage": ai_message})
        response.raise_for_status()
    except requests.RequestException as e:
        print("Callback failed:", e)
        return jsonify({'error': 'Failed to send AI response to callback'}), 500

    return jsonify({'status': 'sent to callback'})
