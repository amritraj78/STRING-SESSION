import os
import time
import logging
import threading
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler

# Ensure asyncio event loop exists on Python 3.12+ before importing pyrogram
try:
    asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

import config

# Initialize kurimod (or pyromod) monkeypatches
try:
    import kurimod  # type: ignore # noqa: F401
except ImportError:
    try:
        from pyromod import listen  # type: ignore # noqa: F401
    except ImportError:
        pass

from pyrogram import Client, idle
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


# Koyeb / Cloud HTTP Health Check Server
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"String Session Bot is running and healthy!\n")

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()

    def log_message(self, format, *args):
        # Silence access logs so bot logs stay clean
        return


def start_health_check_server():
    port = int(os.environ.get("PORT", config.PORT or 8000))
    try:
        server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        logging.info(f"Health check server started on port {port} for Koyeb/cloud deployment.")
    except Exception as e:
        logging.warning(f"Could not bind health check server on port {port}: {e}")


StartTime = time.time()
app = Client(
    "Anonymous",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    in_memory=True,
    plugins=dict(root="StringGenBot"),
)


if __name__ == "__main__":
    start_health_check_server()
    if not config.API_ID or not config.API_HASH or not config.BOT_TOKEN:
        print("\n❌ [ERROR] Missing Telegram Credentials!")
        print("Please configure your .env file or environment variables with:")
        print("  API_ID=your_api_id")
        print("  API_HASH=your_api_hash")
        print("  BOT_TOKEN=your_bot_token")
        print("  OWNER_ID=your_owner_id\n")
        exit(1)

    print("𝐒𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐘𝐨𝐮𝐫 𝐒𝐭𝐫𝐢𝐧𝐠 𝐁𝐨𝐭...")
    try:
        app.start()
    except (ApiIdInvalid, ApiIdPublishedFlood):
        raise Exception("Your API_ID/API_HASH is not valid.")
    except AccessTokenInvalid:
        raise Exception("Your BOT_TOKEN is not valid.")
    uname = app.get_me().username
    print(f"@{uname} 𝐒𝐓𝐀𝐑𝐓𝐄𝐃 𝐒𝐔𝐂𝐄𝐒𝐒𝐅𝐔𝐋𝐋𝐘. 𝐌𝐀𝐃𝐄 𝐁𝐘 @𝐥𝐥_𝐁𝐑𝐀𝐍𝐃𝐄𝐃_𝐥𝐥 🤗")
    idle()
    app.stop()
    print("𝗕𝗢𝗧 𝗦𝗧𝗢𝗣𝗣𝗘𝗗 𝗕𝗬 𝗕𝗬 !")
