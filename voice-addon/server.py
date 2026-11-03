"""Home Assistant ingress-only broker for short-lived OpenAI Realtime client secrets."""
import json
from pathlib import Path
import os
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

API_URL = "https://api.openai.com/v1/realtime/client_secrets"
MODEL = "gpt-realtime"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.split("?", 1)[0] in ("/", "/index.html"):
            page = Path("/app/index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(page)))
            self.end_headers()
            self.wfile.write(page)
            return
        if self.path != "/health":
            self.send_error(404)
            return
        self.reply(200, {"status": "ok", "key_configured": bool(os.getenv("OPENAI_API_KEY"))})

    def do_POST(self):
        if self.path != "/session":
            self.send_error(404)
            return
        # Ingress authenticates the caller before forwarding to this internal service.
        key = os.getenv("OPENAI_API_KEY", "")
        if not key:
            self.reply(503, {"error": "Configure the API key in add-on options"})
            return
        payload = {"session": {
            "type": "realtime",
            "model": MODEL,
            "instructions": "You are Perfecto, a friendly concise home voice assistant. Answer general questions. You cannot yet control home devices. Never claim to have changed devices.",
            "audio": {"output": {"voice": "marin"}}
        }}
        request = urllib.request.Request(API_URL,
            data=json.dumps(payload).encode(),
            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
            method="POST")
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                result = json.load(response)
            # Never return the long-lived API key.
            self.reply(200, result)
        except urllib.error.HTTPError as error:
            self.reply(502, {"error": "OpenAI session request failed", "status": error.code})
        except Exception:
            self.reply(502, {"error": "Unable to create voice session"})

    def reply(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass  # Avoid logging ephemeral tokens.

ThreadingHTTPServer(("0.0.0.0", 8099), Handler).serve_forever()
