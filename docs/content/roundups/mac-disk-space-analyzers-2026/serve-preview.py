"""Read-only isolated review fixture; never exposes private repository paths."""
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

OWNED = Path(__file__).parent
ASSETS = Path('/Users/gabe/code/breathing-room/website/public/assets/roundups/mac-disk-space-analyzers-2026')
ALLOWED = {
    '/': (OWNED / 'preview.html', 'text/html; charset=utf-8'),
    '/assets/roundups/mac-disk-space-analyzers-2026/inspect-before-remove.svg': (ASSETS / 'inspect-before-remove.svg', 'image/svg+xml'),
    '/assets/roundups/mac-disk-space-analyzers-2026/breathing-room-space-preview.png': (ASSETS / 'breathing-room-space-preview.png', 'image/png'),
}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        entry = ALLOWED.get(self.path)
        if entry is None:
            self.send_error(404)
            return
        data = entry[0].read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', entry[1])
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(data)

server = HTTPServer(('127.0.0.1', 0), Handler)
print(f'http://127.0.0.1:{server.server_port}/', flush=True)
server.serve_forever()
