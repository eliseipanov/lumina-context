# Project File Schema

This document outlines the file and directory structure of the Chanker Vanya project. It provides an overview of the organization, purpose, and contents of each directory and key files.

## Root Directory

- **.env.example**: Example environment variables file for configuration.
- **app.py**: Main application script (likely the entry point for the project).
- **config.py**: Configuration file containing project settings.
- **README.md**: Project documentation and overview.
- **requirements.txt**: Python dependencies list for the project.
- **vanya_mcp.py**: MCP (Model Context Protocol) related script, possibly for handling AI model interactions.

## data/

Directory containing data files and processed content.

### data/data_chunks/

Contains chunked data files, organized by categories.

- **ai-pose-prompts.json**: JSON file with AI pose prompts.
- **Compositional/**: Directory for compositional data chunks.
  - **232214_chunk.md**: Markdown chunk file.
- **Luminance/**: Directory for luminance-related data chunks.
  - **231927_chunk.md**: Markdown chunk file.
- **Material/**: Directory for material data chunks.
  - **232018_chunk.md**: Markdown chunk file.
- **Optical/**: Directory for optical data chunks.
  - **231844_chunk.md**: Markdown chunk file.
- **Psychographic/**: Directory for psychographic data chunks.
  - **232113_chunk.md**: Markdown chunk file.

### data/raw_md/

Raw markdown files and related data.

- **index_155023.md**: Indexed markdown file.
- **index_201819.md**: Indexed markdown file.
- **index_231209.md**: Indexed markdown file.
- **Lumina_Context.code-workspace**: VS Code workspace file for Lumina context.
- **orgazmy-u-zhenshhin-vidy-osobennosti-i-sekrety-dostizheniya-naslazhdeniya_150135.md**: Specific content markdown file (Russian title: "Orgasm in women: types, features, and secrets of achieving pleasure").
- **the-perfect-hard-light-set-up-for-studio-portraits_143016.md**: Tutorial or guide on hard light setup for portraits.

### data/raw_poses/

Directory for raw pose data (appears empty in the current structure).

### data/vocab/

Vocabulary and terminology files.

- **lumina_vocabulary.md**: Markdown file defining Lumina-related vocabulary.

## reports/

Sprint and project reports.

- **Report-for-Sprint-1.3-Lumina-Core.md**: Report for Sprint 1.3 focusing on Lumina Core.
- **Report-for-Sprint-1.4.9.md**: Report for Sprint 1.4.9.
- **Report-for-Sprint-1.4.md**: Report for Sprint 1.4.
- **Report-for-Sprint-v1.2.md**: Report for Sprint v1.2.

## schemas/

JSON schemas and prompt templates.

- **system_schema.json**: System-level JSON schema.
- **vision_passport_schema.json**: Schema for vision passport data.

### schemas/prompts/

Prompt templates for various models.

- **live_ref_v1_minicpm-v.md**: Prompt template for MiniCPM-V model.
- **live_ref_v1_moondream.md**: Prompt template for Moondream model.

## sprints/

Sprint documentation and planning files.

- **print-1.5-Vision-Worker-Atomic-Chunks.md**: Sprint documentation for version 1.5 (note: filename appears to have a typo, likely "Sprint-1.5").
- **Sprint-1.3-MCP-Lumina-Core.md**: Sprint 1.3 documentation for MCP Lumina Core.
- **Sprint-1.4-MCP-Logging.md**: Sprint 1.4 documentation for MCP Logging.
- **Sprint-v1.2-MD_Extraction_Stats.md**: Sprint v1.2 documentation on MD extraction stats.
- **Sprint-v1.2.1-v1.2.2-Fix_and_Cleanup.md**: Sprint v1.2.1 to v1.2.2 fix and cleanup documentation.

### sprints/sprints/

Nested directory for additional sprint files.

- **Sprint-1.4.9-Data-Centralization.md**: Sprint 1.4.9 documentation on data centralization.

## Notes

- This schema is based on the current file structure as of the latest update.
- File names and contents may change over time; refer to version control for historical changes.
- Some directories (e.g., `data/raw_poses/`) appear empty and may be placeholders for future content.
- The project appears to be related to AI, computer vision, and content processing, with a focus on "Lumina" components.