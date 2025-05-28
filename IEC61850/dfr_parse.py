import comtrade
import os
from datetime import datetime, timedelta

dir_path = "D:\\Documents\\AG S1 Agile\\ngimbang_agsys\\P442_babat_line2\\1\\DR"
file_path = ''
scrpath ='/var/www/html/dms_setting/assets/api/file_dr/9/PCS931_RCD_01689_20221113_110656_598/'


def getDFRvalue(srcPpath):
    selected_channel = [0, 1, 2, 3, 4, 5, 6]
    # scrpath = srcPpath

    # srcPpath = srcPpath.replace(".zip", '')
    newPath = ''
    # print(srcPpath)
    rec = ""
    for filename in os.listdir(srcPpath):
        f = os.path.join(srcPpath, filename)
        # print(f)
        if f:
            if ".cfg" in f:
                newPath = f.replace(".cfg", '')
                print(newPath)
                rec = comtrade.load(newPath+'.cfg', newPath+".dat")
                break
            elif ".CFG" in f:
                newPath = f.replace(".CFG", '')
                print(newPath)
                rec = comtrade.load(newPath+'.CFG', newPath+".DAT")
                break

    dfrValue = []
    TREf = []
    indexTriggerTime = 0
    for v in rec.time:
        TREf.append(timedelta(seconds=v)+rec.start_timestamp)
    # print(TREf[0].timestamp())
    #print(rec.trigger_timestamp)
    for i in range(len(TREf)):

        if rec.trigger_timestamp.timestamp() == round(TREf[i].timestamp(), 3):
            # print(i)
            indexTriggerTime = i
    print(indexTriggerTime)
    # for i in range(0, len(selected_channel)):
    #     index = selected_channel[i]
    #     # print(rec.analog_channel_unit[index])
    #     dfrValue.append("%s: %f %s" %
    #                     (rec.analog_channel_ids[index], rec.analog[index][indexTriggerTime], rec.analog_channel_unit[index]))
    #     # dfrValue.append()
    
    print(dir(rec))  # Melihat semua atribut yang tersedia dalam objek rec
    # print(rec.__dict__)  # Melihat isi atribut dari objek rec

    for i in range(0, len(rec.analog_channel_ids)):
        index = i
        print(rec.analog_channel_unit[index])
        dfrValue.append("%s: %f %s" %
                        (rec.analog_channel_ids[index], rec.analog[index][indexTriggerTime], rec.analog_channel_unit[index]))
    # for i in range(0, len(rec.digital)):
    #     print(rec.d)
    # print(rec.digital)
    statusValue = []

    for i in range(0, rec.status_count):
        if rec.status[i][indexTriggerTime] == 1 and rec.status[i][indexTriggerTime-1] == 0:
            statusValue.append("%s" %
                               (rec.status_channel_ids[i]))

    for i in range(0, rec.status_count):
        if rec.status[i][indexTriggerTime-2] == 1:
            print("%s" % (rec.status_channel_ids[i]))

    strDfrValue = ''
    for v in dfrValue:
        strDfrValue = strDfrValue + v + "%0D%0A"
    strStatusValue = ''
    for v in statusValue:
        strStatusValue = strStatusValue + v + "%0D%0A"
    # print(strDfrValue)
    return [strDfrValue,strStatusValue]


# print(getDFRvalue(scrpath))
