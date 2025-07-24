# routes/users.py
from flask import Blueprint, jsonify, request
from app.core import inject
from app.service import AgentService

bp = Blueprint('users', __name__)

@bp.route('/chat', methods=['POST'])
@inject
def chat(agent_service: AgentService):
    data = request.get_json()
    conversation = data.get('conversation')

    if conversation is None:
        return jsonify({'error': 'Missing "conversation" field in request body'}), 400

    return jsonify({'agent': agent_service.chat(conversation)})
