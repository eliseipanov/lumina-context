# Sprint 1.9.0: Reverting to Atomic Axes and Fixing Timeouts

This sprint fixes the results consolidation error and resolves the batch processing interruption issue caused by Read Timeouts.

## Tasks

1. **Timeout Configuration (config.py & .env):**
   - Add `VISION_REQUEST_TIMEOUT=600` variable to the `.env` file.
   - Update `config.py` to read this variable (default to 600).
   - REPLACE the hardcoded `timeout=180` in `vision_worker.py` with `config.VISION_REQUEST_TIMEOUT`.

2. **Removal of Consolidation Logic (vision_worker.py):**
   - COMPLETELY REMOVE the logic for saving results into the `consolidated/` folder.
   - Delete any functions or code blocks that attempt to merge results from different axes into a single file.

3. **Restoration of Atomic Saving:**
   - Implement logic where the analysis result of each image is split into separate files based on keys (axes) from the Ollama JSON response.
   - Save path format: `data/data_chunks/{axis_name}/{image_name}_{img_hash}.md`.
   - Each file must contain a YAML header (axis, tags, image, hash) and the corresponding description.

4. **Batch Processing Stability:**
   - Ensure that in case of a `Read timed out` or any other error for a single image, the script logs the `ERROR` status in `registry.json` and PROCEEDS to the next image without terminating the entire worker process.