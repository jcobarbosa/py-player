import _thread
from microWebSrv import MicroWebSrv

class WebServer():
  def _recvTextCallback(self, webSocket, msg) :
    print('WS RECV TEXT : %s' % msg)
    self.webSocket.SendText('Reply for %s' % msg)

  def _recvBinaryCallback(self, webSocket, data) :
    print('WS RECV DATA : %s' % data)

  def _closedCallback(self, webSocket) :
    print('WS CLOSED')

  def _acceptWebSocketCallback(self, webSocket, httpClient) :
    print('WS ACCEPT')
    self.webSocket.RecvTextCallback   = _recvTextCallback
    self.webSocket.RecvBinaryCallback = _recvBinaryCallback
    self.webSocket.ClosedCallback 	 = _closedCallback

  def start_server(self, networkUtil) :
    self.srv = MicroWebSrv(webPath='www/', port=8181, bindIP='0.0.0.0', networkUtil=networkUtil)
    self.srv.MaxWebSocketRecvLen = 256
    self.srv.WebSocketThreaded = True
    self.srv.AcceptWebSocketCallback = self._acceptWebSocketCallback
    self.srv.Start(threaded=True)

  @MicroWebSrv.route('/init')
  def _httpHandlerInitGet(httpClient, httpResponse):
    self.oledDisplay.clear()
    self.oledDisplay.log('init', 0, 25)

  @MicroWebSrv.route('/')
  def _httpHandlerTestGet(httpClient, httpResponse):
    _webserver = httpClient._microWebSrv
    if (_webserver.networkUtil.isWifiApActive()):
      content = """\
      <!DOCTYPE html>
      <html lang=en>
      <head>
        <meta charset='UTF-8' />
        <title>Inicial - Configurar Wifi</title>
      </head>
      <body>
        <form id="formWifi"><input type="submit" value="Atualizar" /></form>
        <form>
        <h1>Redes disponíveis:</h1>
        <table>
          <thead>
            <tr>
              <th>&nbsp;</th>
              <th>Channel</th>
              <th>SSID</th>
              <th>RSSI</th>
              <th>Autenticação</th>
            </tr>
          </thead>
          <tbody>
            %s
          </tbody>
        </table>
        <br />
        <label for="pwd" id="pwd-label" style="display:none">Senha:</label> <input type="password" id="pwd" name="pwd" style="display:none" />
        <br />
        <button onclick="event.preventDefault();enviar()";>Salvar</button>
        </form>
        <script type="text/javascript">
            function selecionarWifi() {
                document.getElementById('pwd').style.display = 'inherit';
                document.getElementById('pwd-label').style.display = 'inherit';
            }
            
            function enviar() {
                if (document.getElementById('pwd').value.trim() === '') {
                    alert('Favor informar a senha de acesso!');
                } else {
                    document.getElementById('formWifi').submit();
                }
            }
        </script>
      </body>
      </html>
      """ % _webserver.networkUtil.listNearbyWifiNetworks()
      httpResponse.WriteResponseOk( headers		 = None,
                                    contentType	 = 'text/html',
                                    contentCharset = 'UTF-8',
                                    content 		 = content )

  def __init__(self, networkUtil, oledDisplay):
    self.networkUtil = networkUtil
    self.oledDisplay = oledDisplay
    self.start_server(networkUtil)
