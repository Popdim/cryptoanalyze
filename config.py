import os
from dotenv import load_dotenv

load_dotenv()
TOKEN_TG = os.getenv("TOKEN_TG")
ANN_KEY = os.getenv("ANN_KEY")
base_url = "https://api.proxyapi.ru/openai/v1"
