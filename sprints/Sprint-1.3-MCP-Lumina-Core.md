# Sprint 1.3: MCP Tools for Lumina Context Analysis

## Context
The "Vanya" MCP tool successfully fetches and cleans URLs but currently acts as a "black box" for the LLM (Kwen). Kwen can't read the resulting Markdown or store structured chunks according to the 6 Lumina Axes (Optical, Luminance, Somatic, Psychographic, Material, Compositional).

## Objectives
1. Implement `read_processed_md(filepath: str)` tool to return the content of cleaned Markdown files.
2. Implement `store_lumina_chunk(axis: str, content: str, tags: list, source_url: str)` tool to save analyzed data.
3. Update `vanya_mcp.py` to register these tools.

## Technical Requirements
- **Tool 1: `read_processed_md`**
  - Input: Absolute or relative path to a .md file in `raw_md/`.
  - Output: Full text content of the file.
  - Security: Ensure the path is within the project directory.

- **Tool 2: `store_lumina_chunk`**
  - Logic: Save the content into `data_chunks/{axis}/{timestamp}_{slug}.md`.
  - Metadata: Prepend the chunk with YAML frontmatter containing tags and source_url.
  - Format: 
    ```markdown
    ---
    axis: [axis_name]
    tags: [tag1, tag2]
    source: [url]
    ---
    [content]
    ```

## Deliverables
- Updated `vanya_mcp.py` with registered tools.
- A report detailing the changes.