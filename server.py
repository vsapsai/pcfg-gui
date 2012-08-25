#!/usr/bin/env python
import http.server
import cgi, urllib.parse
import json
import re

class HTTPStatusCode:
    SUCCESS = 200
    NOT_IMPLEMENTED_ERROR = 501

class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_file("static/index.html")
        elif re.match("^/static/", self.path):
            relative_file_path = urllib.parse.unquote(self.path)[1:]
            self.send_file(relative_file_path)
        else:
            self.send_not_found_response()

    def do_POST(self):
        if self.path == "/app/items":
            obj = self.JSON_from_request()
            if obj is None:
                self.send_error(HTTPStatusCode.NOT_IMPLEMENTED_ERROR)
                return

            if "content" in obj:
                obj["length"] = len(obj["content"])
                del obj["content"]
            obj["id"] = 1

            self.send_response(201)
            self.send_header("Location", "/app/items/1")
            self.send_header("Content-Type", "application/json")
            self.send_header("Connection", "close")
            self.end_headers()

            self.wfile.write(json.dumps(obj).encode())
        else:
            self.send_error(HTTPStatusCode.NOT_IMPLEMENTED_ERROR)

    def do_PUT(self):
        if re.match("^/app/items/", self.path):
            obj = self.JSON_from_request()
            if obj is None:
                self.send_error(HTTPStatusCode.NOT_IMPLEMENTED_ERROR)
                return

            if "content" in obj:
                obj["length"] = len(obj["content"])
                del obj["content"]

            self.send_response(HTTPStatusCode.SUCCESS)
            self.send_header("Content-Type", "application/json")
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(json.dumps(obj).encode())
        else:
            self.send_error(HTTPStatusCode.NOT_IMPLEMENTED_ERROR)

    def rfile_content(self):
        """"Reads from rfile Content-Length bytes.

        There is a catch if you read too much, connection won't be closed.
        That's why need to read exactly Content-Length bytes."""
        length = self.headers["Content-Length"]
        if length is None:
            return None
        length = int(length)
        content = self.rfile.read(length)
        return content

    def JSON_from_request(self):
        "Tries to interpret rfile as JSON and returns deserialized JSON."
        content_type = self.headers.get_content_type()
        if content_type != "application/json":
            return None
        content = self.rfile_content()
        content = str(content, "utf-8")
        obj = json.loads(content)
        return obj

    def send_file(self, filename):
        try:
            with open(filename, "rb") as f:
                self.send_response(HTTPStatusCode.SUCCESS)
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
