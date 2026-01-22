import os
from dotenv import load_dotenv

load_dotenv()

# Проксі збираємо назад у словник
proxy_url = os.getenv('PROXY_URL', '').strip()
PROXIES = {
    'http': proxy_url,
    'https': proxy_url
} if proxy_url else None

# UA розбиваємо назад у список
ua_string = os.getenv('UA_LIST', '').strip().strip('"').strip()
UA_LIST = [ua.strip() for ua in ua_string.split(';')] if ua_string else []

# Шляхи
PROJECT_ROOT = os.getenv('PROJECT_ROOT', '/var/www/chanker_vanya').strip()
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
CHUNKS_DIR = os.path.join(DATA_DIR, 'data_chunks')
RAW_MD_DIR = os.path.join(DATA_DIR, 'raw_md')
RAW_POSES_DIR = os.path.join(DATA_DIR, 'raw_poses')
VOCAB_DIR = os.path.join(DATA_DIR, 'vocab')
REPORTS_DIR = os.path.join(PROJECT_ROOT, 'reports')
SPRINTS_DIR = os.path.join(PROJECT_ROOT, 'sprints')

# Vision Configuration
OLLAMA_URL = os.getenv('OLLAMA_URL', '').strip()
VISION_MODEL_NAME = os.getenv('VISION_MODEL_NAME', '').strip()
VISION_BATCH_SIZE = int(os.getenv('VISION_BATCH_SIZE', 5))

MODEL_PROMPT_MAP = {
    "minicpm-v:latest": os.getenv('VISION_PROMPT_MINICPM', 'live_ref_v1_minicpm-v.md').strip(),
    "moondream:latest": os.getenv('VISION_PROMPT_MOONDREAM', 'live_ref_v1_moondream.md').strip()
}

CURRENT_PROMPT_PATH = os.path.join(PROJECT_ROOT, 'schemas', 'prompts', MODEL_PROMPT_MAP.get(VISION_MODEL_NAME)) if VISION_MODEL_NAME else None