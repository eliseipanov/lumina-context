# Sprint 1.8.2: Registry State Management and Output Consolidation

## Tasks:
1. **Registry "Heartbeat"**: 
   - Before calling Ollama, the worker MUST update `registry.json` with status `PROCESSING`.
   - Save the registry IMMEDIATELY after this update so the placeholder is visible on disk.
   - After analysis, update status to `PROCESSED` or `ERROR` and save again.

2. **One Image = One File**:
   - Rewrite `save_consolidated_chunks` to merge ALL axes from the JSON into a single Markdown file.
   - Path: `/data/data_chunks/consolidated/[image_name]_[HASH].md`.
   - Use `## Axis Name` as headers for each section.

3. **Global YAML Header**:
   - Extract unique tags from ALL axes and place them in a single YAML header at the top of the file.

4. **Directory Cleanup**:
   - Stop splitting files into axis-specific subfolders. Everything goes to `/consolidated/`.

## Instruction:
The registry must act as a real-time status monitor. Ensure `save_registry()` is called twice per image: once to claim it (PROCESSING) and once to finish it (PROCESSED).