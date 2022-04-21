from machine import Pin, I2C, PWM
from time import sleep_ms
import ssd1306
import _thread

class OledDiaplay:

  def log(self, message, x, y, col=1):
    self.oled.text(message, x, y, col)
    self.oled.show()

  def logLoading(self, yPosition = 10):
    while True:
      loading_count = 0
      for loading_count in range(11):
        sleep_ms(200)
        output_log = '{0}{1}'.format('.' * loading_count, (11-loading_count) * ' ')
        self.oled.text(output_log, 0, yPosition)
        self.oled.show()
      self.oled.text('{0}'.format(11 * '.'), 0, yPosition, 0)
      self.oled.show()

  def startLoading(self, yPosition):
    self.loading_thread = _thread.start_new_thread(self.logLoading, (yPosition,))
    # self.logLoading(yPosition)

  def clear(self):
    if self.loading_thread is not None:
      self.loading_thread.exit()
      self.loading_thread = None
    self.oled.clear()

  def __init__(self):
    # ESP32 Pin assignment 
    self.i2c = I2C(0, scl=Pin(22), sda=Pin(21))
    self.oled_width = 128
    self.oled_height = 64
    self.oled = ssd1306.SSD1306_I2C(self.oled_width, self.oled_height, self.i2c)
    self.loading_thread = None

