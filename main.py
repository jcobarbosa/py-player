import network, os
import socket
from time import sleep_ms

from oled import *
from database import *
# from sdcardUtil import *
from networkUtil import *
from webserver import *

oledDisplay = OledDiaplay()
oledDisplay.clear()
oledDisplay.log('Iniciando...', 0, 10)
oledDisplay.startLoading(20)

# # sdCardUtil = SDCardUtil()

database = Db()
oledDisplay.clear()
oledDisplay.log('Db iniciado!', 0, 5)
oledDisplay.startLoading(20)
# audioList = database.getAudios('1')

networkUtil = NetworkUtil(oledDisplay, database)

WebServer(networkUtil, oledDisplay)
oledDisplay.clear()
oledDisplay.log('Webserver iniciado!', 0, 25)

# for audio in audioList:
#   oledDisplay.clear()
#   oledDisplay.log('Audio:', 0, 10)
#   oledDisplay.log(str(audio['name']), 0, 20)
#   sleep_ms(3000)

# oledDisplay.clear()