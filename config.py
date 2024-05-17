from dotenv import load_dotenv
import os

load_dotenv()

USER_NAME = os.getenv("USER_NAME")
USER_PASS = os.getenv("USER_PASS")
API_KEY = os.getenv("API_KEY")
