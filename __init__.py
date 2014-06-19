import eg, httplib, urllib


eg.RegisterPlugin(
    name = "Pushover",
    author = "EssKaa",
    version = "1.0",
    createMacrosOnAdd = False,
    canMultiLoad = False,
    description = "This plugin sends notifications to you mobile using the Pushover service. For more details visit: https://pushover.net/"
)

class Pushover(eg.PluginBase):
    def __init__(self):
        self.AddAction(poSendMessage, clsName="Send message", description="")
        
    def __start__(self, username="", token=""):
    	eg.globals.poUsername = username
    	eg.globals.poToken = token
        
    def Configure(self, username="", token=""):
    
        panel= eg.ConfigPanel()
        labelUsername = wx.StaticText(panel, label="User:", pos=(10, 22))
        textUsername = wx.TextCtrl(panel, -1, username, (10, 40), (250, -1))
        labelToken = wx.StaticText(panel, label="Token:", pos=(10, 72))
        textToken = wx.TextCtrl(panel, -1, token, (10,90), (250, -1))

        while panel.Affirmed():
            panel.SetResult(textUsername.GetValue(), textToken.GetValue())

class ActionBase(eg.ActionClass):
    
    def runSendPushoverMessage(self, msgToSend="EventGhost test message."):
        if msgToSend:
            msgToSend = eg.ParseString(msgToSend)

	conn = httplib.HTTPSConnection("api.pushover.net:443")
	conn.request("POST", "/1/messages.json",
  		urllib.urlencode({
	   		"token": eg.globals.poToken,
    		"user": eg.globals.poUsername,
    		"message": msgToSend,
  		}), { "Content-type": "application/x-www-form-urlencoded" })
	conn.getresponse()

class poSendMessage(ActionBase):

    def __call__(self, msgToSend=None):
        if not msgToSend:
            raise Exception('Please enter message first')
        return self.runSendPushoverMessage(msgToSend=msgToSend)

    def Configure(self, msgToSend=""):
        panel = eg.ConfigPanel()
        labelMessage = wx.StaticText(panel, label="Message:", pos=(10, 22))
        textMessage = wx.TextCtrl(panel, -1, msgToSend, (10, 40), (400, -1))

        while panel.Affirmed():
            panel.SetResult(textMessage.GetValue())

