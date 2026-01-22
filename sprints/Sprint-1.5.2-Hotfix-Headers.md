# Sprint 1.5.2: Hotfix - Malformed HTTP Headers

Fix the regression in `process_url` caused by malformed User-Agent strings in the configuration layer.

## Tasks:
1. **Clean Environment Variables**:
   - Check `.env` for any leading/trailing whitespaces in `UA_LIST` or `USER_AGENT`.
2. **Sanitize Configuration (config.py)**:
   - Apply `.strip()` to all string variables loaded from `.env`, specifically headers and proxy URLs.
   - Example: `USER_AGENT = os.getenv("USER_AGENT").strip()`
3. **Validation**:
   - Ensure `vanya_mcp.py` correctly passes these cleaned headers to the request client (httpx/requests).

## Goal:
Restore `process_url` functionality (but don't try to test it) and eliminate the "Invalid leading whitespace" error.