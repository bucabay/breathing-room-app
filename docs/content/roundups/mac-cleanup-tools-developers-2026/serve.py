"""Read-only isolated draft fixture; only this preview and its two assets."""
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import mimetypes

owned = Path(__file__).resolve().parent
prefix = '/assets/roundups/mac-cleanup-tools-developers-2026/'
assets = Path('/Users/gabe/code/breathing-room/website/public')

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            file = owned / 'preview.html'
        elif self.path in (prefix + 'owner-before-size.svg', prefix + 'breathing-room-space-preview.png'):
            file = assets / self.path.lstrip('/')
        else:
            self.send_error(404)
            return
        data = file.read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', mimetypes.guess_type(file)[0] or 'application/octet-stream')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

server = HTTPServer(('127.0.0.1', 0), Handler)
print(f'http://127.0.0.1:{server.server_port}/', flush=True)
server.serve_forever()
