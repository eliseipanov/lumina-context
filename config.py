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