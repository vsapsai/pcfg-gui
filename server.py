#!/usr/bin/env python
import http.server
import cgi, urllib.parse
import json
import re

class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_file("static/index.html")
        elif re.match("^/static/", self.path):
            relative_file_path = urllib.parse.unquote(self.path)[1:]
            self.send_file(relative_file_path)
        else:
            self.send_not_found_response()
        # self.send_response(200)
        # self.wfile.write(b"abc\n")

    def do_POST(self):
        if self.path == "/app/items":
            content_type = self.headers.get_content_type()
            if content_type != "application/json":
                self.send_error(415) # Unsupported Media Type
                return

            content = self.rfile_content()
            content = str(content, "utf-8")
            obj = json.loads(content)
            print(obj)

            self.send_response(201)
            self.send_header("Location", "/app/items/1")
            self.send_header("Connection", "close")
            self.end_headers()
        else:
            self.send_error(501)

    def rfile_content(self):
        length = self.headers["Content-Length"]
        if length is None:
            return None
        length = int(length)
        content = self.rfile.read(length)
        return content

    def send_file(self, filename):
        try:
            with open(filename, "rb") as f:
                self.send_response(200)
                #self.send_header("Content-Type", "text/html;charset=utf-8")
                #self.send_header("Connection", "close")
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
