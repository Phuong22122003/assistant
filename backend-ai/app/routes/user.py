# routes/users.py
from flask import Blueprint, jsonify, request
from app.core import inject
from app.service import AgentService
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
bp = Blueprint('users', __name__)

@bp.route('/chat', methods=['POST'])
@inject
def chat(agent_service: AgentService):
    data = request.get_json()
    conversation = data.get('message')
    keycloak_id  = data.get('keycloakId')
    print('keycloak_id',keycloak_id)
    
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        jwt = auth_header.split(" ")[1]
        r.set(keycloak_id,jwt)
    if conversation is None:
        return jsonify({'error': 'Missing "conversation" field in request body'}), 400

    conversation +=f"\nkeycloak_id: {keycloak_id}"
    return jsonify({'agent': agent_service.chat(conversation)})
