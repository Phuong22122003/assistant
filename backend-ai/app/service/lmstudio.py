from pydantic import BaseModel, PrivateAttr, Field
from langchain.llms.base import LLM
from typing import Optional, List, Dict, Any
import openai
from google import genai
class LMStudioLLM(LLM):
    model_name: str = Field(...)  # bắt buộc truyền
    api_key: str = Field(...)
    _client: Any = PrivateAttr()

    def __init__(self,**data):
        super().__init__(**data)
        self._client = genai.Client(api_key="AIzaSyC25KhSrP9q6CPmGppr44vUVZASFXFsR6g")
    @property
    def _llm_type(self) -> str:
        return "lm_studio"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = self._client.models.generate_content(
            model=self.model_name, 
            contents= prompt
            )
        return response.text
    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {"model_name": self.model_name}
