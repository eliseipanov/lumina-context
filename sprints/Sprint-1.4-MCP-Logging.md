# Sprint 1.4: MCP Logging & "Glass Box" Implementation

## Context
Kwen 72b (Msty) reports tool success, but no execution is visible. We need to verify if the LLM is hallucinating tool calls or if the MCP server is failing silently.

## Objectives
1. **Centralized Logging**: Redirect all internal logs to `/var/www/chanker_vanya/vanya_mcp.log`.
2. **Call Tracing**: Log every `handle_call_tool` request with its raw arguments.
3. **Error Capture**: Implement global try-except in `handle_call_tool` to log full stack traces.

## Task List
1. **Initialize Logging**: Configure `logging` in `vanya_mcp.py` to write to the log file.
2. **Instrument Tools**:
   - Log at the entry of `handle_call_tool`.
   - Log `trafilatura` results in `process_url`.
   - Log file path and YAML size in `store_lumina_chunk`.
3. **System Access**: Ensure the script has permissions to write to the log on the VPS.

## Definition of Done
- `vanya_mcp.log` is created and tracks every tool interaction.
- Errors are logged with stack traces instead of silent exits.