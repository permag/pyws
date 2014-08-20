#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import sys

PORT_NUMBER = 8000
WWW_PATH = '/www/'

class WSHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path = 'index.html'

        try:
            send_reply = True
            if self.path.endswith('.html') or self.path.endswith('.htm'):
                mime_type = 'text/html'
            elif self.path.endswith('.jpg'):
                mime_type = 'image/jpg'
            elif self.path.endswith('.png'):
                mime_type = 'image/png'
            elif self.path.endswith('.gif'):
                mime_type = 'image/gif'
            elif self.path.endswith('.js'):
                mime_type = 'application/javascript'
            elif self.path.endswith('.css'):
                mime_type = 'text/css'
            else:
                send_reply = False

            if send_reply:
                with open(curdir + sep + WWW_PATH + self.path) as f:
                    self.send_response(200)
                    self.send_header('Content-type', mime_type)
                    self.end_headers()
                    self.wfile.write(f.read())

        except IOError:
            self.send_error(404, 'File Not Found: {}'.format(self.path))


def main():
    if len(sys.argv) > 1:
        port_number = int(sys.argv[1])
    else:
        port_number = PORT_NUMBER

    try:
        server = HTTPServer(('', port_number), WSHandler)
        print('Web Server started on port {}'.format(port_number))
        print('Browse to: http://127.0.0.1:{}'.format(port_number))
        server.serve_forever()

    except KeyboardInterrupt:
        print('\nUser closed connection. Server is shutting down.')
        server.socket.close()


if __name__ == '__main__':
    main()
