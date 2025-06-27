from http.server import SimpleHTTPRequestHandler, HTTPServer
import socketserver
import sys
import urllib

class CustomHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def guess_type(self, path):
        path = urllib.parse.urlparse(path).path
        print(f'path')
        if path.endswith('.js'):
            return 'application/javascript'
        if path.endswith('.wasm'):
            return 'application/wasm'
        
        return super().guess_type(path)

def run(server_class=HTTPServer, handler_class=CustomHandler, port=8000):
    handler = SimpleHTTPRequestHandler
    handler.extensions_map={
    '.manifest': 'text/cache-manifest',
	'.html': 'text/html',
        'png': 'image/png',
	'.jpg': 'image/jpg',
	'.svg':	'image/svg+xml',
	'.css':	'text/css',
	'.js':	'application/x-javascript',
	'': 'application/octet-stream', # Default
    }

    server_address = ('', port)
    httpd = socketserver.TCPServer(("127.0.0.1",8000), handler)
    print(f'Serving on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    port = 8000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    run(port=port)
