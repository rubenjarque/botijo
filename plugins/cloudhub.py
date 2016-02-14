import requests, cloudhub_config, re

applications_url='https://anypoint.mulesoft.com/cloudhub/api/applications'
version_re = '\d+\.\d+'

def init ( actions ):
    actions['status'] = {'module': 'plugins.cloudhub', 'method': 'status'}
    
def getUserAuth( env_name ):
    user = cloudhub_config.username + '@' + env_name
    print user
    return user

def getVersionFromFilename( filename ):
    print 'matching ' + filename
    match = re.search(version_re, filename)
    if match:
        print 'matchs'
        return match.group()
    else:
        print 'does not match'
        return ''

def status( chan, user, words ):
    env = 'dev'
    print words
    print len(words)
    if len(words) >= 3:
        if  words[2] in cloudhub_config.environments:
            env = words[2]
    
    for cloudhub_environment in cloudhub_config.environments[env]:
        response = requests.get(applications_url, auth=(getUserAuth(cloudhub_environment), cloudhub_config.password))
        data = response.json()
        print data
        if ('error' in data):
            chan.send_message('I could not access CLoudHub: ' + data['message'])
            break
        else:
            for application in data:
                print application
                status = application['status']
                if 'deploymentUpdateStatus' in application:
                    status = application['deploymentUpdateStatus']
                    
                emoji = ""
                if 'STARTED' == status:
                    emoji = ':white_check_mark:'
                if 'DEPLOYING' == status:
                    emoji = ':clock2:'
                if 'UNDEPLOYED' == status:
                    emoji = ':grey_exclamation:'
                    
                version = ''
                if 'filename' in application:
                    version = getVersionFromFilename(application['filename'])
                    if version:
                        version = ' [version=' + version + ']'
                    
                chan.send_message(application['domain'] + ': ' + status + ' ' + emoji + version)