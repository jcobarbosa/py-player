import network, os
import socket
import time

global server_socket

retryCount = 0
maxRetry = 5

wifi_pa_ssid = 'encarte-01'
wifi_pa_password = '12345678'

class NetworkUtil:

  def __init__(self, oledDisplay, database):
    # self.addr = socket.getaddrinfo('0.0.0.0', 8080)[0][-1]
    self.wlan_sta = network.WLAN(network.STA_IF)
    self.wlan_ap = network.WLAN(network.AP_IF)

    self.database = database
    self.oledDisplay = oledDisplay

    self.connect()

  def listNearbyWifiNetworks(self):
    self.wlan_sta.active(True)
    availableNetworks = self.wlan_sta.scan()
    AUTHMODE = {0: "open", 1: "WEP", 2: "WPA-PSK", 3: "WPA2-PSK", 4: "WPA/WPA2-PSK"}
    networksList = ''
    for ssid, bssid, channel, rssi, authmode, hidden in sorted(availableNetworks, key=lambda x: x[3], reverse=True):
        networksList += '<tr><td><input type="radio" onclick="selecionarWifi();" name="ssid" value="{1}"></td><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>'.format(channel, ssid, rssi, AUTHMODE.get(authmode, '?'))

    return networksList

  def initWifiSta(self):
    retryCount = 0
    while not self.wlan_sta.active() and maxRetry > retryCount:
      self.wlan_sta.active(True)
      if not self.wlan_sta.active():
        print('Retentativa de ativação da interface: network.STA_IF')
        retryCount += 1
        time.sleep_ms(300)

    return self.wlan_sta.active()

  def initWifiAp(self):
    retryCount = 0
    while not self.wlan_ap.active() and maxRetry > retryCount:
      self.wlan_ap.active(True)
      if not self.wlan_ap.active():
        print('Retentativa de ativação da interface: network.AP_IF')
        retryCount += 1
        time.sleep_ms(300)

    return self.wlan_ap.active()

  def connect(self):
    if self.initWifiSta():
      self.getWifiCredentials()

      if self.wifi_ssid is not None and self.wifi_password is not None:
        self.connectWifiSta()
      else:
        self.startWifiAp()

    else:
      # nofity error on Wifi
      self.oledDisplay.clear()
      self.oledDisplay.log('Erro na interface:', 0, 5)
      self.oledDisplay.log('network.STA_IF', 0, 15)

  def connectWifiSta(self):
    if not wlan_sta.isconnected():
      wifi_pwd = self.wifi_password if self.wifi_pa_password == '' else None
      wlan_sta.connect(self.wifi_ssid, wifi_pwd)

      self.oledDisplay.clear()
      self.oledDisplay.log('Conetando Wi-Fi:', 0 , 5)
      self.oledDisplay.log('SSID: {0}'.format(self.wifi_ssid), 0 , 15)

      printCount = 0
      while not wlan_sta.isconnected() or maxRetry > retryCount:
        for printCount in range(10):
          if wlan_sta.isconnected():
            break
          time.sleep_ms(100)

          ouput_wait = 10 *  ' '

          if printCount <= 10:
            ouput_wait = '{0}{1}'.format((10 - printCount) * ' ', printCount * '.' )

          self.oledDisplay.log(ouput_wait, 0, 25)
        retryCount += 1


  def startWifiAp(self):
    if self.initWifiAp():
      self.wlan_ap.config(essid = wifi_pa_ssid, password = wifi_pa_password, authmode = 3)
      print(self.wlan_ap.ifconfig())

      self.oledDisplay.clear()
      self.oledDisplay.log('Conecte em:', 0, 5)
      self.oledDisplay.log('SSID: {0}'.format(wifi_pa_ssid), 0, 15)
      self.oledDisplay.log('Senha: {0}'.format(wifi_pa_password), 0, 25)

  def getWifiCredentials(self):
    self.wifi_ssid = self.database.getWifiSsid()
    self.wifi_password = self.database.getWifiPassword()

  def isWifiApActive(self):
    return self.wlan_ap.active()