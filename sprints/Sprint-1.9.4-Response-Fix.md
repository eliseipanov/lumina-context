# Sprint 1.9.4: Response Structure & Storage Logic

## Tasks
1. **Prompts**: 
   - Replace `SYSTEM_SCHEMA_JSON` in `prompt_assembler.py` with the content of `schemas/prompts/minicpm_response_v1.json`.
2. **Worker (`vision_worker.py`)**:
   - Implement a loop to iterate through the `chunks` array from the model's JSON response.
   - For each chunk, save it to: `data/data_chunks/{axis_name}/{image_name}_{timestamp}.json`.
   - Validate `axis_name` against `LUMINA_ACTIVE_AXES`. 
   - If the axis is not in the active list, save the chunk to: `data/data_chunks/creative/`.
3. **Logs & Debug**:
   - Save the final assembled prompt to `logs/last_prompt.md`.
   - Save the formatted (pretty-print) model response to `logs/last_response.json`.
   - All logs must be in the `/logs/` directory with `DEBUG=true` level of detail.