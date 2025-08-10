from pydantic import BaseModel, PrivateAttr, Field
from langchain.llms.base import LLM
from typing import Optional, List, Dict, Any
import openai

class LMStudioLLM(LLM):
    model_name: str = Field(...)  # bắt buộc truyền
    api_key: str = Field(...)
    base_url: str = Field(...)
    _client: Any = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        self._client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

    @property
    def _llm_type(self) -> str:
        return "lm_studio"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        print(f'promt:{prompt}')
        messages = [{"role": "user", "content": prompt}]
        response = self._client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
            stop=stop
        )
        return response.choices[0].message.content
    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {"model_name": self.model_name}
