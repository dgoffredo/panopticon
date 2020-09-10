"""TODO"""

import storage

import http.server
import json
import urllib.parse


def debug(*args, **kwargs):
    return print(*args, **kwargs)


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        return self.do_handler('GET')

    def do_POST(self):
        return self.do_handler('POST')

    def do_handler(self, http_method):
        """Call self.do_<method>_<path root>()"""
        http_method = http_method.upper()

        debug('requestline:', self.requestline)
        debug('path:', self.path)
        debug('http_method:', http_method)

        # /foo/bar/baz -> foo
        toplevel = self.path[1:].split('/')[0]

        # Each supported endpoint has a handler method on this object.
        method_name = f'handle_{http_method}_{toplevel}'
        debug('method_name:', method_name)
        if hasattr(self, method_name):
            return getattr(self, method_name)()
        else:
            # e.g. super().do_GET() or super().do_POST()
            debug(f'falling back to calling do_{http_method} on {super()}')
            # Nope, this calls the method on _this_ class, for some reason.
            # return getattr(super(), f'do_{http_method.upper()}')
            if http_method == 'GET':
                return super().do_GET()
            else:
                assert http_method == 'POST'
                return super().do_POST()

    def handle_POST_launch(self):
        content_length = int(self.headers.get('Content-Length', 0))
        input_payload = self.rfile.read(content_length)
        debug('raw payload:', input_payload)
        parsed_input = urllib.parse.parse_qs(input_payload.decode('utf8'))
        debug('parsed payload:', parsed_input)

        # 1. Save the popup settings (width, height, etc.)
        # 2. Insert a "launchPopup" event.
        # 3. Fetch the popup settings (that we just saved) and return them to
        #    the client.
        storage.update_popup_settings(parsed_input)
        storage.insert_event(type_name='launchPopup', activity_name='none')
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

    def handle_POST_activity(self):
        content_length = int(self.headers.get('Content-Length', 0))
        input_payload = self.rfile.read(content_length)
        debug('raw payload:', input_payload)
        parsed_input = json.loads(input_payload.decode('utf8'))
        debug('parsed payload:', parsed_input)
        storage.insert_event(type_name='setActivity', activity_name=parsed_input)

        self.send_response(200)
        self.end_headers()

    def handle_POST_close(self):
        storage.insert_event(type_name='closePopup', activity_name='none')

        self.send_response(200)
        self.end_headers()


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
