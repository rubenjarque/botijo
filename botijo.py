import time, re, json
from slackclient import SlackClient
from pprint import pprint

def getReceiverFromMessage( message ):
    cleanword=re.sub('[@<>:]', '', message)
    return cleanword

def saluda( chan, user ):
    print "send saluda message"
    chan.send_message("Hola " + user["name"] + "!")
    print "sent saluda message"
    
def despide( chan, user ):
    chan.send_message("Que te follen " + user["name"])

def sendAction( action, chan, user ):
    print "choosing action for " + action
    if (action == "saluda"):
        saluda(chan, user)
    if (action == "despidete"):
        despide(chan, user)

token = "xoxb-21267660148-Lj0G7yBSjMq9UxOwhJ6uVQnw"
botijo_user = "U0M7VKE4C"
actions = ["saluda", "despidete"]
sc = SlackClient(token)

if sc.rtm_connect():
    while True:
        new_evts = sc.rtm_read()
        for evt in new_evts:
            if "type" in evt:
                if evt["type"] == "message" and "text" in evt:
                    print(evt)    
                    message=evt["text"]
                    
                    words = message.split()
                    if (getReceiverFromMessage(words[0]) == botijo_user):
                        print "Este es un mensaje para botijo"
                        userinfo = json.loads(sc.api_call("users.info", user=evt["user"]))
                        pprint(userinfo["user"]["name"])
                        
                        chan = sc.server.channels.find(evt["channel"])
                        if ((len(words) > 0) & (words[1] in actions)):
                            sendAction(words[1], chan, userinfo["user"])
                        else:
                            chan.send_message("Lo siento " + userinfo["user"]["name"] + ", pero no te entiendo")
                    
                    #chan = sc.server.channels.find(evt["channel"])
                    #if chan:
                        #chan.send_message(message)
    time.sleep(3)
