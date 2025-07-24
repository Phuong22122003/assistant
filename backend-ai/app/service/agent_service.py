# services/user_service.py
from app.core import service
from config import *
from langchain_together import ChatTogether
import json
from langchain.agents import initialize_agent, AgentType
from .tools import *
from app.prompt import create_prompt
@service
class AgentService:
    def __init__(self):
        self.llm =  ChatTogether(
            together_api_key= API_KEY,
            model=LLM_MODEL_NAME
        )
        self.agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            max_iterations=5,
            handle_parsing_errors=True
        )
    def chat(self, conversation):
        return self.agent.invoke(create_prompt(conversation))['output']