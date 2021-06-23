import os
import requests
import json
import re
import time
import hashlib

state = 1
apiendpoint = 'localhost'
apiport='18000'
authtoken = 'asdf'
urlprefix = 'http://' + apiendpoint + ':' + apiport + '/api?command='

lasthash = ''
minerstopparams = '{"id":1,"method":"miner.stop","params":[]}'
restartparams = '{"id":1,"method":"restart","params":[]}' 
subscribeinfoparams = '{"id":1,"method":"subscribe.info","params":[]}'
quitparams = '{"id":1,"method":"quit","params":[]}'

def stop():
    r = requests.get(url = (urlprefix + minerstopparams), headers = {'Authorization': authtoken})
def start():
    r = requests.get(url = (urlprefix + quitparams), headers = {'Authorization': authtoken})
def getstate():
    r = requests.get(url = (urlprefix + subscribeinfoparams), headers = {'Authorization': authtoken}) 
    if(json.loads(r.text)['connected'] == True):
        return 1
    return 0
while True:
    try:
        currenthash = hashlib.md5(open('games.txt','rb').read()).hexdigest()
        if(not lasthash == currenthash):
            restring = ''
            with open("games.txt") as file: 
                for l in file.readlines():
                    restring += l.rstrip() + '|'
            regex = re.compile('('+restring[:-1]+')',re.IGNORECASE)
            lasthash = currenthash
        state = getstate()
        processes = os.popen('tasklist /NH /FI "STATUS eq running" /FO CSV').read()
        if(re.search(regex, processes) is not None):
            if(state==1):
                print('stopping')
                stop()
        else:
            if(state==0):
                print('starting')
                start()
        time.sleep(30)
    except Exception as e:
        print(e)
        time.sleep(30)
