import ctypes
try:
    import lib61850
except:
    import lib61850_linux as lib61850
import zipfile
from zipfile import ZipFile
from libiec61850client import iec61850client
import db_v2 as db
import time
from datetime import datetime
from paho.mqtt import client as mqtt_client
import paho.mqtt.publish as mqtt_publish
import requests
import json
import logging
import pathlib
from pathlib import Path, PurePosixPath

import os
import sys
import socket


logging.basicConfig(format='%(asctime)s - %(levelname)s - [%(funcName)s():%(lineno)d] %(message)s',
                    level=logging.DEBUG)
# note the `logger` from above is now properly configured
logger = logging.getLogger()
logger.debug("started")

# DBdataMeasurement = db.readDb.m_file_iec_read_by_active(0)
# DBdataDevices = db.readDb.device_list(1)
# DBdataNetwork = db.readDb.network(0)
# DBdataMMesin = db.readDb.m_mesin(0)
# DBMqtt = db.readDb.network_mqtt(0)

dataDevice = []

database = {}
connections = {}
items = {}
disturbance = {}
systems = {}

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
rack_location = []
type_relay = []
name_alias = []
iecfolder = []

time_3s = time.time()
time_60s = time.time()

client = None

# MICOM [.cfg, .dat]
# NR [.cfg,.dat,.hdr]
# SIEMENS [.zip]
# ABB
# TOSHIBA
# GE
# QUALITROL
# GEC
# ALSTOM
extension_file_dr = [".cfg", ".dat", ".hdr", ".cev", ".txt", ".inf",
                     ".CFG", ".DAT", ".HDR", ".CEV", ".TXT", ".INF",
                     ".zip", ".ZIP"]
extension_file_dr_except = ["h.zip", "h.ZIP"]


testFolder = "/"


def _getFileHandler(parameter, buffer, bytesRead):
    filename = ctypes.cast(parameter, ctypes.c_char_p).value.decode(
        "utf-8")  # convert parameter back to python string
    # print("received %i bytes for file: %s" % (bytesRead, filename))
    if bytesRead > 0:
        with open(filename, "ab") as fp:
            bytesbuffer = ctypes.string_at(buffer, bytesRead)
            fp.write(bytesbuffer)  # append bytes to file
    return True


def _printValue(value):
    _type = lib61850.MmsValue_getTypeString(value)
    _type = str(_type)
    if _type == "boolean":
        return ("%r" % lib61850.MmsValue_getBoolean(value)), _type
    if _type == "array":
        return ("arr"), _type
    if _type == "bcd":
        return ("bcd"), _type
    if _type == "binary-time":
        return ("%i" % lib61850.MmsValue_getBinaryTimeAsUtcMs(value)), _type
    if _type == "bit-string":
        return ("%i" % lib61850.MmsValue_getBitStringAsInteger(value)), _type
    if _type == "access-error":
        return ("ACCESS ERROR"), _type
    if _type == "float":
        return ("%f" % lib61850.MmsValue_toFloat(value)), _type
    if _type == "generalized-time":
        return ("%u" % lib61850.MmsValue_toUnixTimestamp(value)), _type
    if _type == "integer":
        return ("%i" % lib61850.MmsValue_toInt64(value)), _type
    if _type == "oid":
        return ("OID ERROR"), _type
    if _type == "mms-string":
        return ("%s" % lib61850.MmsValue_toString(value).decode("utf-8")), _type
    if _type == "structure":
        return value, _type
    if _type == "octet-string":
        len = lib61850.MmsValue_getOctetStringSize(value)
        buf = lib61850.MmsValue_getOctetStringBuffer(value)
        # magic cast to convert a swig pointer into a ctypes pointer, the int(buf) works, but why?
        buff = ctypes.cast(buf, ctypes.POINTER(ctypes.c_char))
        # allocate a buffer for the result
        res = bytearray(len)
        # create a pointer to the result buffer
        rptr = (ctypes.c_char * len).from_buffer(res)
        # copy the memory from the swig buffer to the result buffer
        ctypes.memmove(rptr, buff, len)
        return ("%s" % ''.join(format(x, '02x') for x in res)), _type
    if _type == "unsigned":
        return ("%u" % lib61850.MmsValue_toUint32(value)), _type
    if _type == "utc-time":
        return ("%u" % lib61850.MmsValue_getUtcTimeInMs(value)), _type
    if _type == "visible-string":
        return ("%s" % lib61850.MmsValue_toString(value).decode("utf-8")), _type
    if _type == "unknown(error)":
        return ("UNKNOWN ERROR"), _type
    return ("CANNOT FIND TYPE"), _type


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


def isOpen(ip, port):
    '''
    Fungsi untuk checking ip dan port 102 (port default protocol IEC61850)
    requirement : (ip, port) ip: destinasi, port: 102
    return True: Ip terkoneksi dan port 102 terbuka
    return True: Ip terkoneksi dan port 102 tertutup
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        s.connect((ip, int(port)))
        s.shutdown(socket.SHUT_RDWR)
        # print("IP: %s Port: %d Opened" % (ip, port))
        return True
    except:
        # print("IP: %s Port: %d Closed" % (ip, port))
        return False
    finally:
        s.close()


def db_getDB():

    # initialize database
    buff_db_device = db.readDb.device_list_type2(0)
    for db_val in buff_db_device:
        # db_val['id_device']
        # print(db_val)
        connections[db_val['id_device']] = {}
        connections[db_val['id_device']]['host'] = {
            'ip': db_val['ip_address'], 'port': db_val['port_address']}
        connections[db_val['id_device']]['con'] = None

        items[db_val['id_device']] = {}
        items[db_val['id_device']]['object'] = {}
        items[db_val['id_device']]['type'] = []
        items[db_val['id_device']]['alias'] = []

        database[db_val['id_device']] = {}
        database[db_val['id_device']]['master'] = db_val
        database[db_val['id_device']]['rack'] = db_val['rack_location']
        database[db_val['id_device']]['type'] = db_val['type']

        disturbance[db_val['id_device']] = {}
        disturbance[db_val['id_device']]['type'] = db_val['disturbance_type']
        disturbance[db_val['id_device']]['path'] = db_val['iec_file']
        disturbance[db_val['id_device']]['ext'] = []
        disturbance[db_val['id_device']]['strfiles'] = []
        disturbance[db_val['id_device']]['files'] = []

    for relayId in connections:
        buff_db_DR = db.readDb.data_iec_filedr(x=0, id_device=relayId)
        buff_db_item = db.readDb.m_file_iec_read_by_ID(0, relayId)

        if buff_db_DR == None or len(buff_db_DR) == 0 :

            buff_query = f"INSERT INTO data_iec_filedr(id_device, jumlahDR, status, listDR, device_pathDR,fileDR,extensionDR,timeDR) VALUES('"+str(
                relayId)+"', '""','""', '""', '""', '""', '""', '""') "
            buff_db_ret = db.queryData(0, buff_query)
            # print(buff_db_ret)
            disturbance[relayId]['files'] = set()
            disturbance[relayId]['ext'] = []
        else:
            db_Read = db.readDb.data_iec_filedr(0, relayId)
            # print(db_Read)
            disturbance[relayId]['strfiles'] = db_Read[0]['listDR']
            disturbance[relayId]['ext'] = db_Read[0]['extensionDR']
            disturbance[relayId]['files'] = set()

        db_itemConfig2(relayId, buff_db_item)
    # print(disturbance)
    # buff_db_DR = db.readDb.data_iec_filedr(0)
    # print(buff_db_DR)
    # for db_val in buff_db_DR:
    #     disturbance[db_val['id_device']] = {}
    #     disturbance[db_val['id_device']]['type'] = {}
    #     disturbance[db_val['id_device']]['files'] = {}
    #     disturbance[db_val['id_device']]['extension'] = {}
    #     disturbance[db_val['id_device']]['path'] = {}

    buff_db_mesin = db.readDb.m_mesin(0)[0]
    buff_db_network = db.readDb.network(0)[0]
    buff_db_mqtt = db.readDb.network_mqtt(0)[0]
    systems['mesin'] = {'nama_gi': buff_db_mesin['nama_gi'],
                        'kode_mesin': buff_db_mesin['kode_mesin']}

    systems['network'] = {'ipdevice': buff_db_network['iplocal'],
                          'netmask': buff_db_network['netmask'],
                          'prefik': buff_db_network['prefik'],
                          'gateway': buff_db_network['gateway'],
                          'ipserver': buff_db_network['ipserver']}

    systems['mqtt'] = {'broker': buff_db_mqtt['mqtt_server'],
                       'user': buff_db_mqtt['mqtt_username'],
                       'pass': buff_db_mqtt['mqtt_pass'],
                       'port': buff_db_mqtt['mqtt_port']}
    # print(systems)


def db_itemConfig():
    buff_db_object = db.readDb.m_file_iec_read_by_active(0)
    for ied in connections:
        for v in buff_db_object:
            if ied == v['id_device']:
                if v["active"] == 1:

                    fc_split = v["item_id"].split("$")
                    item_id = v["item_id"].replace("$"+fc_split[1], "")

                    itemID_read = v["domain_id"]+"/"+item_id.replace("$", ".")
                    itemID_mqtt = v["domain_id"]+"/"+item_id
                    itemID_FC = _FC(fc_split[1])
                    itemID_alias = v['alias']

                    items[v['id_device']]['object'][itemID_read] = {
                        'itemRead': itemID_read,
                        'itemMqtt': itemID_mqtt,
                        'itemFC': itemID_FC,
                        'itemType': v["data_type"],
                        'itemAlias': itemID_alias,
                    }


def db_itemConfig2(idDevice, buff_db):
    for v in buff_db:
        if idDevice == v['id_device']:
            if v["active"] == 1:

                fc_split = v["item_id"].split("$")
                item_id = v["item_id"].replace("$"+fc_split[1], "")

                itemID_read = v["domain_id"]+"/"+item_id.replace("$", ".")
                itemID_mqtt = v["domain_id"]+"/"+item_id
                itemID_FC = _FC(fc_split[1])
                itemID_alias = v['alias']

                items[v['id_device']]['object'][itemID_read] = {
                    'itemRead': itemID_read,
                    'itemMqtt': itemID_mqtt,
                    'itemFC': itemID_FC,
                    'itemType': v["data_type"],
                    'itemAlias': itemID_alias,
                }


def iec61850_getIED(id_device):
    id_device = str(id_device)
    # if port == "" or port == None:
    #     port = 102

    # if host == None:
    #     logger.error("missing hostname")
    #     return -1

    # tupl = host + ":" + str(port)
    if id_device in connections and connections[id_device]["con"] != None:
        if isOpen(connections[id_device]['host']['ip'], connections[id_device]['host']['port']):
            # we have a connection and a model
            return 0
        # if not connections[id_device]["model"]:
        #     con = self.connections[tupl]["con"]
        #     model = iec61850client.discovery(con)
        #     if model:  # if model is not empty
        #         # store the model
        #         self.connections[tupl]["model"] = model
        #         return 0
        #     else:
        #         # we could not perform a discovery, so remove connection
        #         lib61850.IedConnection_destroy(con)
        #         self.connections[tupl]["con"] = None
        #         return -1
        else:
            lib61850.IedConnection_destroy(connections[id_device]["con"])
            connections[id_device]["con"] = None
            return -1

    if not id_device in connections:
        connections[id_device]["con"] = None

    if isOpen(connections[id_device]['host']['ip'], connections[id_device]['host']['port']):
        # print(connections[id_device]['host']['ip'])
        hostIP = connections[id_device]['host']['ip']
        portIP = int(connections[id_device]['host']['port'])
        con = lib61850.IedConnection_create()
        error = lib61850.IedClientError()
        lib61850.IedConnection_connect(con, ctypes.byref(
            error), hostIP, portIP)
        if error.value == lib61850.IED_ERROR_OK:
            # store the active connection
            connections[id_device]["con"] = con
            # print(connections)
            return 0
        else:
            lib61850.IedConnection_destroy(con)
            connections[id_device]["con"] = None
            return -1
    else:
        return -1


def iec61850_read_object(id_device: int, item: str, item_FC: int) -> tuple[int | float | bool, str]:
    '''
    Fungsi untuk membaca data dari item IEC61850
    con     -> koneksi IEC61850 dari dictionary connection
    item    -> item object yang dibaca (dari DB)
    item_FC -> functional constrain atau tipe data dari item (parsing DB)

    return tuple list (hasil nilai pembacaan, type data hasil pembacaan)
    '''
    id_device = str(id_device)
    err = iec61850_getIED(id_device)
    # print(connections[id_device]['con'])
    # print(connections)
    if err == 0:
        con = connections[id_device]['con']
        if not con:
            logger.error("no valid connection")
            return None, None

        # item_FC = _FC(item_FC)
        error = lib61850.IedClientError()
        # print(item, item_FC)
        value = lib61850.IedConnection_readObject(
            con, ctypes.byref(error), item, item_FC)

        if error.value == 0:
            read_value, read_type = _printValue(value)
            logger.debug("Value '%s' type %s from item %s" %
                         (str(read_value), read_type, item))
            lib61850.MmsValue_delete(value)
            err = 0
            return read_value, read_type
        else:
            logger.error("could not read DA: %s from device" % item)
            err = error.value
            return None, None

    else:
        logger.error("no connection to IED: %s:%s" %
                     (connections[id_device]['host']['ip'], connections[id_device]['host']['port']))
        return None, None


def iec61850_readFile_directory(id_device: int, directory: str) -> tuple[int | float | bool, str]:
    '''
    Fungsi untuk membaca file pada directory IEC61850
    item        -> item object yang dibaca (dari DB)
    directory   -> directory disturbance IEC61850 pada relay

    return tuple list (hasil nilai pembacaan, type data hasil pembacaan)
    '''
    id_device = str(id_device)
    err = iec61850_getIED(id_device)
    if err == 0:
        con = connections[id_device]['con']
        if not con:
            logger.error("no valid connection")
            return None

        error = lib61850.IedClientError()
        rootDirectory = lib61850.IedConnection_getFileDirectory(
            con, error, directory)
        # print(directory)
        if error.value == lib61850.IED_ERROR_OK:
            directoryEntry = lib61850.LinkedList_getNext(rootDirectory)
            # listingFile = []
            listFile = []  # set()
            newPath = ''
            extensionList = []
            while directoryEntry:
                entry = ctypes.cast(lib61850.LinkedList_getData(
                    directoryEntry), lib61850.FileDirectoryEntry)
                file_name = lib61850.FileDirectoryEntry_getFileName(
                    entry).decode("UTF-8")
                file_modified = lib61850.FileDirectoryEntry_getLastModified(
                    entry)
                # logging.debug("name: %s modified: %s" %
                #               (file_name, file_modified))
                # print("name: %s modified: %s" %
                #       (file_name, file_modified))

                # newPath = os.path.split(file_name)
                # parsePath = pathlib.Path(file_name)
                # logger.debug("path: %s, file: %s, ext: %s, time: %i" %
                #              (parsePath.parent, parsePath.stem, parsePath.suffix, file_modified))
                # listingFile.append([file_name, file_modified])
                # for v in extension_file_dr:
                #     if v in file_name and "h.zip" not in file_name:
                #         extensionList.append(v)
                #         # listFile.append([newPath[1], file_modified])
                #         listFile.add((directory+newPath[0], newPath[1], parsePath.suffix))
                path = os.path.split(file_name)
                file_names, file_ext = os.path.splitext(file_name)
                
                file_names = PurePosixPath(file_names)
                file_names = str(Path(file_names))
                
                for v in extension_file_dr:
                    if v in file_name:
                        # listFile.add(file_name)
                        listFile.append([file_names, file_ext])

                directoryEntry = lib61850.LinkedList_getNext(directoryEntry)
            lib61850.LinkedList_destroy(directoryEntry)

            # print(listFile)

            # for index, v in enumerate(listFile):
            #     # print(v)
            #     if "h.zip" in v[0]:
            #         # print("TERDAPAT HZIP")
            #         listingFile.pop(index)

            # logger.debug("path: %-10s, file: %s, ext: %s, time: %i" %
            #              (path[0], listFile[0], "cfg", listFile[1]))
            # if not newPath:
            #     logger.error("error get file directory")
            #     err = -1
            #     return None, None
            # else:
            # return path[0], listFile
            return listFile

        else:
            logger.error("error get list file directory, code: %d" %
                         (error.value))
            err = error.value
            # return None, None
            return None

    else:
        logger.error("no connection to IED: %s:%s" %
                     (connections[id_device]['host']['ip'], connections[id_device]['host']['port']))
        # return None, None
        return None


def iec61850_downloadFile(id_device: int, filePath: str) -> tuple[int | float | bool, str]:
    '''
    Fungsi untuk download file pada directory IEC61850
    item        -> item object yang dibaca (dari DB)
    fileDir     -> download file via IEC61850

    return tuple list (hasil nilai pembacaan, type data hasil pembacaan)
    '''
    #directorySavedFile = 'D:\\Documents\\VSCode\\IEC61850\\pylibiec61850\\libiec61850_client\\DR_FILES\\'
    directorySavedFile = "/var/www/html/dms_setting/assets/api/file_dr/"
    if filePath[0] != "/":
        filePath = '/'+filePath

    fileNamePath = pathlib.Path(filePath)
    fileName = fileNamePath.stem
    fileExt = fileNamePath.suffix
    # print("fileNamePath: ", fileNamePath, "fileName: ",
    #       fileName, "fileExt: ", fileExt)

    id_device = str(id_device)
    err = iec61850_getIED(id_device)
    if err == 0:
        con = connections[id_device]['con']
        if not con:
            logger.error("no valid connection")
            return -1

        dirName = os.path.join(directorySavedFile, fileName)
        if not os.path.exists(dirName):
            os.mkdir(dirName)

        # print("DIRNAME: ", dirName, "FILENAME: ",
        #       fileName, "FILEEXT: ", fileExt)
        localPath = os.path.join(dirName, fileName+fileExt)
        # print(localPath)
        open(localPath, "w").close()  # create an empty file

        # update file latest
        newfile = dirName+"\\"
        localFileBytes = bytes(localPath.encode('utf-8'))
        # print(localFileBytes)
        # savePath = pathlib.Path(filePath)

        error = lib61850.IedClientError()
        handler = lib61850.IedClientGetFileHandler(_getFileHandler)
        lib61850.IedConnection_getFile(
            con, error, filePath, handler, ctypes.c_char_p(localFileBytes))
        if error.value == lib61850.IED_ERROR_OK:
            return 0

        else:
            logger.error("error download file")
            print(error.value)
            return -1

    else:
        logger.error("no connection to IED: %s:%s" %
                     (connections[id_device]['host']['ip'], connections[id_device]['host']['port']))
        return -1


def convert_strFiletoSet(strFile, delimiter):
    if not strFile:

        return set()
    else:
        if '\\\\' in strFile:
            strFile = strFile.replace('\\\\', '\\')
        return set(strFile.split(str(delimiter)))


def convert_setToStrFile(strFile, delimiter=str):
    str_buff = delimiter.join(strFile)
    if "\\" in str_buff:
        str_buff = str_buff.replace('\\', '\\\\')
    return str_buff


def pack_buildZip(dirName):

    # print(dirName)
    if "\\" in dirName:
        buff = dirName.split("\\")
        dirName = buff[-1]
    elif "/" in dirName:
        buff = dirName.split("/")
        dirName = buff[-1]
    # dirName = "/"+dirName

    # rootDir = '/home/pi/dms/DMSv1.2/IEC61850/DR_FILES'
    #rootDir = 'D:\\Documents\\VSCode\\IEC61850\\pylibiec61850\\libiec61850_client\\DR_FILES\\'
    rootDir = "/var/www/html/dms_setting/assets/api/file_dr/"
    filesDir = rootDir + dirName
    # print(filesDir)
    with ZipFile(filesDir + '.zip', 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk(filesDir):
            for filename in filenames:
                absname = os.path.abspath(os.path.join(filesDir, filename))
                # print(absname)
                # menghilangkan + 1 dari length rootDir
                arcname = absname[len(rootDir):]
                # print(arcname)
                # print('zipping %s as %s' % (os.path.join(filesDir, filename),
                #                             arcname))
                zipObj.write(absname, arcname,
                             compress_type=zipfile.ZIP_DEFLATED)
        zipObj.close()
    return filesDir+".zip"


def send_MQTTData(topic: str, message: str | dict):
    '''
    Fungsi untuk send data ke MQTT
    topic   -> topic mqtt
    message -> payload mqtt

    return  -> None
    '''
    try:
        mqtt_publish.single(hostname=systems['mqtt']['broker'],
                            auth={
                                'username': systems['mqtt']['user'], 'password': systems['mqtt']['pass']},
                            port=systems['mqtt']['port'],
                            topic=str(topic),
                            payload=str(message))
    except:
        logger.error("cannot send to MQTT")


def send_DFRFailADD(id_device, DFRPath):
    nowTime = datetime.now()
    stringTime = nowTime.strftime("%d/%m/%Y %H:%M:%S")

    url = 'http://'+systems['network']['ipserver']+'/mel/dms/fail/add'

    directory, filename = os.path.split(DFRPath)
    DFRName, extension = os.path.splitext(filename)

    try:
        comtradeFolder = DFRPath.replace(".zip", "")
        ret_comtrade = dfr_parse.getDFRvalue(comtradeFolder)
        ret_comtrade = ret_comtrade[1]
    except:
        ret_comtrade = "-"
    # print(DFRPath)

    d = {"machineCode": systems['mesin']["kode_mesin"],
         "relayId": str(id_device),
         "lokasi": systems['mesin']["nama_gi"]+" "+database[id_device]['rack'],
         "status": "DFR Available",
         "namaFile": DFRName,
         "waktu": stringTime,
         "flag": 0,
         "type": database[id_device]['type'],
         "portType": "IEC61850",
         "portNumber": 0,
         "dr_metering": "-",
         "dr_event": ret_comtrade
         }

    print(d)

    try:
        r = requests.post(
            url, data=d, timeout=2)
        r.raise_for_status()
    # except:
    #     logger.error("cannot send to Server")
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)


def send_DFRUploadFile(id_device, DFRPath):

    nowTime = datetime.now()
    stringTime = nowTime.strftime("%d/%m/%Y %H:%M:%S")

    url = 'http://'+systems['network']['ipserver']+'/mel/dms/notif'

    fileZip = {'myfile': open(DFRPath, 'rb')}

    directory, filename = os.path.split(DFRPath)
    DFRName, extension = os.path.splitext(filename)

    d = {"status": "DFR Available",
         "file_name": DFRName,
         "machineCode": systems['mesin']["kode_mesin"],
         "lokasi": systems['mesin']["nama_gi"]+" "+database[id_device]['rack'],
         "namaFile": DFRName,
         "waktu": stringTime,
         "flag": 0,
         "type": database[id_device]['type'],
         "portType": "IEC61850",
         "relayId": str(id_device),
         "portNumber": 0
         }

    print(d)

    try:
        r = requests.post(url,  data=d, files=fileZip, verify=False, timeout=2)
        # print(r)
        r.raise_for_status()
        if r.status_code != 200:
            print('sendErr: '+r.url)
            db.insertDb.m_fileDR_temp(2,id_device,str(id_device),str(d),str(0),DFRName)
        else:
            print(r.text)
            db.insertDb.m_fileDR_temp(2,id_device,str(id_device),str(d),str(1),DFRName)
    # except:
    #     logger.error("cannot send to Server")
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
        db.insertDb.m_fileDR_temp(0,'2',str(id_device),str(d),str(0),DFRName)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
        db.insertDb.m_fileDR_temp(0,'2',str(id_device),str(d),str(0),DFRName)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
        db.insertDb.m_fileDR_temp(0,'2',str(id_device),str(d),str(0),DFRName)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)
        db.insertDb.m_fileDR_temp(0,'2',str(id_device),str(d),str(0),DFRName)


def drfile_checking(drfile_list):

    if drfile_list:
        buff_dfrExtensionList = ()
        buff_dfrNameList = []
        buff_dfrNameFinal = []
        buff_dfrExtFinal = []
        buff_dfrDirList = []
        buff_dfrNameList = drfile_list

        # buff_file_names = set()
        # buff_extension = set()
        # print(drfile_list)
        for file_info in drfile_list:
            # print(file_info)
            file_name = file_info[1]
            dir_file = file_info[0]

            file_name_only = dir_file  # .rsplit('.', 1)[0]
            extension = file_name.split('.')[-1]
            # print(file_name_only)
            # print(extension)

            if file_name_only not in buff_dfrNameFinal:
                buff_dfrNameFinal.append(file_name_only)
                buff_dfrDirList.append(dir_file)
            if extension not in buff_dfrExtFinal:
                buff_dfrExtFinal.append(extension)

        # print(buff_dfrNameList)
        # print(buff_dfrExtFinal)
        # print(buff_dfrNameFinal)
        # print(buff_dfrDirList)

        return buff_dfrNameFinal, buff_dfrExtFinal
    return [], []


# def pollFirst():
#     for ied in connections:
#         # print("pollFirst() in for loop : ",
#         #       iec61850_readFile_directory(ied, "/"))
#         bufferFile = iec61850_readFile_directory(
#             ied, testFolder)
#         # print(bufferFile)
#         if bufferFile != None:
#             print(bufferFile)
#             disturbance[ied]['files'], disturbance[ied]['ext'] = drfile_checking(
#                 bufferFile)
#             # print(disturbance[ied])


fileList = set()


def poll():
    global time_3s
    global time_60s
    kodeMesin = systems['mesin']['kode_mesin']

    if time.time() - time_3s > 1:
        for ied in connections:
            err = iec61850_getIED(ied)
            if err == 0:

                bufferFile = iec61850_readFile_directory(
                    ied, disturbance[ied]['path'])
                bufferFiles, bufferExt = drfile_checking(bufferFile)
                newFiles = 0
                
                if bufferFiles != None:
                    bufferFiles = set(bufferFiles)
                    print(bufferFiles)
                    # set_Files = fileList
                    set_Files = convert_strFiletoSet(
                        disturbance[ied]['strfiles'], "|")
                    if len(set_Files) != 0:
                        prevBufferFiles = set_Files
                        # prevBufferFiles = set(disturbance[ied]['files'])
                    else:
                        prevBufferFiles = set()

                    # print("from DB prevBufferFiles: ", prevBufferFiles)
                    # print("Pembacaan sekarang BufferFiles: ", bufferFiles)
                    # print(bufferExt)

                    newFiles = bufferFiles.difference(prevBufferFiles)

                    if newFiles:
                        err = 0
                        list_newFile = set()
                        for itemFile in newFiles:
                            retries = 0
                            for ext in bufferExt:
                                while retries < 3:
                                    # buffFilePath = "/" + \
                                    #     pathlib.PurePosixPath(
                                    #         itemFile).as_posix()+"."+ext
                                    buffFilePath = disturbance[ied]['path'] + \
                                        itemFile+"."+ext
                                    # print("Starting Download File : ",
                                    #       buffFilePath)
                                    logging.debug(
                                        "Downloading file %s" % (buffFilePath))
                                    download = iec61850_downloadFile(
                                        ied, buffFilePath)
                                    if download != 0:
                                        err = -1
                                        retries += 1
                                    else:
                                        err += 0
                                        retries = 3
                                retries = 0

                            if err == 0:

                                str_folderFilePath = pathlib.Path(
                                    itemFile).stem

                                str_zipName = pack_buildZip(str_folderFilePath)
                                print(str_zipName)
                                #prevBufferFiles.add(itemFile)
                                prevBufferFiles.add(itemFile)
                                # list_newFile.add(itemFile)

                                #if isOpen(systems['network']['ipserver'], int(80)):
                                #send_DFRFailADD(ied, itemFile)
                                send_DFRUploadFile(ied, str_zipName)
                                #else:
                                 #   logger.error(
                                  #      "value: None not send to MQTT")
                                # ret_StrDBFileDR = convert_setToStrFile(
                                #     prevBufferFiles, "|")
                                #list_newFile.add(itemFile)
                        prevBufferFiles.clear()
                        prevBufferFiles = bufferFiles

                        #print("prevBufferFiles", prevBufferFiles)
                        ret_StrDBFileDR = convert_setToStrFile(
                            prevBufferFiles, "|")

                        disturbance[ied]['strfiles'] = ret_StrDBFileDR
                        db.writeDb.update_data_iec_filedr(
                            0, ied, ret_StrDBFileDR, 0)

                        # print(disturbance[ied]['strfiles'])

                for item in items[ied]['object']:
                    if items[ied]['object'][item]['itemType'] == 'boolean':
                        itemFC = items[ied]['object'][item]['itemFC']
                        itemAlias = items[ied]['object'][item]['itemAlias']
                        itemMqtt = items[ied]['object'][item]['itemMqtt']

                        ret_val, ret_type = iec61850_read_object(
                            ied, item, itemFC)
                        if ret_val != None:
                            mqtt_payload = {"alias": itemAlias,
                                            "val": ret_val, "dataType": ret_type}
                            mqtt_topic = f"DMS/{kodeMesin}/IEC61850/{ied}/{itemMqtt}/"
                            mqtt_payload = str(mqtt_payload).replace("'", "\"")
                            if isOpen(systems['mqtt']['broker'], systems['mqtt']['port']):
                                send_MQTTData(mqtt_topic, mqtt_payload)
                            else:
                                logger.error("value: None not send to MQTT")
                        else:
                            logger.error("value: None not send to MQTT")

            else:
                logger.error("no connection to IED: %s:%s" %
                             (connections[ied]['host']['ip'], connections[ied]['host']['port']))

        time_3s = time.time()

    if time.time() - time_60s > 2:
        for ied in connections:
            err = iec61850_getIED(ied)
            if err == 0:
                for item in items[ied]['object']:
                    if items[ied]['object'][item]['itemType'] == 'float':
                        itemFC = items[ied]['object'][item]['itemFC']
                        itemAlias = items[ied]['object'][item]['itemAlias']
                        itemMqtt = items[ied]['object'][item]['itemMqtt']

                        ret_val, ret_type = iec61850_read_object(
                            ied, item, itemFC)
                        if ret_val != None:
                            mqtt_payload = {"alias": itemAlias,
                                            "val": ret_val, "dataType": ret_type}
                            mqtt_topic = f"DMS/{kodeMesin}/IEC61850/{ied}/{itemMqtt}/"
                            mqtt_payload = str(mqtt_payload).replace("'", "\"")
                            send_MQTTData(mqtt_topic, mqtt_payload)
                        else:
                            logger.error("value: None not send to MQTT")
            else:
                logger.error("no connection to IED: %s:%s" %
                             (connections[ied]['host']['ip'], connections[ied]['host']['port']))

        time_60s = time.time()


db_getDB()

while True:
    poll()
    lib61850.Thread_sleep(100)
