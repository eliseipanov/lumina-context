# Sprint v1.2: Markdown Extraction & Content Analysis

## Goal
Transform the server from a simple "hello world" into a content scout. The server must fetch a URL, convert the main content to Markdown, and provide data metrics for chunking strategy.

## Tasks
1. **Extraction**: Use `trafilatura` to fetch and extract the main content.
2. **Format**: Convert extracted content into clean Markdown (MD).
3. **Metrics Calculation**:
   - Calculate total Word count.
   - Estimate Token count (approx. words * 1.3 or use a basic tokenizer).
   - Identify key structural elements (headers, lists).
4. **New Tool**: `process_url(url: str)`
   - Returns: A summary containing:
     - Filename of the saved .md file.
     - Word count.
     - Estimated token count.
     - Status of the operation.
5. **Storage**: Save the full processed Markdown file into `/var/www/chanker_vanya/data/raw_md/`.

## Constraints
- Maintain the stable MCP initialization logic.
- NO arbitrary text splitting. Keep the full document structure in MD.
- Ensure `stdout` remains clean (JSON-RPC only).