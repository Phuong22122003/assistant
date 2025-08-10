# services/user_service.py
from app.core import service
from config import *
from langchain_together import ChatTogether
import json
from langchain.agents import initialize_agent, AgentType
from .tools import *
from app.prompt import create_prompt
from .lmstudio import LMStudioLLM
@service
class AgentService:
    def __init__(self):
        self.llm = LMStudioLLM(
            api_key=API_KEY,
            model_name=LLM_MODEL_NAME
        )

        self.agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            max_iterations=5,
            handle_parsing_errors=True
        )
    def chat(self, conversation, keycloak_id):
        return self.agent.invoke(create_prompt(conversation,keycloak_id))['output']