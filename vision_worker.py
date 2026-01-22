import os
import base64
import json
import requests
import re
import time
import config
from datetime import datetime

def log(message):
    """Log message with timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")

def sanitize_axis_name(axis):
    """Sanitize axis name for directory use."""
    return re.sub(r'[^\w\-_]', '', axis)

def load_prompt():
    """Load the system prompt from CURRENT_PROMPT_PATH."""
    log(f"Loading prompt from {config.CURRENT_PROMPT_PATH}")
    if not config.CURRENT_PROMPT_PATH or not os.path.exists(config.CURRENT_PROMPT_PATH):
        raise FileNotFoundError(f"Prompt file not found: {config.CURRENT_PROMPT_PATH}")
    with open(config.CURRENT_PROMPT_PATH, 'r', encoding='utf-8') as f:
        prompt = f.read().strip()
    log(f"Prompt loaded successfully ({len(prompt)} characters)")
    return prompt

def encode_image(image_path):
    """Encode image to base64."""
    log(f"Encoding image {image_path}")
    with open(image_path, 'rb') as f:
        encoded = base64.b64encode(f.read()).decode('utf-8')
    log(f"Image encoded successfully ({len(encoded)} characters)")
    return encoded

def analyze_image(image_path, prompt):
    """Send image and prompt to Ollama and get JSON response."""
    start_time = time.time()
    log(f"Starting analysis for {image_path}")

    url = f"{config.OLLAMA_URL}/api/generate"
    image_b64 = encode_image(image_path)

    payload = {
        "model": config.VISION_MODEL_NAME,
        "prompt": prompt,
        "images": [image_b64],
        "format": "json",
        "stream": True
    }

    log(f"Sending streaming request to Ollama at {url}")
    response = requests.post(url, json=payload, timeout=180, stream=True)
    response.raise_for_status()

    accumulated_response = ""
    log("Waiting for Ollama stream...")

    for line in response.iter_lines(decode_unicode=True):
        if line:
            try:
                chunk = json.loads(line)
                if 'response' in chunk:
                    accumulated_response += chunk['response']
                    print(".", end="", flush=True)  # Visual heartbeat
                if chunk.get('done', False):
                    break
            except json.JSONDecodeError:
                continue  # Skip malformed lines

    print()  # New line after dots
    log(f"Stream completed, accumulated {len(accumulated_response)} characters")

    # Save raw accumulated response for debugging
    if config.DEBUG_MODE:
        debug_path = os.path.join(config.PROJECT_ROOT, 'data', 'logs', 'last_raw_response.json')
        os.makedirs(os.path.dirname(debug_path), exist_ok=True)
        with open(debug_path, 'w', encoding='utf-8') as f:
            json.dump({"response": accumulated_response}, f, indent=2)
        log(f"Raw response saved to {debug_path}")

    # Clean the response to remove markdown blocks
    response_text = accumulated_response.strip()
    response_text = re.sub(r'^```json\s*', '', response_text)
    response_text = re.sub(r'\s*```$', '', response_text)

    try:
        parsed = json.loads(response_text)
        duration = time.time() - start_time
        log(f"Analysis completed successfully in {duration:.2f} seconds")
        return parsed
    except json.JSONDecodeError as e:
        log(f"JSON parsing failed: {e}")
        log(f"Failed string (first 200 chars): {response_text[:200]}")
        raise

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
            raw_axis = chunk.get('axis', 'Unknown')
            axes = [sanitize_axis_name(ax.strip()) for ax in raw_axis.split('|') if ax.strip()]
            log(f"Detected axes: {axes}")
            content = chunk.get('content', '')
            tags = chunk.get('tags', [])
            for axis in axes:
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
    log("Starting vision_worker test")

    # Test connection
    success, message = test_ollama_connection()
    log(f"Ollama connection: {message}")
    if not success:
        exit(1)

    # Test with sample image
    test_image = "data/raw_images/test_image2.jpg"
    if not os.path.exists(test_image):
        log(f"Test image not found: {test_image}")
        exit(1)

    try:
        prompt = load_prompt()
        result = analyze_image(test_image, prompt)
        saved_files = process_analysis_result(result, test_image)
        log(f"Analysis complete. Saved {len(saved_files)} chunks: {saved_files}")
    except Exception as e:
        log(f"Error: {e}")
        exit(1)