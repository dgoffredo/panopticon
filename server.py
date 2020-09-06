"""TODO"""

import storage

import http.server
import json
import urllib.parse


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        print('requestline:', self.requestline)
        print('path:', self.path)

        # /foo/bar/baz -> foo
        toplevel = self.path[1:].split('/')[0]

        # Each supported endpoint has a handler method on this object.
        method_name = f'handle_POST_{toplevel}'
        return getattr(self, method_name)()

    def handle_POST_launch(self):
        content_length = int(self.headers.get('Content-Length', 0))

        input_payload = self.rfile.read(content_length)
        print('raw payload:', input_payload)
        parsed_input = urllib.parse.parse_qs(input_payload.decode('utf8'))
        print('parsed payload:', parsed_input)

        # TODO: Save the settings, pick defaults for missing settings, return the settings.
        output_payload = json.dumps(parsed_input).encode('utf8') # TODO

        self.send_response(200)
        self.send_header('Content-Type', 'application/JSON')
        self.send_header('Content-Length', len(output_payload))
        self.end_headers()
        self.wfile.write(output_payload)


class ReusableHTTPServer(http.server.HTTPServer):
    # prevent "address in use" error after restarting server
    allow_reuse_address = True

    def __init__(self, host, port):
        super().__init__((host, port), RequestHandler)

    def end_headers(self):
        self.send_nocache_headers()
        super().end_headers()

    def send_nocache_headers(self):
        """Ask the browser not to cache anything. This makes development
        iterations easier. Sometimes even Ctrl+F5 still caches something.
        """
        self.send_header("Cache-Control",
                         "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
