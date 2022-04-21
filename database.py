import microPyDatabase

class Db:

  def getConfigValueFromKey(self, key):
    self.config_table = self.databaseFile.open_table('config')
    return self.config_table.query({'key': key})

  def getWifiSsid(self):
    return self.getConfigValueFromKey('wifi_ssid')
  
  def getWifiPassword(self):
    return self.getConfigValueFromKey('wifi_password')

  def getAudios(self, activeFlag):
    self.databaseFile = microPyDatabase.Database.open('appdb')
    self.audios_table = self.databaseFile.open_table('audios')
    return self.audios_table.query({'active': activeFlag})

  def insertConfig(self, key, value, description = ''):
    self.config_table = self.databaseFile.open_table('config')
    self.config_table.insert({'key': key, 'value': value, 'description': description})

  def __init__(self):
    try:
      self.databaseFile = microPyDatabase.Database.open('appdb')
    except Exception:
      self.databaseFile = microPyDatabase.Database.create('appdb')

    self.databaseFile = microPyDatabase.Database.open('appdb')
    
    try:
        self.audios_table = self.databaseFile.create_table('audios', ['name', 'description', 'active'])
        self.audios_table = self.databaseFile.open_table('audios')
    except:
        self.audios_table = self.databaseFile.open_table('audios')
    self.audios_table.insert({'name': 'cantos01', 'description': 'Cantos para inicio', 'active': '1'})
    self.audios_table.insert({'name': 'cantos02', 'description': 'Cantos para inicio', 'active': '0'})
    self.audios_table.insert({'name': 'cantos03', 'description': 'Cantos para inicio', 'active': '1'})

    try:
        self.config_table = self.databaseFile.create_table('config', ['key', 'value', 'description'])
        self.config_table = self.databaseFile.open_table('config')
    except:
        self.config_table = self.databaseFile.open_table('config')
    # self.insertConfig('wifi_ssid', '')
    # self.insertConfig('wifi_password', '')
