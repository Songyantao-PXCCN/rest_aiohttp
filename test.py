import logging
import os
import time

import com.Phoenixcontact.REST as PLCnREST
import com.Phoenixcontact.utils as PLCnUtils

# setting log function
_localpath = os.path.split(os.path.abspath(__file__))[0]
_logpath = os.path.join(_localpath, 'log/')
log = PLCnUtils.Logger.Log()
log.setLogConfig(level=logging.DEBUG, logPath=_logpath, logFilename='Outputs.log')

client = PLCnREST.NewClient('192.168.124.10')
client.PLCnUserName = 'admin'
client.PLCnPasswd = '42bad0fd'
client.sessionMode = True
client.connect()


GlobalGroup = client.registerReadGroups(['ESM_DATA.ESM_INFOS[1].TICK_COUNT'])

GlobalGroup.asyncStart()

ddd = 0
l = 0
time2 = 0
while True:
    t = int(GlobalGroup._Results.get('ESM_DATA.ESM_INFOS[1].TICK_COUNT',0))

    if l != t :
        time1 = time.time()
        print ('{}:::::{}----{}'.format('+'if t>l else '-',time1 - time2,t))
        time2 = time1
        l = t



    # for i in range(10):
    #     ts = time.time()
    #     tmp += 1
    #     # res = client.writeDatas({'A': tmp})
    #     # ff = client.readDatas_list(['A'])
    #     y=GlobalGroup.results_dict
    #     te = time.time()
    #     print("{} \t\t----- {}".format(y, te-ts))
    #     if tmp > 500:
    #         tmp = 0
    #
    # # time.sleep(21*60)




