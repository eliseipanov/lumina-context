# Sprint 1.6.3: Axis Sanitization and Multi-Axis Splitting

Fix the issue where the model returns combined axes (e.g., "Domain|Luminance") which breaks the directory structure.

## Tasks:
1. **Axis Logic Update**:
   - In `process_analysis_result`, if a chunk's `axis` field contains a pipe `|`, the worker must treat this chunk as applying to BOTH axes.
   - Save a copy of the `.md` file in each respective axis directory (e.g., one in `data/data_chunks/Domain/` and one in `data/data_chunks/Luminance/`).
2. **Directory Naming**:
   - Strip any special characters from axis names before using them as folder names to prevent OS errors.
3. **Log Expansion**:
   - Print the detected `Domain` in the main log so the Lead can see the classification without opening files.

## Goal:
Ensure a clean directory structure regardless of how the model groups the JSON output.