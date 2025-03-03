from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '0.0.0.0']

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
