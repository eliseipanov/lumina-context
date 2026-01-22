import os
import base64
import json
import requests
import re
import config
from datetime import datetime

def load_prompt():
    """Load the system prompt from CURRENT_PROMPT_PATH."""
    if not config.CURRENT_PROMPT_PATH or not os.path.exists(config.CURRENT_PROMPT_PATH):
        raise FileNotFoundError(f"Prompt file not found: {config.CURRENT_PROMPT_PATH}")
    with open(config.CURRENT_PROMPT_PATH, 'r', encoding='utf-8') as f:
        return f.read().strip()

def encode_image(image_path):
    """Encode image to base64."""
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def analyze_image(image_path, prompt):
    """Send image and prompt to Ollama and get JSON response."""
    url = f"{config.OLLAMA_URL}/api/generate"
    image_b64 = encode_image(image_path)

    payload = {
        "model": config.VISION_MODEL_NAME,
        "prompt": prompt,
        "images": [image_b64],
        "format": "json",
        "stream": False
    }

    response = requests.post(url, json=payload, timeout=180)
    response.raise_for_status()
    result = response.json()

    # Clean the response to remove markdown blocks
    response_text = result['response'].strip()
    response_text = re.sub(r'^```json\s*', '', response_text)
    response_text = re.sub(r'\s*```$', '', response_text)

    return json.loads(response_text)

def save_chunk(axis, content, tags, source):
    """Save a chunk as Markdown with YAML header."""
    axis_dir = os.path.join(config.CHUNKS_DIR, axis)
    os.makedirs(axis_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%H%M%S')
    slug = os.path.splitext(os.path.basename(source))[0]
    filename = f"{timestamp}_{slug}_chunk.md"
    filepath = os.path.join(axis_dir, filename)

    yaml_header = f"---\naxis: {axis}\ntags: {json.dumps(tags)}\nsource: {source}\n---\n\n"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(yaml_header + content)

    return filepath

def process_analysis_result(result, image_path):
    """Process the JSON result and save chunks."""
    saved_files = []
    if 'chunks' in result:
        for chunk in result['chunks']:
            axis = chunk.get('axis', 'Unknown')
            content = chunk.get('content', '')
            tags = chunk.get('tags', [])
            filepath = save_chunk(axis, content, tags, os.path.basename(image_path))
            saved_files.append(filepath)
    return saved_files

def test_ollama_connection():
    """Test connection to Ollama."""
    try:
        url = f"{config.OLLAMA_URL}/api/tags"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return True, "Connection successful"
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    # Test connection
    success, message = test_ollama_connection()
    print(f"Ollama connection: {message}")
    if not success:
        exit(1)

    # Test with sample image
    test_image = "data/raw_images/test_image.jpg"
    if not os.path.exists(test_image):
        print(f"Test image not found: {test_image}")
        exit(1)

    try:
        prompt = load_prompt()
        result = analyze_image(test_image, prompt)
        saved_files = process_analysis_result(result, test_image)
        print(f"Analysis complete. Saved {len(saved_files)} chunks: {saved_files}")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)