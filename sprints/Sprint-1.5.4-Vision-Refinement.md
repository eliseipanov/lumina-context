# Sprint 1.5.4: Vision Worker Refinement & Bugfix

Refine `vision_worker.py` to handle real-world LVM outputs and ensure YAML compatibility.

## Tasks:
1. **JSON Robustness**:
   - Update `analyze_image` to include `"format": "json"` in the Ollama payload.
   - Implement a cleaner for `result['response']` to strip potential markdown blocks (e.g., ```json ... ```) before `json.loads()`.
   - Increase `timeout` to 180 seconds to account for tunnel latency and LVM processing.

2. **Schema Alignment**:
   - Change the processing logic in `process_analysis_result` to look for the key `chunks` (as defined in the prompt) 

3. **YAML Formatting**:
   - In `save_chunk`, ensure the `tags` list is formatted as a valid YAML array (e.g., using `json.dumps(tags)`).

4. **Directory Correction**:
   - Ensure the output path is strictly `data/data_chunks/{axis}/` and the code correctly creates these subdirectories.

## Goal:
Stable processing of image analysis results into correctly formatted Markdown chunks.