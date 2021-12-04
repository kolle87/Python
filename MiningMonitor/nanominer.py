import json
import time
import requests
from prometheus_client.metrics import Info
from prometheus_client import start_http_server, Gauge

class MiningMetrics:

    def __init__(self, polling_interval_seconds=10):
        self.polling_interval_seconds = polling_interval_seconds
        self.uptime = 0

        self.POOL_CON_ERR = Gauge('miner_pool_con_err','HTTP Connection Errors to Pool')
        self.POOL_RESP_ERR = Gauge('miner_pool_resp_err','HTTP Response Status from Pool not OK')
        self.MINER_CON_ERR = Gauge('miner_miner_con_err','HTTP Connection Errors to Miner')
        self.MINER_RESP_ERR = Gauge('miner_miner_resp_err','HTTP Response Status from Miner not OK')
        self.BALANCE = Gauge('miner_balance','Current confirmed wallet balance')
        self.BALANCE_UNCONFIRMED = Gauge('miner_balance_unconfirmed','Current balance waiting for confirmation')
        self.HR_CALC = Gauge('miner_hashrate_calc','Calculated current Hashrate')
        self.HR_1h = Gauge('miner_hashrate_1h','Average Hashrate over 1h')
        self.HR_3h = Gauge('miner_hashrate_3h','Average Hashrate over 3h')
        self.HR_6h = Gauge('miner_hashrate_6h','Average Hashrate over 6h')
        self.HR_12h = Gauge('miner_hashrate_12h','Average Hashrate over 12h')
        self.HR_24h = Gauge('miner_hashrate_24h','Average Hashrate over 24h')
        self.DEV0_NAME = Info('miner_dev0_name','Name of GPU 0')
        self.DEV0_FAN = Gauge('miner_dev0_fan','Fan speed of GPU 0')
        self.DEV0_POWER = Gauge('miner_dev0_power','Power consumption of GPU 0')
        self.DEV0_HR = Gauge('miner_dev0_hashrate','Hashrate of GPU 0')
        self.DEV0_TEMP = Gauge('miner_dev0_temp','Temperature of GPU 0')
        self.DEV0_ACCEPTED = Gauge('miner_dev0_accepted','Accepted shares of GPU 0')
        self.DEV0_DENIED = Gauge('miner_dev0_denied','Denied shares of GPU 0')
        self.DEV1_NAME = Info('miner_dev1_name','Name of GPU 1')
        self.DEV1_FAN = Gauge('miner_dev1_fan','Fan speed of GPU 1')
        self.DEV1_POWER = Gauge('miner_dev1_power','Power consumption of GPU 1')
        self.DEV1_HR = Gauge('miner_dev1_hashrate','Hashrate of GPU 1')
        self.DEV1_TEMP = Gauge('miner_dev1_temp','Temperature of GPU 1')
        self.DEV1_ACCEPTED = Gauge('miner_dev1_accepted','Accepted shares of GPU 1')
        self.DEV1_DENIED = Gauge('miner_dev1_denied','Denied shares of GPU 1')
        self.WORKER_HR = Gauge('miner_worker_hashrate', 'Total Hashrate of Miner')
        self.WORKER_ACCEPTED = Gauge('miner_worker_accepted', 'Total Shares accepted from Miner')
        self.WORKER_DENIED = Gauge('miner_worker_denied','Total Shares dinied from Miner')
        self.WORKER_UPTIME = Gauge('miner_worker_uptime','Miner uptime')
        self.WORKER_RESTARTS = Gauge('miner_worker_restarts','Count of Miner restarts')

    def run_fetching_loop(self):
        while True:
            self.fetch_data()
            time.sleep(self.polling_interval_seconds)
    
    def fetch_data(self):
        try:
            nanopool = requests.get('https://rvn.nanopool.org/api/v1/user/RRRarQAs9cmn6btETjuvErSeGxYyfzmQSm', timeout=5)

            if nanopool.status_code == 200:
                nanopool_json = json.loads(nanopool.content)
                #print('Balance: ',nanopool_json['data']['balance'], 'RVN')
                self.BALANCE.set(float(nanopool_json['data']['balance']))
                #print('unconfirmed: ', nanopool_json['data']['unconfirmed_balance'], 'RVN')
                self.BALANCE_UNCONFIRMED.set(float(nanopool_json['data']['unconfirmed_balance']))
                #print('Hashrate (calculated): ',nanopool_json['data']['hashrate'],'MH/s')
                self.HR_CALC.set(float(nanopool_json['data']['hashrate']))
                #print('Hashrate (Avg 1h)    : ',nanopool_json['data']['avgHashrate']['h1'],'MH/s')
                self.HR_1h.set(float(nanopool_json['data']['avgHashrate']['h1']))
                #print('Hashrate (Avg 3h)    : ',nanopool_json['data']['avgHashrate']['h3'],'MH/s')
                self.HR_3h.set(float(nanopool_json['data']['avgHashrate']['h3']))
                #print('Hashrate (Avg 6h)    : ',nanopool_json['data']['avgHashrate']['h6'],'MH/s')
                self.HR_6h.set(float(nanopool_json['data']['avgHashrate']['h6']))
                #print('Hashrate (Avg 12h)   : ',nanopool_json['data']['avgHashrate']['h12'],'MH/s')
                self.HR_12h.set(float(nanopool_json['data']['avgHashrate']['h12']))
                #print('Hashrate (Avg 24h)   : ',nanopool_json['data']['avgHashrate']['h24'],'MH/s')
                self.HR_24h.set(float(nanopool_json['data']['avgHashrate']['h24']))
            else:
                self.POOL_RESP_ERR.inc()
        except Exception as e:
            self.POOL_CON_ERR.inc()
            print(e)


        try:
            nanominer = requests.get('http://192.168.1.13:9090/stat', timeout=5)

            if nanominer.status_code == 200:
                nanominer_json = json.loads(nanominer.content)

                #print(nanominer_json['Statistics']['Devices'][0]['name'])
                self.DEV0_NAME.info({'name':nanominer_json['Statistics']['Devices'][0]['name']})
                #print('\tFan: ',nanominer_json['Statistics']['Devices'][0]['fan'],'%')
                self.DEV0_FAN.set(float(nanominer_json['Statistics']['Devices'][0]['fan']))
                #print('\tPower: ',nanominer_json['Statistics']['Devices'][0]['power'].split(' ')[0],'W')
                self.DEV0_POWER.set(float(nanominer_json['Statistics']['Devices'][0]['power'].split(' ')[0]))
                #print('\tTemp: ',nanominer_json['Statistics']['Devices'][0]['temp'],'°C')
                self.DEV0_TEMP.set(float(nanominer_json['Statistics']['Devices'][0]['temp']))
                #print('\tHashrate: ',nanominer_json['Statistics']['Devices'][0]['hashrates'][0]['hashrate'], 'MH/s')
                self.DEV0_HR.set(float(nanominer_json['Statistics']['Devices'][0]['hashrates'][0]['hashrate']))
                #print('\taccepted: ',nanominer_json['Statistics']['Devices'][0]['hashrates'][0]['gpuAccepted'])
                self.DEV0_ACCEPTED.set(float(nanominer_json['Statistics']['Devices'][0]['hashrates'][0]['gpuAccepted']))
                #print('\tdenied: ',nanominer_json['Statistics']['Devices'][0]['hashrates'][0]['gpuDenied'])
                self.DEV0_DENIED.set(float(nanominer_json['Statistics']['Devices'][0]['hashrates'][0]['gpuDenied']))

                #print(nanominer_json['Statistics']['Devices'][1]['name'])
                self.DEV1_NAME.info({'name':nanominer_json['Statistics']['Devices'][1]['name']})
                #print('\tFan: ',nanominer_json['Statistics']['Devices'][1]['fan'],'%')
                self.DEV1_FAN.set(float(nanominer_json['Statistics']['Devices'][1]['fan']))
                #print('\tPower: ',nanominer_json['Statistics']['Devices'][1]['power'].split(' ')[0],'W')
                self.DEV1_POWER.set(float(nanominer_json['Statistics']['Devices'][1]['power'].split(' ')[0]))
                #print('\tTemp: ',nanominer_json['Statistics']['Devices'][1]['temp'],'°C')
                self.DEV1_TEMP.set(float(nanominer_json['Statistics']['Devices'][1]['temp']))
                #print('\tHashrate: ',nanominer_json['Statistics']['Devices'][1]['hashrates'][0]['hashrate'], 'MH/s')
                self.DEV1_HR.set(float(nanominer_json['Statistics']['Devices'][1]['hashrates'][0]['hashrate']))
                #print('\taccepted: ',nanominer_json['Statistics']['Devices'][1]['hashrates'][0]['gpuAccepted'])
                self.DEV1_ACCEPTED.set(float(nanominer_json['Statistics']['Devices'][1]['hashrates'][0]['gpuAccepted']))
                #print('\tdenied: ',nanominer_json['Statistics']['Devices'][1]['hashrates'][0]['gpuDenied'])
                self.DEV1_DENIED.set(float(nanominer_json['Statistics']['Devices'][1]['hashrates'][0]['gpuDenied']))

                #print('Hashrate : ',nanominer_json['Statistics']['Currencies'][0]['hashrate'], 'MH/s')
                self.WORKER_HR.set(float(nanominer_json['Statistics']['Currencies'][0]['hashrate']))
                #print('Accepted : ',nanominer_json['Statistics']['Currencies'][0]['accepted'])
                self.WORKER_ACCEPTED.set(float(nanominer_json['Statistics']['Currencies'][0]['accepted']))
                #print('Denied   : ',nanominer_json['Statistics']['Currencies'][0]['denied'])
                self.WORKER_DENIED.set(float(nanominer_json['Statistics']['Currencies'][0]['denied']))
                #print('WorkTime : ',nanominer_json['Statistics']['Currencies'][0]['workTime'], 'sec')
                self.WORKER_UPTIME.set(float(nanominer_json['Statistics']['Currencies'][0]['workTime']))
                #print('Reconnect: ',nanominer_json['Statistics']['Currencies'][0]['reconnectionCount'])
                self.WORKER_RESTARTS.set(float(nanominer_json['Statistics']['Currencies'][0]['reconnectionCount']))

                if (float(nanominer_json['Statistics']['Currencies'][0]['workTime'])<self.uptime):
                    self.POOL_CON_ERR.set(0)
                    self.POOL_RESP_ERR.set(0)
                    self.MINER_CON_ERR.set(0)
                    self.MINER_RESP_ERR.set(0)
                self.uptime = float(nanominer_json['Statistics']['Currencies'][0]['workTime'])
            else:
                self.MINER_RESP_ERR.inc()
        except Exception as e:
            self.MINER_CON_ERR.inc()
            print(e)

def main():
    mining_metrics = MiningMetrics(polling_interval_seconds=10)
    start_http_server(9867)
    mining_metrics.run_fetching_loop()

if __name__ == "__main__":
    main()