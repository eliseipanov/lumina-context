# Sprint 1.9.1: Lumina Dynamic Prompt Assembler

## Context
Currently, `vision_worker.py` loads a static Markdown file as a prompt. To prevent LVM context overflow and ensure architectural purity, we need to transition to a dynamic assembly system based on `.tpl` templates and atomic `.md` vocabulary files.

## Objectives
1. Implement a `PromptAssembler` class to handle template rendering.
2. Integrate the assembler into the `vision_worker.py` workflow.
3. Maintain backward compatibility (fallback to static prompt if assembly fails).

## Technical Tasks

1. **New Module: `prompt_assembler.py`**
   - Create a class that loads the template from `LUMINA_TEMPLATE` defined in `.env`.
   - Implement `_get_axis_data(axis_name)`: 
     - Read `data/vocab/lumina_{axis_name}.md`.
     - Extract the **Definition** (content of the first blockquote `>`).
     - Extract **Core Tags** (all bullet points `- tag`).
   - Implement `render_system_prompt(active_axes_list)`:
     - Load `data/roles/architect_v1.md` as `ROLE_DESCRIPTION`.
     - Load `schemas/system_schema.json` as `SYSTEM_SCHEMA_JSON`.
     - Map the `active_axes_list` into a list of dictionaries for the template's `ACTIVE_AXES` loop.
     - Return the final string.

2. **Configuration Update (`config.py`)**
   - Add `LUMINA_TEMPLATE` (default: `lumina_base_v1.tpl`).
   - Add `LUMINA_ROLE` (default: `architect_v1.md`).
   - Add `LUMINA_ACTIVE_AXES` as a list (parsed from a comma-separated string in `.env`).

3. **Worker Integration (`vision_worker.py`)**
   - Refactor `load_prompt()`:
     - Instead of just reading a file, initialize `PromptAssembler`.
     - Call `render_system_prompt(config.LUMINA_ACTIVE_AXES)`.
     - If any error occurs during assembly, log a warning and fall back to the old `CURRENT_PROMPT_PATH` logic.

4. **Validation**
   - Ensure the assembled prompt is logged if `DEBUG_MODE=true` to verify correct "injection" of definitions and schema.

## Definition of Done
- `vision_worker.py` starts and generates a system prompt dynamically using the `.tpl` file.
- The model receives definitions only for axes specified in `LUMINA_ACTIVE_AXES`.