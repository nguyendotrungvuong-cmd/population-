import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT/".env")
def get_api():
    API = os.getenv("API")
    if not API:
        raise ValueError("MISSING API")
    return API
def get_url():
    URL = os.getenv("URL")
    if not URL:
        raise ValueError("MISSING URL")
    return URL