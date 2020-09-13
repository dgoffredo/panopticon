"""Serve the Panopticon website."""

import server
import json
from pathlib import Path
import random


def cat():
    cats_path = Path(__file__).parent.absolute() / 'cats.json'
    with cats_path.open() as file:
        cats = json.load(file)

    return random.choice(cats)


# Wikipedia says that port 4000 is for Diablo 2, so we can probably use it.
ip, port = '127.0.0.1', 4000
httpd = server.ReusableHTTPServer(ip, port)
url = f'http://{ip}:{port}/'
print(cat())
print()
print(url)

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass # Ctrl+C (SIGTERM) is fine, don't consider it an error
