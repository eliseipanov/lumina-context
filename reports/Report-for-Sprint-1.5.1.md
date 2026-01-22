# Sprint 1.5.1: Vision Lab Infrastructure & Mapping - Report

## Overview
Successfully implemented the configuration layer for the upcoming Vision Worker. This sprint focused on infrastructure setup without processing logic.

## Completed Tasks

### 1. Environment Setup (.env)
- Added `VISION_MODEL_NAME=minicpm-v:latest` (default model)
- Added `VISION_BATCH_SIZE=5` (default batch size)

### 2. Configuration Mapping (config.py)
- Implemented `MODEL_PROMPT_MAP` dictionary:
  ```python
  MODEL_PROMPT_MAP = {
      "minicpm-v:latest": "live_ref_v1_minicpm-v.md",
      "moondream:latest": "live_ref_v1_moondream.md"
  }
  ```
- Added vision configuration variables:
  - `VISION_MODEL_NAME` loaded from environment
  - `VISION_BATCH_SIZE` loaded from environment with default fallback
- Defined `CURRENT_PROMPT_PATH` that dynamically resolves based on selected model

### 3. System Directory
- Created `data/system/` directory for future `processed_hashes.json` storage

### 4. Placeholder Prompts
- Added placeholder content to `schemas/prompts/live_ref_v1_minicpm-v.md`: `# Placeholder for minicpm-v`
- Added placeholder content to `schemas/prompts/live_ref_v1_moondream.md`: `# Placeholder for moondream`

## Verification Results

### Dynamic Prompt Resolution Test
Verified that `config.py` correctly resolves the prompt path when `VISION_MODEL_NAME` is changed:

- **Test 1**: `VISION_MODEL_NAME=minicpm-v:latest`
  - Result: `CURRENT_PROMPT_PATH = /var/www/chanker_vanya/schemas/prompts/live_ref_v1_minicpm-v.md`
  - Status: ✅ PASS

- **Test 2**: `VISION_MODEL_NAME=moondream:latest`
  - Result: `CURRENT_PROMPT_PATH = /var/www/chanker_vanya/schemas/prompts/live_ref_v1_moondream.md`
  - Status: ✅ PASS

The configuration layer successfully maps model names to their respective prompt files and dynamically updates the path based on environment settings.

## Files Modified
- `.env`: Added vision settings
- `config.py`: Added vision configuration and mapping logic
- `schemas/prompts/live_ref_v1_minicpm-v.md`: Added placeholder
- `schemas/prompts/live_ref_v1_moondream.md`: Added placeholder
- `data/system/`: Created directory

## Next Steps
The infrastructure is now ready for the Vision Worker implementation. The configuration layer provides:
- Model selection via environment variables
- Automatic prompt file resolution
- Extensible mapping for additional models
- System directory for processing state management

## Status
✅ **COMPLETED** - All tasks implemented and verified successfully.