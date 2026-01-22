# Sprint 1.5.6: Vision Worker Streaming & Persistence

Upgrade `vision_worker.py` to use streaming responses to prevent tunnel timeouts and handle long LVM processing times.

## Tasks:
1. **Streaming Implementation**:
   - Update `analyze_image` payload: set `"stream": true`.
   - Modify the request handling to iterate over the response lines (`response.iter_lines()`).
   - Accumulate the `response` field from each JSON chunk received from Ollama.

2. **Visual Heartbeat**:
   - Print a visual indicator (e.g., a dot `.` or a "token count") in the console every time a chunk of data is received. This keeps the tunnel active and informs the user of progress.

3. **Robust Aggregation**:
   - Once the stream ends (the last chunk with `done=true`), pass the full accumulated string to the existing regex cleaner and JSON parser.

4. **Timeout Logic Adjustment**:
   - Keep the `timeout` high, but understand that with streaming, the "Read timeout" will only trigger if *no data at all* is received for 180s, which is much safer.

## Goal:
Ensure the analysis completes even if the model takes 5+ minutes to generate the full breakdown.