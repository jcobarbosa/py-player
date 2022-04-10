from http.server import BaseHTTPRequestHandler
from classes.db import Database
import time, json, vlc
from urllib.parse import urlparse, parse_qs

from pprint import pprint


database = Database()

class Api(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
            self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
            # vlc_instance = vlc.Instance()
            # player = vlc_instance.media_player_new()
            # media = vlc_instance.media_new("/mnt/d/jcobarbosa/Downloads/fogos.mp3")
            # player.set_media(media)
            # player.play()
        if self.path == "/assets":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Accept", "application/json")
            self.end_headers()
                # print(str(file))
            self.wfile.write(bytes(database.getFiles(), "utf-8"))
            # [f for f in db.search(Query()) if isfile(self.wfile.write(bytes(str(f) + "<br>", "utf-8")))]
    def do_POST(self):
        if self.path == "/schedule":
            content_len = int(self.headers.get("Content-Length"))
            body = self.rfile.read(content_len)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(database.addSchedule(body), "utf-8"))
    def do_DELETE(self):
        urlParse = urlparse(self.path)
        if urlParse.path == "/schedule/remove" or urlParse.path == "/schedule/remove/":
            parameters = parse_qs(urlParse.query)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(database.removeSchedule(parameters), "utf-8"))