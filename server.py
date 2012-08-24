#!/usr/bin/env python
import http.server
import re

class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_file("static/index.html")
        elif re.match("^/static/", self.path):
            relative_path = self.path[1:]
            self.send_file(relative_path)
        else:
            self.send_not_found_response()
        # self.send_response(200)
        # self.wfile.write(b"abc\n")

    def send_file(self, filename):
        try:
            with open(filename, "rb") as f:
                self.send_response(200)
                #self.send_header("Content-Type", "text/html;charset=utf-8")
                self.send_header("Connection", "close")
                self.end_headers()

                file_contents = f.read()
                self.wfile.write(file_contents)
        except IOError:
            self.send_not_found_response()

    def send_not_found_response(self):
        self.send_error(404)

def run(server_class=http.server.HTTPServer, handler_class=http.server.BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print("Server started...")
    httpd.serve_forever()

run(handler_class=HTTPRequestHandler)
