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

  def start_server(self):
    self.srv = MicroWebSrv(webPath='www/', port=8080, bindIP='0.0.0.0')
    self.srv.MaxWebSocketRecvLen = 256
    self.srv.WebSocketThreaded = False
    self.srv.AcceptWebSocketCallback = _acceptWebSocketCallback
    self.srv.Start()

  @MicroWebSrv.route('/')
  def _httpHandlerTestGet(self, httpClient, httpResponse):
    if (self.networkUtil.is_sta_active()):
      content = """\
      <!DOCTYPE html>
      <html lang=en>
        <head>
          <meta charset='UTF-8' />
         <title>TEST GET</title>
        </head>
        <body>
          <h1>TEST GET</h1>
          Client IP address = %s
          <br />
          <form action='/test' method='post' accept-charset='ISO-8859-1'>
            First name: <input type='text' name='firstname'><br />
            Last name: <input type='text' name='lastname'><br />
            <input type='submit' value='Submit'>
          </form>
        </body>
      </html>
      """ % httpClient.GetIPAddr()
      httpResponse.WriteResponseOk( headers		 = None,
                                    contentType	 = 'text/html',
                                    contentCharset = 'UTF-8',
                                    content 		 = content )
  def __init__(self, networkUtil):
    self.networkUtil = networkUtil
    _thread.start_new_thread(self.start_server, ())
