# Sprint 1.5.3: Vision Worker Core Logic

Implement the base class for image analysis using Ollama and the dynamic prompt mapping.

## Tasks:
1. **Core Script (`vision_worker.py`)**:
   - Create a script that initializes the Ollama client using `VISION_MODEL_NAME` from `config.py`.
   - Implement a function to load the system prompt from `CURRENT_PROMPT_PATH`.

2. **Analysis Logic**:
   - The script must send an image (base64) and the system prompt to Ollama.
   - **Crucial**: Expected output from Ollama is a JSON (as defined in the prompt).

3. **Markdown Conversion**:
   - Implement a converter that takes the JSON response and saves individual `.md` files to `data/chunks/`.
   - **Format Template**:
     ---
     axis: {axis_name}
     tags: {tags_list + global_tags}
     source: {image_filename}
     ---
     {content}

4. **Testing**:
   - Create a simple entry point to test one single image from `data/raw_images/test_image.jpg`.

## Goal:
Successfully convert one image analysis into Lumina Markdown chunks.