import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_PATH")
SECRET_KEY = os.getenv("SECRET_KEY")