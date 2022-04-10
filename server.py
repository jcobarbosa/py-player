from classes.api import Api
from classes.player import Player
from http.server import HTTPServer
import threading

hostName = "localhost"
serverPort = 8080

player = None

def call_player():
    player = threading.Thread(target=Player().init(),args=(), daemon=True)
    player.start()

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), Api)
    print("Server started http://%s:%s" % (hostName, serverPort))
    call_player
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")