# Combined Sprint: Schema Fix & Process Management

## Part 1: Input Schema Fix (v1.2.1)
- **Problem**: Llama 3.2 fails with "is not of type 'string'".
- **Task**: Simplify `inputSchema` in `handle_list_tools` for `process_url`.
- **Structure**: It must explicitly expect `url` as a string. Remove any redundant object descriptions that confuse the model.
- **Extraction**: Ensure `handle_call_tool` extracts `url` correctly from the arguments dict.

## Part 2: Process Control (v1.2.2)
- **Problem**: Accumulated ghost processes on VPS.
- **Task**: 
  - Implement a check for `stdin`. If the input stream closes (client disconnects), the server must `sys.exit(0)` immediately.
  - Add basic signal handling (SIGTERM) to ensure clean shutdown.
  - (Optional) Create/clean a `.vanya.pid` file on startup/exit for tracking.

## Goal
A stable MCP server that correctly accepts URLs from Llama 3.2 and doesn't leave zombie processes behind.