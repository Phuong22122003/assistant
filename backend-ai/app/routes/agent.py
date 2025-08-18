# routes/users.py
from config import *
from flask import Blueprint, jsonify, request
from app.core import inject
from app.service import AgentService
import requests
import redis
import time
import logging
from datetime import datetime
import os
# ANSI console color
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

# logging file config
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "chat.log")

logging.basicConfig(
    filename=log_file,
    filemode="a",
    encoding="utf-8", 
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
r = redis.from_url(REDIS_URL)
bp = Blueprint('users', __name__)

@bp.route('/chat', methods=['POST'])
@inject
def chat(agent_service: AgentService):
    start_time = time.perf_counter()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = request.get_json()
    conversation = data.get('conversation')
    keycloak_id = data.get('keycloakId')

    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        jwt = auth_header.split(" ")[1]
        r.set(keycloak_id, jwt)

    if conversation is None:
        return jsonify({'error': 'Missing "conversation" field in request body'}), 400
    ai_message = agent_service.chat(conversation, keycloak_id)

    try:
        callback_url = f"{SCHEDULE_API}/ai-agent/sse/callback?keycloakId={keycloak_id}"
        response = requests.post(callback_url, json={"aiMessage": ai_message})
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"{RED} [Callback Error]{RESET}", e)
        logging.error(f"[Callback Error] {e}")
        return jsonify({'error': 'Failed to send AI response to callback'}), 500

    elapsed_time = (time.perf_counter() - start_time) * 1000

    # Console log có màu
    print(f"\n{GREEN}{'='*25} START TIME {now_str} {'='*25}{RESET}")
    print(f"   ➤ Keycloak ID : {keycloak_id}")
    print(f"   ➤ Conversation: {conversation}")
    print(f"   ➤ AI Message  : {ai_message}")
    print(f"   ⚡ Response Time: {elapsed_time:.2f} ms")
    print(f"{RED}{'='*26} END TIME {'='*26}{RESET}\n")

    logging.info("\n" + "="*70)
    logging.info(f"START TIME: {now_str}")
    logging.info(f"Keycloak ID: {keycloak_id}")
    logging.info(f"Conversation: {conversation}")
    logging.info(f"AI Message: {ai_message}")
    logging.info(f"Response Time: {elapsed_time:.2f} ms")
    logging.info(f"END TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info("="*70 + "\n")

    return jsonify({'status': 'sent to callback'})
