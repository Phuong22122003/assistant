import os
DEBUG = True
API_KEY = 'AIzaSyC25KhSrP9q6CPmGppr44vUVZASFXFsR6g'
LLM_MODEL_NAME  = 'gemini-2.5-flash' # deepseek-ai/DeepSeek-V3

TOGETHER_LLM_MODEL_NAME  = "deepseek-ai/DeepSeek-V3"
TOGETHER_API_KEY = '7c3a24eae57b61625a17c35af628a8d1a81583e86cff62cd6f6f5769805d0c48'

ROOM_BOOKING_API_URL = ''
CHECK_AVAILABLE_ROOM_API_URL = ''

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

SCHEDULE_API = os.getenv('SCHEDULE_SERVICE_URL','http://localhost:8080')