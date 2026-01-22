# Sprint 1.5.1: Vision Lab Infrastructure & Mapping

Prepare the configuration layer for the upcoming Vision Worker. No processing logic yet, only infrastructure.

## Tasks:
1. **Environment Setup (.env):**
   - Add `VISION_MODEL_NAME` (e.g., "minicpm-v:latest").
   - Add `VISION_BATCH_SIZE` (default: 5).

2. **Configuration Mapping (config.py):**
   - Implement `MODEL_PROMPT_MAP`. A dictionary linking `VISION_MODEL_NAME` to specific prompt files.
   - Initial mapping:
     - "minicpm-v:latest" -> "live_ref_v1_minicpm-v.md"
     - "moondream:latest" -> "live_ref_v1_moondream.md"
   - Define `CURRENT_PROMPT_PATH` dynamically based on the selected model.

3. **System Directory:**
   - Ensure `data/system/` exists for future `processed_hashes.json`.

4. **Placeholder Prompts:**
   - If files `schemas/prompts/live_ref_v1_*.md` are missing or empty, create them with a simple comment: `# Placeholder for {model_name}`.

## Goal:
Verify that `config.py` correctly resolves the path to the system prompt when `VISION_MODEL_NAME` is changed in `.env`.