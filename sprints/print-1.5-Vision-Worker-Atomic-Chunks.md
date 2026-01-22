# Sprint 1.5: Vision Lab - Atomic Axis Worker

We are implementing a sequential background worker to process images from `models/raw_poses/` and convert LVM analysis into atomic Markdown chunks.

## Core Logic:
- Process images one-by-one to respect VPS RAM limits (8GB).
- Use SHA-256 hashing to avoid re-processing (registry: `data/processed_hashes.json`).
- Convert LVM JSON output into multiple Markdown files based on identified Lumina Axes.

## Tasks:
1. **Deduplication:** Calculate SHA-256 for each file in `models/raw_poses/`. Skip if hash exists in registry.
2. **LVM Integration:** Call Ollama API using modular prompts from `schemas/prompts/`.
3. **Atomic Axis Routing:** - Parse the LVM response. 
   - For each axis (e.g., Somatic, Luminance, Optical), create a separate `.md` file in the corresponding `data_chunks/[axis_name]/` directory.
   - Filename format: `vision_[hash].md`.
4. **Markdown Format:**
   - Use YAML frontmatter: `tags` (include 'live' or 'recognized'), `source_path`, `hash`, `axis`.
   - Body: The descriptive text provided by the model for that specific axis.
5. **Loop:** Implement a 10-second wait cycle between folder scans.