import asyncio
import trafilatura
import requests
import random
import os
import re
import sys
import signal
import atexit
import logging
import traceback
from datetime import datetime
import old_files.config_old as config_old
from mcp.server.stdio import stdio_server
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.lowlevel.server import NotificationOptions
import mcp.types as types

# Configure logging
logging.basicConfig(
    filename='/var/www/chanker_vanya/vanya_mcp.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Ініціалізація сервера
server = Server("vanya-chunker")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """Реєструємо інструменти"""
    return [
        types.Tool(
            name="vanya_hallo",
            description="Перевірка зв'язку",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        types.Tool(
            name="process_url",
            description="Extract main content from URL, convert to Markdown, save to file, and return stats",
            inputSchema={
                "type": "object",
                "properties": {"url": {"type": "string"}},
                "required": ["url"]
            }
        ),
        types.Tool(
            name="read_processed_md",
            description="Read the content of a processed Markdown file from raw_md directory",
            inputSchema={
                "type": "object",
                "properties": {"filepath": {"type": "string"}},
                "required": ["filepath"]
            }
        ),
        types.Tool(
            name="store_lumina_chunk",
            description="Store a Lumina axis chunk with metadata",
            inputSchema={
                "type": "object",
                "properties": {
                    "axis": {"type": "string"},
                    "content": {"type": "string"},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "source_url": {"type": "string"}
                },
                "required": ["axis", "content", "tags", "source_url"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    try:
        logging.info(f"Tool called: {name}, args: {arguments}")
        
        if name == "vanya_hallo":
            return [types.TextContent(type="text", text="Hallo from Vanya!")]
            
        elif name == "process_url":
            url = arguments.get("url") if arguments else None
            if not url or not isinstance(url, str):
                return [types.TextContent(type="text", text="Error: URL must be a valid string")]
            try:
                response = requests.get(url, headers={'User-Agent': random.choice(config_old.UA_LIST)},
                                        proxies=config_old.PROXIES, timeout=20)
                response.raise_for_status()
                html_raw = response.text

                md_content = trafilatura.extract(html_raw, include_formatting=True, output_format='markdown')
                logging.info(f"Extracted MD length: {len(md_content) if md_content else 0} for {url}")
                
                if not md_content:
                    return [types.TextContent(type="text", text="Error: Failed to extract content")]

                word_count = len(md_content.split())
                token_count = int(word_count * 1.3)

                slug = re.sub(r'[^\w\-_\.]', '_', url.split('/')[-1] or "index")
                filename = f"{slug}_{datetime.now().strftime('%H%M%S')}.md"
                filepath = os.path.join("/var/www/chanker_vanya/raw_md", filename)

                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(md_content)

                summary = f"Processed {url}\nFilepath: {filepath}\nWord count: {word_count}\nStatus: Success"
                return [types.TextContent(type="text", text=summary)]
            except Exception as e:
                logging.error(f"process_url error: {str(e)}")
                return [types.TextContent(type="text", text=f"Error processing URL: {str(e)}")]

        elif name == "read_processed_md":
            filepath = arguments.get("filepath") if arguments else None
            if not filepath or not isinstance(filepath, str):
                return [types.TextContent(type="text", text="Error: filepath must be a valid string")]
            
            abs_path = os.path.abspath(filepath)
            allowed_dir = "/var/www/chanker_vanya/raw_md"
            if not abs_path.startswith(allowed_dir):
                return [types.TextContent(type="text", text="Error: Access denied")]
            
            if not os.path.exists(abs_path):
                return [types.TextContent(type="text", text="Error: File not found")]
            
            try:
                with open(abs_path, "r", encoding="utf-8") as f:
                    content = f.read()
                return [types.TextContent(type="text", text=content)]
            except Exception as e:
                return [types.TextContent(type="text", text=f"Error reading file: {str(e)}")]

        elif name == "store_lumina_chunk":
            axis = arguments.get("axis")
            content = arguments.get("content")
            tags = arguments.get("tags")
            source_url = arguments.get("source_url")
            
            if not all(isinstance(x, str) for x in [axis, content, source_url]) or not isinstance(tags, list):
                return [types.TextContent(type="text", text="Error: Invalid arguments")]
                
            try:
                base_dir = "/var/www/chanker_vanya/data_chunks"
                axis_dir = os.path.join(base_dir, axis)
                os.makedirs(axis_dir, exist_ok=True)
                
                slug = re.sub(r'[^\w\-_\.]', '_', source_url.split('/')[-1] or "chunk")
                filename = f"{datetime.now().strftime('%H%M%S')}_{slug}.md"
                filepath = os.path.join(axis_dir, filename)
                
                yaml_front = f"---\naxis: {axis}\ntags: {tags}\nsource: {source_url}\n---\n\n"
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(yaml_front + content)
                
                logging.info(f"Stored chunk: {filepath}")
                return [types.TextContent(type="text", text=f"Stored chunk in {filepath}")]
            except Exception as e:
                logging.error(f"store_lumina_chunk error: {str(e)}")
                return [types.TextContent(type="text", text=f"Error storing chunk: {str(e)}")]

        else:
            logging.warning(f"Unknown tool requested: {name}")
            return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        logging.error(f"Critical error in tool {name}: {str(e)}\n{traceback.format_exc()}")
        return [types.TextContent(type="text", text=f"Internal error: {str(e)}")]

async def monitor_stdin(read_stream):
    try:
        while True:
            if read_stream.at_eof():
                sys.exit(0)
            await asyncio.sleep(0.1)
    except:
        pass

async def main():
    # PID file
    pid_file = '.vanya.pid'
    with open(pid_file, 'w') as f:
        f.write(str(os.getpid()))
    atexit.register(lambda: os.remove(pid_file) if os.path.exists(pid_file) else None)

    # Signal handling
    signal.signal(signal.SIGTERM, lambda s, f: sys.exit(0))

    async with stdio_server() as (read_stream, write_stream):
        init_options = InitializationOptions(
            server_name="vanya-chunker",
            server_version="1.0.0",
            capabilities=server.get_capabilities(
                notification_options=NotificationOptions(),
                experimental_capabilities={}
            )
        )

        monitor_task = asyncio.create_task(monitor_stdin(read_stream))

        try:
            await server.run(
                read_stream,
                write_stream,
                init_options
            )
        finally:
            monitor_task.cancel()
            try:
                await monitor_task
            except asyncio.CancelledError:
                pass

if __name__ == "__main__":
    asyncio.run(main())