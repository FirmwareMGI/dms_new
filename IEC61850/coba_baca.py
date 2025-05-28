import ctypes
try:
    import lib61850
except:
    import lib61850_linux as lib61850
from libiec61850client import iec61850client
import db
import time
from datetime import datetime
import requests

DEBUG = False  # """untuk percobaan dengan server localhost"""

if DEBUG:
    dataDevice = ['127.0.0.1']
else:
    dataMeasurement = db.readDb.m_file_iec_read_by_active(0)
    dataDevices = db.readDb.device_list(1)
dataDevice = []

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

def ClientFile61850_dir():
    for i in range(0, max_client):
        if error[i]['error'].value == lib61850.IED_ERROR_OK:
            error_file = lib61850.IedClientError()
            rootDirectory = lib61850.IedConnection_getFileDirectory(
                con[i]['con'], error_file, "/")
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
                file_modified = lib61850.FileDirectoryEntry_getLastModified(
                    entry)
                print("name: %s size: %d modified: %s" %
                      (file_name, file_size, file_modified))

                directoryEntry = lib61850.LinkedList_getNext(directoryEntry)
            lib61850.LinkedList_destroy(directoryEntry)
        else:
            print("connection issue")

def ClientFile61850_get(file_name):
    handler = lib61850.IedClientGetFileHandler(_getFileHandler)
    localfilename = file_name.replace('\\', '')
    open(localfilename, "w").close()  # create an empty file
    error_getfile = lib61850.IedClientError()
    file_name_array = bytes(localfilename.encode('utf-8'))
    print(file_name_array)
    for i in range(max_client):
        lib61850.IedConnection_getFile(
            con[i]['con'], error_getfile, file_name, handler, ctypes.c_char_p(file_name_array))
        if error_getfile.value != lib61850.IED_ERROR_OK:
            print("Failed to get file!")

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
                    # print(item_id)
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
            error), object_read, object_fc) #pembacaan beberapa param dari file library
        #print(len(object_read[i][j]))
        val, types = iec61850client.printValue(value) #mendapatkan nilai value dan type data itu apa (float,bolean )
        #print(val,types)
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

Client61850_config()
CLient61850_itemConfig()
            

try:
    while True:
        lib61850.Thread_sleep(3000)
        for i in range(0, max_client): #ada berapa nilai register yg didaftarkan
            if 'obj' in object_read[i]:
                for j in range(len(object_read[i]['obj'])): #ada berapa data yg ditemukan (dipisahkan)
                    print("counting object %d" % (j)) #data muncul pisah
                    value, types = CLient61850_monitoringRead(
                        con[i]['con'], error[i]['error'], object_read[i]['obj'][j], object_FC[i]['obj'][j])
                    dataJson = {"alias": alias_monit[i]['alias'][j], "hasil": value, "dataType": types}
                    print(dataJson)
                    coba = f"{object_read[i]['itemID'][j]}"
                    print(range(len(object_read[i]['obj'])))

except KeyboardInterrupt:
    CLient61850_destroyConn()
    print('interrupted!')
