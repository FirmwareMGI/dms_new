import ctypes
try:
    import lib61850
except:
    import lib61850_linux as lib61850
import zipfile
from zipfile import ZipFile
from libiec61850client import iec61850client
import db
import time
from datetime import datetime
import mqtt as mqtt
import requests

import os, socket

DEBUG = False  # """untuk percobaan dengan server localhost"""

if DEBUG:
    dataDevice = ['127.0.0.1']
else:
    dataMeasurement = db.readDb.m_file_iec_read_by_active(0)
    dataDevices = db.readDb.device_list(1)
    #dataDRIEC = db.
dataDevice = []
dbMqtt = db.readDb.network_mqtt(0)

for v in dataDevices:
    if v['port_type'] == '2':
        dataDevice.append(v)
max_client = len(dataDevice)

dic_conn = []

alias_name = []
rack_location = []
alias_monit = []
ipserver = []
hostname = []
tcpport = []
error = []
con = []
model = []
object_read = []
object_FC = []
file_list = []

client = None

extension_file_dr = [".cfg", ".dat", ".hdr", ".cev", ".txt",
                     ".CFG", ".DAT", ".HDR", ".CEV", ".TXT"]

def _FC(rawfc):
    if rawfc == "ST":
        return lib61850.IEC61850_FC_ST
    if rawfc == "MX":
        return lib61850.IEC61850_FC_MX
    if rawfc == "SP":
        return lib61850.IEC61850_FC_SP
    if rawfc == "SV":
        return lib61850.IEC61850_FC_SV
    if rawfc == "CF":
        return lib61850.IEC61850_FC_CF
    if rawfc == "DC":
        return lib61850.IEC61850_FC_DC
    if rawfc == "SG":
        return lib61850.IEC61850_FC_SG
    if rawfc == "SE":
        return lib61850.IEC61850_FC_SE
    if rawfc == "SR":
        return lib61850.IEC61850_FC_SR
    if rawfc == "OR":
        return lib61850.IEC61850_FC_OR
    if rawfc == "BL":
        return lib61850.IEC61850_FC_BL
    if rawfc == "EX":
        return lib61850.IEC61850_FC_EX
    if rawfc == "CO":
        return lib61850.IEC61850_FC_CO
    if rawfc == "US":
        return lib61850.IEC61850_FC_US
    if rawfc == "MS":
        return lib61850.IEC61850_FC_MS
    if rawfc == "RP":
        return lib61850.IEC61850_FC_RP
    if rawfc == "BR":
        return lib61850.IEC61850_FC_BR
    if rawfc == "LG":
        return lib61850.IEC61850_FC_LG
    if rawfc == "GO":
        return lib61850.IEC61850_FC_GO


def _getFileHandler(parameter, buffer, bytesRead):
    filename = ctypes.cast(parameter, ctypes.c_char_p).value.decode(
        "utf-8")  # convert parameter back to python string
    print("received %i bytes for file: %s" % (bytesRead, filename))
    if bytesRead > 0:
        with open(filename, "ab") as fp:
            bytesbuffer = ctypes.string_at(buffer, bytesRead)
            fp.write(bytesbuffer)  # append bytes to file
    return True


#def ClientFile61850_dir():
def ClientFile61850_dir(con):
    counterFile = 0
    listFile = []
    #for i in range(0, max_client):
     #   if error[i]['error'].value == lib61850.IED_ERROR_OK:
    error_file = lib61850.IedClientError()
    rootDirectory = lib61850.IedConnection_getFileDirectory(
        con, error_file, "")
    print(rootDirectory)
    if error_file.value != lib61850.IED_ERROR_OK:
        print("Error retrieving file directory")
        exit(1)

    directoryEntry = lib61850.LinkedList_getNext(rootDirectory)

    while directoryEntry:

        entry = ctypes.cast(lib61850.LinkedList_getData(
            directoryEntry), lib61850.FileDirectoryEntry)

        file_name = lib61850.FileDirectoryEntry_getFileName(
            entry).decode("UTF-8")
        file_size = lib61850.FileDirectoryEntry_getFileSize(entry)
        file_modified = lib61850.FileDirectoryEntry_getLastModified(entry)
        print("name: %s size: %d modified: %s" %(file_name, file_size, file_modified))
        for v in extension_file_dr:
            if v in file_name:
                listFile.append([file_name, file_modified])

        directoryEntry = lib61850.LinkedList_getNext(directoryEntry)
    lib61850.LinkedList_destroy(directoryEntry)
    print(counterFile)
    return listFile
       # else:
        #    print("connection issue")


def ClientFile61850_get(file_name):
    handler = lib61850.IedClientGetFileHandler(_getFileHandler)
    localfilename = file_name.replace('COMTRADE/', '')
    open(localfilename, "w").close()  # create an empty file
    error_getfile = lib61850.IedClientError()
    file_name_array = bytes(localfilename.encode('utf-8'))
    print(file_name_array)
    for i in range(max_client):
        lib61850.IedConnection_getFile(
            con[i]['con'], error_getfile, file_name, handler, ctypes.c_char_p(file_name_array))
        if error_getfile.value != lib61850.IED_ERROR_OK:
            print("Failed to get file!")
            
            
def build_zip(dirName):
    dirName = dirName.replace('COMTRADE/', '')
    
#    json_names = {f.stem for f in p.iterdir() if f.suffix == '.json'}
#    nii_names = {Path(f.stem).stem for f in p.iterdir() if f.suffixes == ['.nii', '.gz']}
#    for file_name in json_names & nii_names:
#        json_path = p / (file_name + '.json')
#        nii_path = p / (file_name + '.nii.gz')
    
    iecdirname = '/home/pi/Desktop/DMSv1.2/IEC61850/zipDR/'
    with ZipFile('/home/pi/Desktop/DMSv1.2/IEC61850/zipDR/'+ dirName +'.zip', 'w') as zipObj:
        zipObj.write(dirName+".dat", compress_type=zipfile.ZIP_DEFLATED)
        zipObj.write(dirName+".cfg", compress_type=zipfile.ZIP_DEFLATED)
        zipObj.write(dirName+".hdr", compress_type=zipfile.ZIP_DEFLATED)
    
    return iecdirname + dirName +'.zip'
    
    
    
    if not os.path.exists('/home/pi/Desktop/DMSv1.2/IEC61850/' + dirName):
        print("Folder " , dirName ,  " tidak tersedia ")
    else:
        shutil.rmtree('/home/pi/Desktop/DMSv1.2/IEC61850/'+dirName)
        print("Folder telah dihapus")
        
    


def Client61850_config():

    if DEBUG:
        for i in range(0, max_client):
            hostname[i] = dataDevice[i]
            tcpport[i] = 102
            error[i]['error'] = lib61850.IedClientError()
            con[i]['con'] = lib61850.IedConnection_create()

        for i in range(max_client):
            lib61850.IedConnection_connect(
                con[i]['con'], ctypes.byref(error[i]['error']), hostname[i], int(tcpport[i]))
    else:
        for i in range(0, max_client):
            hostname.append(
                {'id': dataDevice[i]["id_device"],
                 'hostname': dataDevice[i]["ip_address"]})
            # ipserver[i] = dataMeasurement[i]['ipserver']
            tcpport.append(
                {'id': dataDevice[i]["id_device"],
                 'port': dataDevice[i]["port_address"]})
            error.append(
                {'id': dataDevice[i]["id_device"],
                 'error': lib61850.IedClientError()})
            con.append(
                {'id': dataDevice[i]["id_device"],
                 'con': lib61850.IedConnection_create()})

            object_read.append(
                {'id': dataDevice[i]["id_device"]})

            object_FC.append(
                {'id': dataDevice[i]["id_device"]})

            alias_monit.append(
                {'id': dataDevice[i]["id_device"]})

            alias_name.append(
                {'id': dataDevice[i]["id_device"]})

            rack_location.append(
                {'id': dataDevice[i]["rack_location"]})

    for i in range(0, max_client):
        lib61850.IedConnection_connect(
            con[i]['con'], ctypes.byref(error[i]['error']), hostname[i]['hostname'], int(tcpport[i]['port']))
        if (error[i]['error'].value == lib61850.IED_ERROR_OK):
            print("IEC61850 Connection OK in %s:%s" % (
                hostname[i]['hostname'], tcpport[i]['port']))
        else:
            print("IEC61850 Connection error in %s:%s" % (
                hostname[i]['hostname'], tcpport[i]['port']))


def CLient61850_itemConfig():
    # for k,v in dataMeasurement.items():
    #     if v in object_read['id']
    for v in dataMeasurement:
        # if v in object_read['id']
        if v["active"] == 1:
            for i in range(len(object_read)):
                if v['id_device'] == alias_monit[i]['id']:
                    if 'alias' in alias_monit[i]:
                        print('key obj')
                    else:
                        alias_monit[i]['alias'] = []
                        alias_name[i]['name'] = []

                    alias_monit[i]['alias'].append(v['alias'])
                    alias_name[i]['name'].append(v['name'])

                if v['id_device'] == object_read[i]['id']:
                    # print(i)
                    # if 'alias' in alias_monit[i] :
                    #     print('key obj')
                    # else:
                    #     alias_monit[i]['alias'] = []

                    # alias_monit[i]['alias'].append({'id': dataDevice[i]["id_device"],'obj': v['alias']})

                    fc_split = v["item_id"].split("$")
                    item_id = v["item_id"].replace("$"+fc_split[1], "")
                    print(item_id)
                    # object_FC[i].append(_FC(fc_split[1]))
                    if 'obj' in object_read[i] or 'obj' in object_FC[i]:
                        print('key obj')
                    else:
                        object_read[i]['obj'] = []
                        object_read[i]['itemID'] = []
                        object_FC[i]['obj'] = []

                    object_read[i]['obj'].append(
                        v["domain_id"]+"/"+item_id.replace("$", "."))
                    object_read[i]['itemID'].append(
                        v["domain_id"]+"/"+item_id)
                    object_FC[i]['obj'].append(_FC(fc_split[1]))
                    # j += 1


def CLient61850_monitoringRead(con, error, object_read, object_fc):
    if (error.value == lib61850.IED_ERROR_OK):
        value = lib61850.IedConnection_readObject(con, ctypes.byref(
            error), object_read, object_fc)
        # print(object_read)
        val, types = iec61850client.printValue(value)
        return val, types
    else:
        print("Failed to connect to %s:%s" % ("hostname", "102"))
        return 0, 0


def CLient61850_monitoringLoop():
    for i in range(0, max_client):
        for j in range(len(object_read[i])):
            value = lib61850.IedConnection_readObject(con[0], ctypes.byref(
                error[0]), object_read[i][j], object_FC[i][j])
            val, types = iec61850client.printValue(value)
            print(val, types)
            # if types == 'utc-time':


def CLient61850_destroyConn():
    for i in range(0, max_client):
        lib61850.IedConnection_release(con[i]['con'], error[i]['error'])
        if (error[i]['error'].value != lib61850.IED_ERROR_OK):
            print("Release returned error: %d" % error[i]['error'].value)
        else:
            while (lib61850.IedConnection_getState(con[i]['con']) != lib61850.IED_STATE_CLOSED):
                lib61850.Thread_sleep(10)

        lib61850.IedConnection_destroy(con[i]['con'])


def isOpen(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(socket.SHUT_RDWR)
        print("IP: %s Port: %d Opened" % (ip, port))
        return True
    except:
        print("IP: %s Port: %d Closed" % (ip, port))
        return False
    finally:
        s.close()


def Client61850_checkConnect(host, port, con, error):
    # response = os.system("ping -n 1 " + '192.168.2.13')
    response = isOpen(host, port)
    if not response:
        lib61850.IedConnection_connect(
            con, ctypes.byref(error), host, int(port))
        if (error.value == lib61850.IED_ERROR_OK):
            print("IEC61850 Connection OK in %s:%s" % (
                host, port))
        else:
            print("IEC61850 Connection error in %s:%s" % (
                host, port))
    else:
        if (error.value == lib61850.IED_ERROR_OK):
            print("IEC61850 Connection OK in %s:%s" % (
                host, port))
        else:
            print("IEC61850 Connection error in %s:%s and Reconnecting" % (
                 host, port))
            lib61850.IedConnection_connect(
                con, ctypes.byref(error), host, int(port))


def connectMqtt(mqtt):
    global mqttRetry
    global client
    if (client != None):
        print("rekonnect mqtt")
        client.disconnect()
    dbMqtt = db.readDb.network_mqtt(0)
    mqttUser = dbMqtt[0]['mqtt_username']
    mqttPass = dbMqtt[0]['mqtt_pass']
    broker = dbMqtt[0]['mqtt_server']
    port = dbMqtt[0]['mqtt_port']
    try:
        client = mqtt.connect_mqtt(mqttUser, mqttPass, broker, port)
        client.loop_start()
        # client.loop_forever()
    except:
        print("mqttNOtconnect")
        if (mqttRetry < 10):
            connectMqtt(mqtt)


mqtt = mqtt.MQTT(0)
connectMqtt(mqtt)

Client61850_config()
CLient61850_itemConfig()
flagNotif = 0
print(object_read)
# print(object_FC)
listFIleprev = 0


listfile = []
for i in range(0, max_client):
    listfile.append(ClientFile61850_dir(con[i]['con']))
print(listfile)
for i in range(0, max_client):
    listfile[i].sort(key=lambda x: x[1], reverse=True)
listfile_prev = listfile
print(listfile)
print(listfile_prev)


valueDataBoolean = []
for i in range(0, max_client):
    valueDataBoolean.append([])
    if 'obj' in object_read[i]:
        for j in range(len(object_read[i]['obj'])):
            value, types = CLient61850_monitoringRead(con[i]['con'], error[i]['error'], object_read[i]['obj'][j], object_FC[i]['obj'][j])
            valueDataBoolean[i].append(value)
print(valueDataBoolean)
valueDataBooleanPrev = valueDataBoolean

flagStatus = 0


try:
    while True:
        lib61850.Thread_sleep(3000)
        for i in range(0, max_client):

            #Client61850_checkConnect(hostname[i]['hostname'], int(tcpport[i]['port']), con[i]['con'], error[i]['error'])
            if 'obj' in object_read[i]:
                for j in range(len(object_read[i]['obj'])):
                    print("counting object %d" % (j))
                    value, types = CLient61850_monitoringRead(
                        con[i]['con'], error[i]['error'], object_read[i]['obj'][j], object_FC[i]['obj'][j])
                    dataJson = {
                        "alias": alias_monit[i]['alias'][j], "val": value, "dataType": types}
                    print(dataJson)
                    kode_wilayah = "0001"
                    print(valueDataBoolean)
                    print(valueDataBooleanPrev)

                    # if (alias_monit[i]['alias'][j] == "TRIP"):
                    if (types == 'boolean'):
                        if valueDataBoolean[i][j] != valueDataBooleanPrev[i][j]:
                            print(valueDataBoolean)
                            if flagStatus == 0:
                                flagStatus = 1
                                print("kirim notif")
                                # send_telegram()
                        else:
                            flagStatus = 0

#try:
#    while True:
#        lib61850.Thread_sleep(3000)
#        for i in range(0, max_client):
            
        #time.sleep(0.5)

except KeyboardInterrupt:
    CLient61850_destroyConn()
    print('interrupted!')
