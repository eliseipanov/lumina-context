import os
import base64
import json
import requests
import re
import time
import hashlib
import config
from datetime import datetime

def log(message):
    """Log message with timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")

def sanitize_axis_name(axis):
    """Sanitize axis name for directory use."""
    return re.sub(r'[^\w\-_]', '', axis)

def load_registry():
    """Load the processing registry."""
    registry_path = os.path.join(config.PROJECT_ROOT, 'data', 'registry.json')
    if os.path.exists(registry_path):
        with open(registry_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_registry(registry):
    """Save the processing registry."""
    registry_path = os.path.join(config.PROJECT_ROOT, 'data', 'registry.json')
    with open(registry_path, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2)

def calculate_image_hash(image_path):
    """Calculate SHA-256 hash of image file."""
    hash_sha256 = hashlib.sha256()
    with open(image_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

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

def save_consolidated_chunks(axis, chunks, image_name, image_hash):
    """Save all chunks for an axis from one image into a single file."""
    axis_dir = os.path.join(config.CHUNKS_DIR, axis)
    os.makedirs(axis_dir, exist_ok=True)

    filename = f"{image_name}_{image_hash}.md"
    filepath = os.path.join(axis_dir, filename)

    # Collect all tags
    all_tags = list(set(tag for chunk in chunks for tag in chunk['tags']))

    # Concatenate contents with separators
    contents = []
    for i, chunk in enumerate(chunks):
        if i > 0:
            contents.append("\n---\n")
        contents.append(chunk['content'])

    full_content = ''.join(contents)

    yaml_header = f"---\naxis: {axis}\ntags: {json.dumps(all_tags)}\nsource: {image_name}\n---\n\n"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(yaml_header + full_content)

    return filepath

def process_analysis_result(result, image_path, image_hash):
    """Process the JSON result and save consolidated chunks."""
    saved_files = []
    image_name = os.path.splitext(os.path.basename(image_path))[0]

    if 'chunks' in result:
        # Group chunks by axis
        axis_chunks = {}
        for chunk in result['chunks']:
            raw_axis = chunk.get('axis', 'Unknown')
            axes = [sanitize_axis_name(ax.strip()) for ax in raw_axis.split('|') if ax.strip()]
            log(f"Detected axes: {axes}")
            content = chunk.get('content', '')
            tags = chunk.get('tags', [])
            for axis in axes:
                if axis not in axis_chunks:
                    axis_chunks[axis] = []
                axis_chunks[axis].append({'content': content, 'tags': tags})

        # Save consolidated files
        for axis, chunks in axis_chunks.items():
            filepath = save_consolidated_chunks(axis, chunks, image_name, image_hash)
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
    log("Starting vision_worker with registry system")

    # Test connection
    success, message = test_ollama_connection()
    log(f"Ollama connection: {message}")
    if not success:
        exit(1)

    # Load registry
    registry = load_registry()
    log(f"Loaded registry with {len(registry)} entries")

    # Determine scan directory
    if config.RELAB_SPECIFIC_DIR and config.SPECIFIC_DIR:
        scan_dir = os.path.join(config.PROJECT_ROOT, 'data', 'raw_images', config.SPECIFIC_DIR)
        log(f"Re-processing specific directory: {scan_dir}")
        # Mark all images in this dir as NOT_PROCESSED
        for hash_val, entry in registry.items():
            if entry['path'].startswith(scan_dir):
                entry['status'] = 'NOT_PROCESSED'
                entry['timestamp'] = datetime.now().isoformat()
    else:
        scan_dir = os.path.join(config.PROJECT_ROOT, 'data', 'raw_images')
        log(f"Scanning directory: {scan_dir}")

    # Scan for images
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
    images_to_process = []
    for root, dirs, files in os.walk(scan_dir):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_path = os.path.join(root, file)
                image_hash = calculate_image_hash(image_path)
                if image_hash not in registry or registry[image_hash]['status'] == 'NOT_PROCESSED':
                    images_to_process.append((image_path, image_hash))
                    registry[image_hash] = {
                        'status': 'NOT_PROCESSED',
                        'path': image_path,
                        'timestamp': datetime.now().isoformat()
                    }

    log(f"Found {len(images_to_process)} images to process")

    # Process in batches
    batch_size = config.VISION_BATCH_SIZE
    processed_count = 0

    try:
        prompt = load_prompt()
        for i in range(0, len(images_to_process), batch_size):
            batch = images_to_process[i:i + batch_size]
            log(f"Processing batch {i//batch_size + 1} with {len(batch)} images")

            for image_path, image_hash in batch:
                try:
                    log(f"Processing {image_path}")
                    result = analyze_image(image_path, prompt)
                    saved_files = process_analysis_result(result, image_path, image_hash)
                    registry[image_hash]['status'] = 'PROCESSED'
                    registry[image_hash]['timestamp'] = datetime.now().isoformat()
                    processed_count += 1
                    log(f"Completed {image_path}, saved {len(saved_files)} files")
                except Exception as e:
                    log(f"Error processing {image_path}: {e}")
                    registry[image_hash]['status'] = 'ERROR'
                    registry[image_hash]['timestamp'] = datetime.now().isoformat()

        save_registry(registry)
        log(f"Processing complete. Processed {processed_count} images. Registry saved.")

    except Exception as e:
        log(f"Critical error: {e}")
        save_registry(registry)
        exit(1)