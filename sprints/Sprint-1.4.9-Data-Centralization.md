# Sprint 1.4.9: Data Centralization

We are moving all project content and terminology into a single `data/` directory to standardize the project structure.

## Actions:
1. **Physical Migration:** Move the following folders into the new `data/` root:
   - `raw_md/` -> `data/raw_md/`
   - `data_chunks/` -> `data/chunks/`
   - `vocab/` -> `data/vocab/`
   - `models/raw_poses/` -> `data/raw_poses/`
2. **Path Refactoring:** - Update all hardcoded paths in the codebase to reflect the new structure.
   - Update `.env` variables (PROJECT_ROOT, etc.).
   - Update MCP "Vanya" configuration to ensure the chunker and search tools point to `data/raw_md/` and `data/chunks/`.
3. **Registry:** Create `data/system/` for future metadata (e.g., `processed_hashes.json`).

## Goal:
The entire system (MCP, scripts etc) must work flawlessly with the new paths.