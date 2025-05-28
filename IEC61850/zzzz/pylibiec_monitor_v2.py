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
# import dfr_parse
import os
import socket
import logging

logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    level=logging.DEBUG)
# note the `logger` from above is now properly configured
logger = logging.getLogger(__name__)


DEBUG = False  # """untuk percobaan dengan server localhost"""
DRSAVE_PATH = 'D:\\Documents\\VSCode\\IEC61850\\pylibiec61850\\libiec61850_client\\'


if DEBUG:
    dataDevice = ['127.0.0.1']
else:
    DBdataMeasurement = db.readDb.m_file_iec_read_by_active(0)
    DBdataDevices = db.readDb.device_list(1)
    DBdataNetwork = db.readDb.network(0)
    DBdataMMesin = db.readDb.m_mesin(0)
    # dataDRIEC = db.
dataDevice = []
dbMqtt = db.readDb.network_mqtt(0)
# print(dbMqtt)

for v in DBdataDevices:
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

con = []
conn = {}
model = []
object_read = []
object_FC = []
file_list = []
rack_location = []
type_relay = []
name_alias = []
disturbanceType = []
iecfolder = []
object_type = []

db_fileList = []
listfileArr = []

network_ipserver = DBdataNetwork[0]['ipserver']
mesin_mesin = DBdataMMesin[0]['kode_mesin']
mesin_namaGi = DBdataMMesin[0]['nama_gi']

# disturbanceType = DBdataDevices[0]['disturbance_type']
# print(disturbanceType)

client = None

extension_file_dr = [".cfg", ".dat", ".hdr", ".cev", ".txt", ".inf",
                     ".CFG", ".DAT", ".HDR", ".CEV", ".TXT", ".INF",
                     ".zip", ".ZIP"]
mqttRetry = 0


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
    # print("received %i bytes for file: %s" % (bytesRead, filename))
    if bytesRead > 0:
        with open(filename, "ab") as fp:
            bytesbuffer = ctypes.string_at(buffer, bytesRead)
            fp.write(bytesbuffer)  # append bytes to file
    return True


# def ClientFile61850_dir():
def ClientFile61850_dir(con, iec_dir):
    counterFile = 0
    listFile = []
    # for i in range(0, max_client):
    #   if error[i]['error'].value == lib61850.IED_ERROR_OK:
    error_file = lib61850.IedClientError()
    rootDirectory = lib61850.IedConnection_getFileDirectory(
        con, error_file, iec_dir)
    if error_file.value != lib61850.IED_ERROR_OK:
        print("Error retrieving file directory")
        return None, None

    else:
        directoryEntry = lib61850.LinkedList_getNext(rootDirectory)

        while directoryEntry:

            entry = ctypes.cast(lib61850.LinkedList_getData(
                directoryEntry), lib61850.FileDirectoryEntry)

            file_name = lib61850.FileDirectoryEntry_getFileName(
                entry).decode("UTF-8")
            file_size = lib61850.FileDirectoryEntry_getFileSize(entry)
            file_modified = lib61850.FileDirectoryEntry_getLastModified(
                entry)
            # print("name: %s size: %d modified: %s" % (file_name, file_size, file_modified))
            path = os.path.split(file_name)
            for v in extension_file_dr:
                if v in file_name:
                    listFile.append([path[1], file_modified])
            directoryEntry = lib61850.LinkedList_getNext(directoryEntry)
        for index, v in enumerate(listFile):
            # print(v)
            if "h.zip" in v[0]:
                # print("TERDAPAT HZIP")
                listFile.pop(index)

        lib61850.LinkedList_destroy(directoryEntry)
        # print(listFile)
        return path[0], listFile
    # else:
    #    print("connection issue")


def ClientFile61850_get(con, fileNameAsal):
    # update file latest
    rootDir = "/home/pi/dms/DMSv1.2/IEC61850/DR_FILES"
    dirName = fileNameAsal[:-4]
    dirName = rootDir+dirName
    if not os.path.exists(dirName):
        os.mkdir(dirName)
    # update file latest

    handler = lib61850.IedClientGetFileHandler(_getFileHandler)
    if 'COMTRADE/' in fileNameAsal:
        localfilename = fileNameAsal.replace('COMTRADE/', '')
    elif '\\' in fileNameAsal:
        localfilename = fileNameAsal.replace('\\', '')

    open(localfilename, "w").close()  # create an empty file
    error_getfile = lib61850.IedClientError()

    # update file latest
    newfile = dirName+"\\"+localfilename
    fileNameOutput = bytes(newfile.encode('utf-8'))
    print(fileNameOutput)
    # update file latest

    for i in range(max_client):
        lib61850.IedConnection_getFile(
            con[i]['con'], error_getfile, fileNameAsal, handler, ctypes.c_char_p(fileNameOutput))
        if error_getfile.value != lib61850.IED_ERROR_OK:
            print("Failed to get file!")

# lama
# def build_zip(dirName):
#     dirName = dirName.replace('COMTRADE/', '')

# #    json_names = {f.stem for f in p.iterdir() if f.suffix == '.json'}
# #    nii_names = {Path(f.stem).stem for f in p.iterdir() if f.suffixes == ['.nii', '.gz']}
# #    for file_name in json_names & nii_names:
# #        json_path = p / (file_name + '.json')
# #        nii_path = p / (file_name + '.nii.gz')

#     iecdirname = '/home/pi/Desktop/DMSv1.2/IEC61850/zipDR/'
#     with ZipFile('/home/pi/Desktop/DMSv1.2/IEC61850/zipDR/' + dirName + '.zip', 'w') as zipObj:
#         zipObj.write(dirName+".dat", compress_type=zipfile.ZIP_DEFLATED)
#         zipObj.write(dirName+".cfg", compress_type=zipfile.ZIP_DEFLATED)
#         zipObj.write(dirName+".hdr", compress_type=zipfile.ZIP_DEFLATED)

#     return iecdirname + dirName + '.zip'

#     if not os.path.exists('/home/pi/Desktop/DMSv1.2/IEC61850/' + dirName):
#         print("Folder ", dirName,  " tidak tersedia ")
#     else:
#         shutil.rmtree('/home/pi/Desktop/DMSv1.2/IEC61850/'+dirName)
#         print("Folder telah dihapus")


def Client61850_config():

    for i in range(0, max_client):
        hostname.append(
            {'id': dataDevice[i]["id_device"],
                'hostname': dataDevice[i]["ip_address"]})
        # ipserver[i] = DBdataMeasurement[i]['ipserver']
        tcpport.append(
            {'id': dataDevice[i]["id_device"],
                'port': dataDevice[i]["port_address"]})

        con.append(
            {'id': dataDevice[i]["id_device"],
                'con': None})

        object_read.append(
            {'id': dataDevice[i]["id_device"]})

        object_FC.append(
            {'id': dataDevice[i]["id_device"]})

        alias_monit.append(
            {'id': dataDevice[i]["id_device"]})

        object_type.append(
            {'id': dataDevice[i]["id_device"]})

        alias_name.append(
            {'id': dataDevice[i]["id_device"]})

        rack_location.append(
            {'id': dataDevice[i]["rack_location"]})

        type_relay.append(
            {'id': dataDevice[i]["type"]})

        iecfolder.append(
            {'id': dataDevice[i]["iec_file"]})

        disturbanceType.append(
            {'type': dataDevice[i]["disturbance_type"]})
        # print(disturbanceType)

    for i in range(0, max_client):
        buff_con = lib61850.IedConnection_create()
        buff_error = lib61850.IedClientError()
        lib61850.IedConnection_connect(
            buff_con, buff_error, hostname[i]['hostname'], int(tcpport[i]['port']))
        if buff_error.value == lib61850.IED_ERROR_OK:
            print("IEC61850 Connection OK in %s:%s" % (
                hostname[i]['hostname'], tcpport[i]['port']))
            con[i]['con'] = buff_con

        else:
            print("IEC61850 Connection error in %s:%s" % (
                hostname[i]['hostname'], tcpport[i]['port']))
            lib61850.IedConnection_destroy(buff_con)


def CLient61850_itemConfig():
    # for k,v in DBdataMeasurement.items():
    #     if v in object_read['id']
    for v in DBdataMeasurement:
        # if v in object_read['id']
        if v["active"] == 1:
            for i in range(len(object_read)):
                if v['id_device'] == object_type[i]['id']:
                    if not 'object_type' in object_type[i]:
                        object_type[i]['object_type'] = []
                    object_type[i]['object_type'].append(v['data_type'])

                if v['id_device'] == alias_monit[i]['id']:
                    if not 'alias' in alias_monit[i]:
                        # print('key obj')
                        # else:
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
                    if not 'obj' in object_read[i] or not 'obj' in object_FC[i]:
                        #     print('key obj')
                        # else:
                        object_read[i]['obj'] = []
                        object_read[i]['itemID'] = []
                        object_FC[i]['obj'] = []

                    object_read[i]['obj'].append(
                        v["domain_id"]+"/"+item_id.replace("$", "."))
                    object_read[i]['itemID'].append(
                        v["domain_id"]+"/"+item_id)
                    object_FC[i]['obj'].append(_FC(fc_split[1]))
                    # j += 1


def CLient61850_monitoringRead(con, hostname, error, object_read, object_fc):
    if (error.value == lib61850.IED_ERROR_OK):
        value = lib61850.IedConnection_readObject(con, ctypes.byref(
            error), object_read, object_fc)
        # print(object_read)
        if (error.value == lib61850.IED_ERROR_OK):
            val, types = iec61850client.printValue(value)
            lib61850.MmsValue_delete(value)
            return val, types
        lib61850.MmsValue_delete(value)
        return 0, 0
    else:
        print("Failed to connect to %s:%s" % (hostname, "102"))
        # Client61850_checkConnect(hostname, 102, con, error)
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
        errors = lib61850.IedClientError()
        lib61850.IedConnection_release(con[i]['con'], errors)
        if errors.value != lib61850.IED_ERROR_OK:
            print("Release returned error: %d" % errors.value)
        else:
            while (lib61850.IedConnection_getState(con[i]['con']) != lib61850.IED_STATE_CLOSED):
                lib61850.Thread_sleep(10)

        lib61850.IedConnection_destroy(con[i]['con'])


def Client61850_connection(con, error, hostname, port):
    # for i in range(0, maxClient):
    # if isOpen(hostname, 102):
    lib61850.IedConnection_connect(
        con, ctypes.byref(error), hostname, int(port))
    if (error.value == lib61850.IED_ERROR_OK):
        print("IEC61850 Connection OK in %s:%s" % (
            hostname, port))
    else:
        print("IEC61850 Connection error in %s:%s" % (
            hostname, port))


def isOpen(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
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
    # if not response:
#    lib61850.IedConnection_connect(
#        con, ctypes.byref(error), host, int(port))
#    if (error.value == lib61850.IED_ERROR_OK):
#        print("IEC61850 Connection OK in %s:%s" % (
#            host, port))
#    else:
#        print("IEC61850 Connection error in %s:%s" % (
#            host, port))
#    else:
#        if (error.value == lib61850.IED_ERROR_OK):
#            print("IEC61850 Connection OK in %s:%s" % (
#                host, port))
#        else:
#            print("IEC61850 Connection error in %s:%s and Reconnecting" % (
#                host, port))
#            lib61850.IedConnection_connect(
#                con, ctypes.byref(error), host, int(port))


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


def ClientFile61850_getFile(con, fileNameAsal, directory):
    # create folder
    print(fileNameAsal)
    dirName = ''
    localfilename = ''
    #rootDir = DRSAVE_PATH+'DR_FILES'
    rootDir = "/home/pi/dms/DMSv1.2/IEC61850/DR_FILES"

#    if "COMTRADE" in fileNameAsal:
#        dirName = fileNameAsal.replace("COMTRADE", "")
#        print(dirName)
#        localfilename = dirName
#        dirName = dirName[:-4]
#    else:
#        dirName = fileNameAsal[:-4]
#        localfilename = fileNameAsal
#    dirName = rootDir+dirName

    if "\\" in fileNameAsal:
        buff = fileNameAsal.split("\\")
        dirName = buff[-1]
        localfilename = dirName
        dirName = dirName[:-4]
    elif "/" in fileNameAsal:
        buff = fileNameAsal.split("/")
        dirName = buff[-1]
        localfilename = dirName
        dirName = dirName[:-4]
    else:
        dirName = fileNameAsal[:-4]
        localfilename = fileNameAsal
    dirName = rootDir+"/"+dirName
    print(dirName)

    if not os.path.exists(dirName):
        os.mkdir(dirName)

    handler = lib61850.IedClientGetFileHandler(_getFileHandler)
    # localfilename = fileNameAsal.replace('\\', '')
    localfilename = localfilename.replace('/', '')
    open(dirName+"/"+localfilename, "w").close()  # create an empty file
    # print(dirName+"\\"+localfilename)
    error_getfile = lib61850.IedClientError()

    newfile = dirName+"/"+localfilename
    fileNameOutput = bytes(newfile.encode('utf-8'))
    # print(fileNameOutput)

    # lib61850.IedConnection_getFile(
    #     con, error_getfile, directory+fileNameAsal, handler, ctypes.c_char_p(fileNameOutput))
    # if error_getfile.value != lib61850.IED_ERROR_OK:
    #     print("Failed to get file!")

    # tambahan 02 juni 2024
    print("DIRECTORY: ", directory)
    print("FILENAME: ", fileNameAsal)
    # dirs = os.path.join(directory, fileNameAsal)
    dirs = directory+"/"+fileNameAsal
    # dirs = "\\"+dirs
    print("GABUNGAN: ", dirs)

    try:
        lib61850.IedConnection_getFile(
            con, error_getfile, dirs, handler, ctypes.c_char_p(fileNameOutput))
        # '''directory+fileNameAsal'''
        if error_getfile.value != lib61850.IED_ERROR_OK:
            print("Failed to get file!")
            return -1
        else:
            print("FILE NAME OUTPUT UNTUK EXTRACT", newfile)

            # print(directory+FileFinal+e)
            if ".zip" in newfile:
                if os.path.isfile(newfile):
                    with zipfile.ZipFile(newfile, 'r') as zip_ref:
                        zip_ref.extractall(newfile.replace(localfilename, ""))
                    os.remove(newfile)
                else:
                    print("FILE NO EXIST")
            return 0
    except:
        return -1
        print("CANNOT GET FILE")
    # tambahan 02 juni 2024


def newFileMechanism(conn, fileList, directory):
    if file_list or file_list != None:
        # sorting
        listFileNew = sorted(
            fileList, key=lambda fileList: fileList[1], reverse=True)
        # listFileNew = listfile
        FileFinal = listFileNew[0][0]
        for e in extension_file_dr:
            if e in FileFinal:
                print(e)
                FileFinal = FileFinal.replace(e, "")
        print(FileFinal)

        ExtensionFinal = []
        for v in listFileNew:
            for e in extension_file_dr:
                if FileFinal+e in v[0]:
                    ExtensionFinal.append(e)
        print(ExtensionFinal)
        for e in ExtensionFinal:
            ClientFile61850_getFile(conn, FileFinal+e, directory)
        return FileFinal, ExtensionFinal
    else:
        print("FILE LIST NONE")
        return [None, None]


def newFileMechanism(conn, fileList, directory):
    if file_list or file_list != None:
        # sorting
        listFileNew = sorted(
            fileList, key=lambda fileList: fileList[1], reverse=True)
        # listFileNew = listfile
        FileFinal = listFileNew[0][0]
        for e in extension_file_dr:
            if e in FileFinal:
                print(e)
                FileFinal = FileFinal.replace(e, "")
        print(FileFinal)

        ExtensionFinal = []
        for v in listFileNew:
            for e in extension_file_dr:
                if FileFinal+e in v[0]:
                    ExtensionFinal.append(e)
        print(ExtensionFinal)
        for e in ExtensionFinal:
            ClientFile61850_getFile(conn, FileFinal+e, directory)
        return FileFinal, ExtensionFinal
    else:
        print("FILE LIST NONE")
        return [None, None]


def newFileMechanismNew(conn, prevFileList, newfileList, directory, extension):
    if newfileList or newfileList != None or prevFileList or prevFileList != None:
        newfileList = newfileList.split("|")
        prevFileList = prevFileList.split("|")
        extensionList = extension.split("|")
        extensionList = [str("."+g) for g in extensionList]
        # print(prevFileList)
        # print(newfileList)
        # sorting
        newFileDownload = []
        for new in newfileList:
            if new not in prevFileList:
                newFileDownload.append(new)
        # print(newFileDownload)
        # listFileNew = sorted(
        #     fileList, key=lambda fileList: fileList[1], reverse=True)
        # # listFileNew = listfile
        # FileFinal = listFileNew[0][0]
        # for e in extension_file_dr:
        #     if e in FileFinal:
        #         print(e)
        #         FileFinal = FileFinal.replace(e, "")
        # print(FileFinal)

        # ExtensionFinal = []
        # for v in listFileNew:
        #     for e in extension_file_dr:
        #         if FileFinal+e in v[0]:
        #             ExtensionFinal.append(e)
        # print(ExtensionFinal)
        succesGetFile = []

        for download in newFileDownload:
            buff_succes = []
            for ext in extensionList:
                # print(os.path.join(directory, download+ext))
                # print(download+ext)
                retFile = ClientFile61850_getFile(conn, download+ext, directory)
                buff_succes.append(retFile)
            if len([i for i, e in enumerate(buff_succes) if e != 0]) == 0:
                succesGetFile.append(0)
            else:
                succesGetFile.append(-1)
        return newFileDownload, succesGetFile       
    else:
        print("FILE LIST NONE")
        return None, None


def dfr_checkingFiles(con, directory):
    dfr_dir, ret_dfrList = ClientFile61850_dir(con, directory)
    # print(ret_dfrList)

    if ret_dfrList != None:
        buff_dfrExtensionList = []
        buff_dfrNameList = []
        buff_dfrNameFinal = []
        buff_dfrExtFinal = []
        buff_dfrNameList = sorted(
            ret_dfrList, key=lambda ret_dfrList: ret_dfrList[1], reverse=True)

        # buff_file_names = set()
        # buff_extension = set()

        for file_info in buff_dfrNameList:
            file_name = file_info[0]

            file_name_only = file_name.rsplit('.', 1)[0]
            extension = file_name.split('.')[-1]

            if file_name_only not in buff_dfrNameFinal:
                buff_dfrNameFinal.append(file_name_only)
            if extension not in buff_dfrExtFinal:
                buff_dfrExtFinal.append(extension)

        #     buff_file_names.add(file_name_only)
        #     buff_extension.add(extension)

        # for file_name in buff_file_names:
        #     buff_dfrNameFinal.append(file_name)
        # for ext in buff_extension:
        #     buff_dfrExtFinal.append(ext)

        # print(buff_dfrExtFinal)
        # print(buff_dfrNameFinal)

        # buff_dfrNameFinal = buff_dfrNameList[:][0]
        # print(buff_dfrNameFinal)
        # for e in extension_file_dr:
        #     if e in buff_dfrNameList:
        #         buff_dfrNameFinal = buff_dfrNameFinal.replace(e, "")
        # print(buff_dfrNameFinal)

        # for v in buff_dfrNameList:
        #     for e in extension_file_dr:
        #         if buff_dfrNameFinal+e in v[0]:
        #             buff_dfrExtensionList.append(e)
        # print(buff_dfrExtensionList)
        return [dfr_dir, buff_dfrNameFinal, buff_dfrExtFinal]
    else:
        return ["", "", ""]


def dfr_checkingFilesLoop(con, directory):
    dfr_dir, ret_dfrList = ClientFile61850_dir(con, directory)
    # print(dfr_dir)

    if ret_dfrList != None:
        newFileName = []

        buff_dfrNameFinal = []
        buff_dfrExtFinal = []
        buff_dfrTimeFinal = []

        buff_dfrNameList = []
        buff_dfrNameList = sorted(
            ret_dfrList, key=lambda ret_dfrList: ret_dfrList[1], reverse=True)
        # print(buff_dfrNameList)

        # buff_file_names = set()
        # buff_extension = set()
        # buff_timestamp = set()
        buff_file_names = []
        buff_extension = []
        buff_timestamp = []

        for file_info in buff_dfrNameList:
            file_name = file_info[0]
            timestamp = file_info[1]

            file_name_only = file_name.rsplit('.', 1)[0]
            extension = file_name.split('.')[-1]

            if file_name_only not in buff_file_names:
                buff_file_names.append(file_name_only)
            if extension not in buff_extension:
                buff_extension.append(extension)
            if timestamp not in buff_timestamp:
                buff_timestamp.append(timestamp)

            # buff_file_names.add(file_name_only)
            # buff_extension.add(extension)
            # buff_timestamp.add(timestamp)

        # print(buff_file_names)
        # print(buff_extension)
        # print(buff_timestamp)

        # print(newFileName)
        # buff_file_names = sorted(buff_file_names, reverse=True)
        # print(buff_file_names)

        # for file_name in buff_file_names:
        #     # print(file_name)
        #     buff_dfrNameFinal.append(file_name)
        buff_dfrNameFinal = '|'.join(buff_file_names)
        buff_dfrTimeFinal = buff_timestamp

        # for ext in buff_extension:
        #     buff_dfrExtFinal.append(ext)

        # for time in buff_timestamp:
        #     buff_dfrTimeFinal.append(time)

        # print(buff_dfrExtFinal)
        # print(buff_dfrNameFinal)

        # buff_dfrNameFinal = buff_dfrNameList[:][0]
        # print(buff_dfrNameFinal)
        # for e in extension_file_dr:
        #     if e in buff_dfrNameList:
        #         buff_dfrNameFinal = buff_dfrNameFinal.replace(e, "")
        # print(buff_dfrNameFinal)

        # for v in buff_dfrNameList:
        #     for e in extension_file_dr:
        #         if buff_dfrNameFinal+e in v[0]:
        #             buff_dfrExtensionList.append(e)
        # print(buff_dfrExtensionList)

        return [dfr_dir, buff_dfrNameFinal, buff_dfrTimeFinal]
    else:
        return [None, None, None]


def buildZip(dirName):
    #    if "COMTRADE" in dirName:
    #        dirName = dirName.replace("COMTRADE", "")
    #        print(dirName)
    print(dirName)
    if "\\" in dirName:
        buff = dirName.split("\\")
        dirName = buff[-1]
    elif "/" in dirName:
        buff = dirName.split("/")
        dirName = buff[-1]
    dirName = "/"+dirName

    rootDir = '/home/pi/dms/DMSv1.2/IEC61850/DR_FILES'
    #rootDir = DRSAVE_PATH+'DR_FILES'
    filesDir = rootDir+dirName
    with ZipFile(filesDir + '.zip', 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk(filesDir):
            for filename in filenames:
                absname = os.path.abspath(os.path.join(filesDir, filename))
                arcname = absname[len(rootDir) + 1:]
                print('zipping %s as %s' % (os.path.join(filesDir, filename),
                                            arcname))
                zipObj.write(absname, arcname,
                             compress_type=zipfile.ZIP_DEFLATED)
        zipObj.close()
    return filesDir+".zip"


def paramStatusTelegram(relayId, rack, alias, value):
    now = datetime.now()
    waktus = now.strftime("%d/%m/%Y %H:%M:%S")
    d = {"machineCode": mesin_mesin, "relayId": relayId, "lokasi": mesin_namaGi+" "+rack, "status": alias + " " + str(value),
         "namaFile": "STRR" + ' Disturbance.000', "waktu": waktus, "flag": str(0), "type": "IEC61850",
         "portType": 1, "portNumber": 0}

    print(d)
    # response = requests.post("http://"+str(dbCfg3[0])+"/dms/fail/add", data=d)
    # print(response)
    try:
        r = requests.post(
            "http://"+network_ipserver+"/mel/dms/fail/add_event", data=d)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)


def DFRFailADD(relayId, rack, DFRPath, types):
    now = datetime.now()
    waktus = now.strftime("%d/%m/%Y %H:%M:%S")

    url = 'http://'+network_ipserver+'/mel/dms/fail/add'
    print(url)
    # DFRName = os.path.split(DFRPath)
    # DFRName = DFRName[1]

    directory, filename = os.path.split(DFRPath)
    DFRName, extension = os.path.splitext(filename)
    # print(directory)
    # print(DFRName)
    # DFRName = DFRPath.replace(
    #     '/home/pi/dms/DMSv1.2/IEC61850/DR_FILES/', '')
    # DFRName = DFRName.replace(".zip", "")

    try:
        comtradeFolder = DFRPath.replace(".zip", "")
        ret_comtrade = dfr_parse.getDFRvalue(comtradeFolder)
        ret_comtrade = ret_comtrade[1]
    except:
        ret_comtrade = "-"
    # print(DFRPath)
    d = {"machineCode": mesin_mesin,
         "relayId": relayId,
         "lokasi": mesin_namaGi+" "+rack,
         "status": "DFR Available",
         "namaFile": DFRName,
         "waktu": waktus,
         "flag": 0,
         "type": types,
         "portType": "IEC61850",
         "portNumber": 0,
         "dr_metering": "-",
         "dr_event": ret_comtrade
         }

    print(d)

    try:
        r = requests.post(
            url, data=d)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)


def DFRUploadFile(relayId, rack, DFRPath, types):

    now = datetime.now()
    waktus = now.strftime("%d/%m/%Y %H:%M:%S")

    url = 'http://'+network_ipserver+'/mel/dms/notif'
    print(url)
    fileZip = {'myfile': open(DFRPath, 'rb')}
    # print(DFRPath)
    directory, filename = os.path.split(DFRPath)
    DFRName, extension = os.path.splitext(filename)
    # print(directory)
    # print(DFRName)
    # DFRName = DFRPath.replace(
    #     '/home/pi/dms/DMSv1.2/IEC61850/DR_FILES/', '')
    # DFRName = DFRName.replace(".zip", "")

    d = {"status": "DFR Available",
         "file_name": DFRName,
         "machineCode": mesin_mesin,
         "lokasi": mesin_namaGi+" "+rack,
         "namaFile": DFRName,
         "waktu": waktus,
         "flag": 0,
         "type": types,
         "portType": "IEC61850",
         "relayId": relayId,
         "portNumber": 0
         }

    print(d)

    try:
        r = requests.post(url,  data=d, files=fileZip, verify=False)
        print(r)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)

    # r = requests.post(url,  data=d, files=fileZip, verify=False)
    # if r.status_code != 200:
    #     print('sendErr: '+r.url)
    # else:
    #     print(r.text)


def check_IED(con, hostname, port):
    if con == None and isOpen(hostname, port):
        con = lib61850.IedConnection_create()
        error = lib61850.IedClientError()
        lib61850.IedConnection_connect(
            con, ctypes.byref(error), hostname, port)
        if error.value == lib61850.IED_ERROR_OK:
            return con
    elif con != None:
        return 0
    else:
        return None


def initializeFileDR():
    # listFileArray = []

    for i in range(max_client):
        db_fileList.append(None)
        # listFileArray.append(None)

    for i in range(max_client):
        if disturbanceType[i]['type'] == '1':
            idDevice = hostname[i]['id']
            buff_dbFileDR = db.readDb.filedr(0, idDevice)
            # buff_listfileArr = ClientFile61850_dir(
            #     con[i]['con'], iecfolder[i]['id'])

            if len(buff_dbFileDR) == 0:
                checking_IED = check_IED(
                    con[i]['con'], hostname[i]['hostname'], int(tcpport[i]['port']))
                if checking_IED == 0:
                    ret_dfr_list = dfr_checkingFiles(
                        con[i]['con'], iecfolder[i]['id'])
                    db.writeDb.inserfileDR(0, con[i]['id'], ret_dfr_list)
                #     if buff_
                #     db.writeDb.inserfileDR(0, idDevice, buff_listfileArr)
                    db_fileList[i] = db.readDb.filedr(0, idDevice)
                elif checking_IED == None:
                    print("NONE: NOT CONNECTED")
                else:
                    ret_dfr_list = dfr_checkingFiles(
                        checking_IED, iecfolder[i]['id'])
                    db.writeDb.inserfileDR(0, con[i]['id'], ret_dfr_list)
                    db_fileList[i] = db.readDb.filedr(0, idDevice)
            else:
                db_fileList[i] = buff_dbFileDR

        # print(db_fileList[i])

        # for i in range(0, max_client):
        #     if disturbanceType[i]['type'] == '1':
        #         ret_dfr_list = dfr_checkingFiles(
        #             con[i]['con'], iecfolder[i]['id'])
        #         db.writeDb.inserfileDR(0, con[i]['id'], ret_dfr_list)
        #     else:
        #         dfr_fileList.append(None)
        #         db.writeDb.inserfileDREmpty(0, con[i]['id_device'])

    # if db.readDb.filedr(0, i) == 0:
    #     print("DB KOSONG")
    # if ret_db == None:
    #     print("DB KOSONG")


logger.debug("started")
print(con)
mqtt = mqtt.MQTT(0)
connectMqtt(mqtt)

print(network_ipserver)

Client61850_config()
CLient61850_itemConfig()
print(con)
flagNotif = 0

dfr_fileList = []

initializeFileDR()
# for i in range(0, max_client):
#     if disturbanceType[i]['type'] == '1':
#         ret_dfr_list = dfr_checkingFiles(
#             con[i]['con'], iecfolder[i]['id'])
#         db.writeDb.inserfileDR(0, con[i]['id'], ret_dfr_list)
#     else:
#         dfr_fileList.append(None)
#         db.writeDb.inserfileDREmpty(0, con[i]['id_device'])


# update file berdasarkan latest
# for i in range(0, max_client):
#     if disturbanceType[i]['type'] == '1':
#         listfileArr.append(ClientFile61850_dir(
#             con[i]['con'], iecfolder[i]['id']))
#     else:
#         listfileArr.append(None)
# listfileArr[i].sort(key=lambda x: x[1], reverse=False)
# for j in range(len(listfileArr[i])):
#     print(listfileArr[i][j])


listfileArrPrev = []
flags = 0

flagStatus = 0
# update status notif telegram

# print(object_FC)
listFIleprev = 0

start_time_3s = time.time()
start_time_60s = time.time()

try:
    while True:
        # lib61850.Thread_sleep(3000)
        if time.time() - start_time_3s > 3:
            for i in range(0, max_client):
                id_devices = con[i]['id']
                print("ID_DEVICE: ", id_devices,
                      " IP: ", hostname[i]['hostname'])
                checking_IED = check_IED(
                    con[i]['con'], hostname[i]['hostname'], int(tcpport[i]['port']))

                if disturbanceType[i]['type'] == '1':
                    buffCon = None
                    if checking_IED == None:
                        print("NONE: NOT CONNECTED")
                    else:

                        if checking_IED == 0:
                            buffCon = con[i]['con']
                        else:
                            buffCon = checking_IED

                        dfr_checking = dfr_checkingFilesLoop(
                            buffCon, iecfolder[i]['id'])
                        #print(dfr_checking)

                        dfr_existing = db_fileList[i][0]['data']
                        #print(dfr_existing)

                        if dfr_checking[1] != dfr_existing and dfr_checking[1] != None:
                            print("NEW FILE")
                            # print("check ", dfr_checking[1])
                            # print("existing ", dfr_existing)
                            extension = db_fileList[i][0]['extensionDR']
                            dirName, succesFile = newFileMechanismNew(
                                buffCon, dfr_existing, dfr_checking[1], iecfolder[i]['id']+dfr_checking[0], extension)

                            # print(dirName)
                            # print(extFile)
                            #and len([i for i, e in enumerate(succesFile) if e != 0]) == 0
                            
                            for idxDir in range(len(dirName)):

                                if dirName[idxDir] != None and succesFile[idxDir] != None:
                                    print("NEW FILE TO SEND")
                                    dir_correct = dirName[idxDir]
                                    dir_success = succesFile[idxDir]
                                    print("dir_correct: ",dir_correct, "dir_success: ",dir_success)
                                    if dir_success == 0:
#                                    if len(dirName) > 1:
#                                        for v in dirName:
#                                            print(v)
                                        dr_fileZip = buildZip(dir_correct)
                                        try:
                                            DFRFailADD(
                                                i, rack_location[i]['id'], dr_fileZip, type_relay[i]['id'])
                                            DFRUploadFile(
                                                i, rack_location[i]['id'], dr_fileZip, type_relay[i]['id'])
                                        except:
                                            print("ERROR SEND TO SERVER")
                                            
                            updatedDFRList = dfr_checkingFiles(
                                buffCon, iecfolder[i]['id'])
                            db.writeDb.updfileDRNEW(
                                0, con[i]['id'], updatedDFRList)
                            db_fileList[i] = db.readDb.filedr(
                                0, con[i]['id'])
    
#                                    else:
#                                        dr_fileZip = buildZip(dirName[0])
#                                        try:
#                                            DFRFailADD(
#                                                i, rack_location[i]['id'], dr_fileZip, type_relay[i]['id'])
#                                            DFRUploadFile(
#                                                i, rack_location[i]['id'], dr_fileZip, type_relay[i]['id'])
#                                            updatedDFRList = dfr_checkingFiles(
#                                                buffCon, iecfolder[i]['id'])
#                                            db.writeDb.updfileDRNEW(
#                                                0, con[i]['id'], updatedDFRList)
#                                            db_fileList[i] = db.readDb.filedr(
#                                                0, con[i]['id'])
#                                        except:
#                                            print("ERROR SEND TO SERVER")

                if 'obj' in object_read[i]:
                    buffCon = None
                    for j in range(len(object_read[i]['obj'])):
                        if object_type[i]['object_type'][j] == 'boolean':
                            buffCon = None
                            if checking_IED == None:
                                print("NONE: NOT CONNECTED")
                            else:
                                buffCon = None
                                if checking_IED == 0:
                                    buffCon = con[i]['con']
                                else:
                                    buffCon = checking_IED

                                errors = lib61850.IedClientError()
                                value, types = CLient61850_monitoringRead(
                                    buffCon, hostname[i]['hostname'], errors, object_read[i]['obj'][j], object_FC[i]['obj'][j])
                                dataJson = {
                                    "alias": alias_monit[i]['alias'][j], "val": value, "dataType": types}
                                topic = f"DMS/{mesin_mesin}/IEC61850/{object_read[i]['id']}/{object_read[i]['itemID'][j]}/"
                                # print(type(types))
                                if types == 0 or types == None:
                                    print("Data is None")

                                else:
                                    try:
                                        mqtt.send(client, topic, str(dataJson))
                                    except:
                                        print("mqtt not connect")

            start_time_3s = time.time()

        if time.time() - start_time_60s > 60:
            for i in range(0, max_client):
                id_devices = con[i]['id']
                print("ID_DEVICE: ", id_devices,
                      " IP: ", hostname[i]['hostname'])
                checking_IED = check_IED(
                    con[i]['con'], hostname[i]['hostname'], int(tcpport[i]['port']))
                if 'obj' in object_read[i]:
                    buffCon = None
                    if checking_IED == None:
                        print("NONE: NOT CONNECTED")
                    else:
                        buffCon = None
                        if checking_IED == 0:
                            buffCon = con[i]['con']
                        else:
                            buffCon = checking_IED

                        errors = lib61850.IedClientError()
                        value, types = CLient61850_monitoringRead(
                            buffCon, hostname[i]['hostname'], errors, object_read[i]['obj'][j], object_FC[i]['obj'][j])
                        dataJson = {
                            "alias": alias_monit[i]['alias'][j], "val": value, "dataType": types}
                        topic = f"DMS/{mesin_mesin}/IEC61850/{object_read[i]['id']}/{object_read[i]['itemID'][j]}/"
                        # print(type(types))
                        if types == 0 or types == None:
                            print("Data is None")

                        else:
                            try:
                                mqtt.send(client, topic, str(dataJson))
                            except:
                                print("mqtt not connect")

            start_time_60s = time.time()


except KeyboardInterrupt:
    CLient61850_destroyConn()
    print('interrupted!')
