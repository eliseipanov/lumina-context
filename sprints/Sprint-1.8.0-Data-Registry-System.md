# Sprint 1.8.0: Global Registry and Directory Targeting

Implement a central registry for hash tracking and enable targeted directory re-processing.

## Tasks:
1. **Global Registry**:
   - Create `/data/registry.json` to store `{hash: {status, path, timestamp}}`.
     By default only images in registry with status "NOT_PROCESSED" are going to queue
2. **Axis File Consolidation**:
   - Ensure all chunks for the SAME axis from ONE image are saved into a single `[image_name]_[HASH].md` file.
3. **Targeted Scanning**:
   - Implement logic for `RELAB_SPECIFIC_DIR` (=true or =false. Default is 'false').
   - If enabled, force re-processing of all images in the specified sub-directory specified as SPECIFIC_DIR, updating the registry and overwriting old `.md` chunks. 
   Important! The variable VISION_BATCH_SIZE in .env still must be used.
4. **Hashing Engine**:
   - Finalize the SHA-256 worker to scan `data/raw_images` recursively.

## Instruction:
Build the registry system. The worker must now check `registry.json` before any API call to Ollama.