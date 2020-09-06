"""TODO"""

import server
import webbrowser


# Wikipedia says that port 4000 is for Diablo 2, so we can probably use it.
ip, port = '127.0.0.1', 4000
httpd = server.ReusableHTTPServer(ip, port)
url = f'http://{ip}:{port}/'
print(url)
# webbrowser.open(url)

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass # Ctrl+C (SIGTERM) is fine, don't consider it an error
