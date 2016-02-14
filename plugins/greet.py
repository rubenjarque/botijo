def init ( actions ):
    actions['greet'] = {'module': 'plugins.greet', 'method': 'greet'}
    actions['saluda'] = {'module': 'plugins.greet', 'method': 'saluda'}

def greet( chan, user, words ):
    chan.send_message("Hello " + user["name"] + "!")
    
def saluda( chan, user, words ):
    chan.send_message("Hola " + user["name"] + "!")