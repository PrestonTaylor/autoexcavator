import os
import requests
import json
import re
import time

state = 1
apiendpoint = 'localhost'
apiport='18000'
authtoken = 'asdf'
authtokenheader =  {'Authorization': authtoken}
urlprefix = 'http://' + apiendpoint + ':' + apiport + '/api?command='
stopfor = ('RocketLeague.exe', 'Satisfactory.exe')
restring = ''
for x in stopfor:
    restring += x + '|'
regex = re.compile('('+restring[:-1]+')')

minerstopparams = '{"id":1,"method":"miner.stop","params":[]}'
restartparams = '{"id":1,"method":"restart","params":[]}'
subscribeinfoparams = '{"id":1,"method":"subscribe.info","params":[]}'

def stop():
    r = requests.get(url = (urlprefix + minerstopparams), headers = authtokenheader)
    print(r.text)
def start():
    r = requests.get(url = (urlprefix + restartparams), headers = authtokenheader)
    print(r.text)
def getstate():
    r = requests.get(url = (urlprefix + subscribeinfoparams), headers = authtokenheader)
    if(json.loads(r.text)['connected'] == True):
        return 1
    return 0
while True:
    state = getstate()
    processes = os.popen('tasklist /NH /FI "STATUS eq running" /FO CSV').read()
    if(re.search(regex, processes) is not None):
        if(state==1):
            stop()
    else:
        if(state==0):
            start()
    time.sleep(15)
