import time, re, json, bot_config, plugins, importlib
from slackclient import SlackClient

def getReceiverFromMessage( message ):
    cleanword=re.sub('[@<>:]', '', message)
    return cleanword

def sendAction( action, chan, user, words ):
    if action in plugins.actions:
        action_config = plugins.actions[action]
        module = importlib.import_module(action_config['module'])
        getattr(module, action_config['method'])(chan, user, words)
    else:
        chan.send_message("I'm sorry, but I don't understand that")

botijo_user = bot_config.bot_user
sc = SlackClient(bot_config.bot_token)

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
                        print "This is a message to botijo"
                        userinfo = json.loads(sc.api_call("users.info", user=evt["user"]))
                        
                        chan = sc.server.channels.find(evt["channel"])
                        if ((len(words) > 1)):
                            sendAction(words[1], chan, userinfo["user"], words)
                        else:
                            chan.send_message("What?")

    time.sleep(3)
