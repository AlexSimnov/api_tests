from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv('BASE_URL')

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
