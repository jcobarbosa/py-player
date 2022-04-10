import time

class Player():
    def init(self):
        while True:
            timeSeconds = time.localtime().tm_sec
            if timeSeconds == 0:
                # verificar se tem nova playlist e suas regras
                print("segundo 0 do minuto" + str(time.localtime().tm_min))
            time.sleep(1)
