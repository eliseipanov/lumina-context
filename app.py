import trafilatura
import requests
import json
import os
import random
import re
from datetime import datetime
import config as config 

def vanya_cleaner(text):
    """Видаляє сміття, яке заважає AI"""
    text = re.sub(r'\[\d+\]', '', text) # Прибираємо [1], [2]
    text = text.replace('Advertisement', '')
    return text.strip()

def vanya_monolith():
    url = config.START_URL
    print(f"--- [ВАНЯ] Запуск конвеєра: {url} ---")

    # 1. FETCH + RAW STORAGE
    try:
        res = requests.get(url, headers={'User-Agent': random.choice(config.UA_LIST)}, 
                           proxies=config.PROXIES, timeout=20)
        res.raise_for_status()
        html_raw = res.text
        
        # Миттєвий дамп
        if not os.path.exists("raw_content"): os.makedirs("raw_content")
        slug = url.split('/')[-1] or "index"
        raw_path = f"raw_content/{slug}_{datetime.now().strftime('%H%M%S')}.html"
        with open(raw_path, "w", encoding="utf-8") as f:
            f.write(html_raw)
        print(f"--- [ВАНЯ] Raw-копія збережена: {raw_path}")
        
    except Exception as e:
        print(f"!!! [FETCH ERROR]: {e}"); return

    # 2. MARKDOWN EXTRACTION (The AI Way)
    md_content = trafilatura.extract(html_raw, include_formatting=True, output_format='markdown')
    if not md_content:
        print("!!! [EXTRACTION ERROR]: Не вдалося отримати Markdown."); return

    # 3. CHUNKING (Логіка заголовок-текст)
    # Шукаємо блоки, що починаються з ** (жирного тексту)
    matches = re.findall(r'\*\*(.*?)\*\*(.*?)(?=\*\*|$)', md_content, re.DOTALL)
    
    final_dataset = []
    for label, content in matches:
        clean_label = label.strip()
        clean_content = vanya_cleaner(content)
        
        if len(clean_label) > 3 and len(clean_content) > 10:
            final_dataset.append({
                "label": clean_label,
                "content": clean_content,
                "source": url,
                "created_at": datetime.now().isoformat()
            })

    # 4. EXPORT TO JSON
    if not os.path.exists("data_chunks"): os.makedirs("data_chunks")
    out_path = f"data_chunks/{slug}.json"
    
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(final_dataset, f, ensure_ascii=False, indent=4)

    print(f"--- [ВАНЯ] Успіх! Створено чанків: {len(final_dataset)}")
    print(f"--- [ВАНЯ] JSON: {out_path}")

if __name__ == "__main__":
    vanya_monolith()