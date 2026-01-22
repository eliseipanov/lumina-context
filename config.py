import os
from dotenv import load_dotenv

load_dotenv()

# Проксі збираємо назад у словник
proxy_url = os.getenv('PROXY_URL')
PROXIES = {
    'http': proxy_url,
    'https': proxy_url
} if proxy_url else None

# UA розбиваємо назад у список
ua_string = os.getenv('UA_LIST', '')
UA_LIST = ua_string.split(';') if ua_string else []

# Шляхи
PROJECT_ROOT = os.getenv('PROJECT_ROOT', '/var/www/chanker_vanya')
RAW_DIR = os.path.join(PROJECT_ROOT, 'raw_content')
CHUNKS_DIR = os.path.join(PROJECT_ROOT, 'data_chunks')
RAW_MD_DIR = os.path.join(PROJECT_ROOT, 'raw_md')
REPORTS_DIR = os.path.join(PROJECT_ROOT, 'reports')
SPRINTS_DIR = os.path.join(PROJECT_ROOT, 'sprints')