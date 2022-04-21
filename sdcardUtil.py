import os
from machine import Pin, SoftSPI
from sdcard import SDCard
# import machine, sdcard, os


class SDCardUtil():
  def __init__(self):
    spisd = SoftSPI(-1, miso=Pin(19), mosi=Pin(23), sck=Pin(18))
    sd = SDCard(spisd, Pin(5))
    os.mount(sd, '/sd')
    os.listdir('/')
    # spisd = SoftSPI(-1, miso=Pin(19), mosi=Pin(23), sck=Pin(18))
    # sd = SDCard(spisd, Pin(15))
    # print('Root directory:{}'.format(os.listdir()))
    # vfs = os.VfsFat(sd)
    # os.mount(vfs, '/sd1')
    # print('Root directory:{}'.format(os.listdir()))
    # os.chdir('sd1')
    # print('SD Card contains:{}'.format(os.listdir()))
