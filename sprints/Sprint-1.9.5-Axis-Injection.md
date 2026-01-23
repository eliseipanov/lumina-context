# Sprint 1.9.5: Axis Data Injection

## Tasks
1. **Engine**: Add `jinja2` to `requirements.txt`.
2. **Vocab Parser**: 
   - Get `LUMINA_ACTIVE_AXES` from `.env`.
   - Read each file: `data/vocab/lumina_{axis}.md`.
   - Extract the "Definition" and "Core Tags" sections.
3. **Assembler Logic**:
   - Update `prompt_assembler.py` to use `Jinja2`.
   - Instead of just reading `schemas/prompts/lumina_base_v1.tpl`, RENDER it.
   - Pass the list of axis data into the template.
4. **Validation**: 
   - Check `logs/last_prompt.md`. It must contain the ACTUAL text from vocab files, not `{{ }}`.