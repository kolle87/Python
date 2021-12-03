import json
import requests


nanopool = requests.get('https://rvn.nanopool.org/api/v1/user/RRRarQAs9cmn6btETjuvErSeGxYyfzmQSm')

if nanopool.status_code == 200:
    nanopool_json = json.loads(nanopool.content)
    print('Balance: ',nanopool_json['data']['balance'], 'RVN')
    print('unconfirmed: ', nanopool_json['data']['unconfirmed_balance'], 'RVN')
    print('Hashrate (calculated): ',nanopool_json['data']['hashrate'],'MH/s')
    print('Hashrate (Avg 1h)    : ',nanopool_json['data']['avgHashrate']['h1'],'MH/s')
    print('Hashrate (Avg 3h)    : ',nanopool_json['data']['avgHashrate']['h3'],'MH/s')
    print('Hashrate (Avg 6h)    : ',nanopool_json['data']['avgHashrate']['h6'],'MH/s')
    print('Hashrate (Avg 12h)   : ',nanopool_json['data']['avgHashrate']['h12'],'MH/s')
    print('Hashrate (Avg 24h)   : ',nanopool_json['data']['avgHashrate']['h24'],'MH/s')

nanominer = requests.get('http://192.168.1.13:9090/stat')

if nanominer.status_code == 200:
    nanominer_json = json.loads(nanominer.content)
    print(nanominer_json['Statistics']['Devices'][0]['name'])

    print('\tFan: ',nanominer_json['Statistics']['Devices'][0]['fan'],'%')
    print('\tPower: ',nanominer_json['Statistics']['Devices'][0]['power'].split(' ')[0],'W')
    print('\tTemp: ',nanominer_json['Statistics']['Devices'][0]['temp'],'°C')
    print('\tHashrate: ',nanominer_json['Statistics']['Devices'][0]['hashrates'][0]['hashrate'], 'MH/s')
    print('\taccepted: ',nanominer_json['Statistics']['Devices'][0]['hashrates'][0]['gpuAccepted'])
    print('\tdenied: ',nanominer_json['Statistics']['Devices'][0]['hashrates'][0]['gpuDenied'])

    print(nanominer_json['Statistics']['Devices'][1]['name'])
    print('\tFan: ',nanominer_json['Statistics']['Devices'][1]['fan'],'%')
    print('\tPower: ',nanominer_json['Statistics']['Devices'][1]['power'].split(' ')[0],'W')
    print('\tTemp: ',nanominer_json['Statistics']['Devices'][1]['temp'],'°C')
    print('\tHashrate: ',nanominer_json['Statistics']['Devices'][1]['hashrates'][0]['hashrate'], 'MH/s')
    print('\taccepted: ',nanominer_json['Statistics']['Devices'][1]['hashrates'][0]['gpuAccepted'])
    print('\tdenied: ',nanominer_json['Statistics']['Devices'][1]['hashrates'][0]['gpuDenied'])

    print('Hashrate : ',nanominer_json['Statistics']['Currencies'][0]['hashrate'], 'MH/s')
    print('Accepted : ',nanominer_json['Statistics']['Currencies'][0]['accepted'])
    print('Denied   : ',nanominer_json['Statistics']['Currencies'][0]['denied'])
    print('WorkTime : ',nanominer_json['Statistics']['Currencies'][0]['workTime'], 'sec')
    print('Reconnect: ',nanominer_json['Statistics']['Currencies'][0]['reconnectionCount'])