"""App settings, read from environment variables / the .env file."""
import os
from pathlib import Path

from dotenv import load_dotenv

# theprocess/ (the folder that holds app/, requirements.txt, .env)
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

# Path to YOUR Firebase service account key. Each teammate downloads their own
# from Firebase Console > Project settings > Service accounts. Never commit it.
# Default: theprocess/serviceAccountKey.json (ignored by .gitignore).
FIREBASE_KEY_PATH = Path(
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS", BASE_DIR / "serviceAccountKey.json")
)
