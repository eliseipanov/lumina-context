# Sprint 1.5.5: Vision Worker Observability & Debugging

Add verbose logging and debug exports to track performance through the tunnel and LVM processing.

## Tasks:
1. **Console Progress Logging**:
   - Add timestamps to all console outputs.
   - Print status before and after: loading prompt, encoding image, and sending API request.
   - Add a "Waiting for Ollama..." message immediately after the request is sent.

2. **Debug Artifacts**:
   - Implement a `DEBUG_MODE` check (load from .env).
   - If `DEBUG_MODE=True`, save the raw string response from Ollama to `data/logs/last_raw_response.json` before any regex cleaning. This is critical for fixing parsing errors.

3. **Error Reporting**:
   - Wrap `json.loads` in a try-except block that prints the first 200 characters of the failed string if parsing fails.

4. **Performance Tracking**:
   - Measure and print the duration (in seconds) of the `analyze_image` call.

## Goal:
Full transparency of the data flow. No more "silent hangs" during tunnel communication.