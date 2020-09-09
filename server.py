"""TODO"""

import storage

import http.server
import json
import urllib.parse


def debug(*args, **kwargs):
    return print(*args, **kwargs)


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        debug('requestline:', self.requestline)
        debug('path:', self.path)

        # Route some special endpoints. Otherwise forward to the file-serving
        # implementation.
        if self.path == '/launch':
            return self.handle_GET_launch()
        # TODO: more handlers

        return super().do_GET()

    def do_POST(self):
        debug('requestline:', self.requestline)
        debug('path:', self.path)

        # /foo/bar/baz -> foo
        toplevel = self.path[1:].split('/')[0]

        # Each supported endpoint has a handler method on this object.
        method_name = f'handle_POST_{toplevel}'
        return getattr(self, method_name)()

    def handle_POST_launch(self):
        content_length = int(self.headers.get('Content-Length', 0))

        input_payload = self.rfile.read(content_length)
        debug('raw payload:', input_payload)
        parsed_input = urllib.parse.parse_qs(input_payload.decode('utf8'))
        debug('parsed payload:', parsed_input)

        storage.update_popup_settings(parsed_input)
        self.send_popup_settings()

    def handle_GET_launch(self):
        self.send_popup_settings()

    def send_popup_settings(self):
        output_dict = storage.select_popup_settings()
        output_payload = json.dumps(output_dict).encode('utf8')

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
