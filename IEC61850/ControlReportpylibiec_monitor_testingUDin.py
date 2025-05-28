import ctypes
from ctypes import c_char_p
# try:
#    import lib61850
# except:
import lib61850_linux as lib61850
import zipfile
from zipfile import ZipFile
from libiec61850client import iec61850client
import db
import time
from datetime import datetime
# import mqtt as mqtt
import requests

import dfr_parse

import os
import socket
import paho.mqtt.publish as mqtt_publish
from collections import defaultdict
import psutil
import sys
import subprocess
import re
import shutil
import faulthandler
faulthandler.enable()

process = psutil.Process(os.getpid())

DEBUG = False  # """untuk percobaan dengan server localhost"""
MQTT_HOST = "localhost"
MQTT_PORT = 1883
RECONNECT_TIMEOUT = 1  # seconds
MAX_FILES_PER_DEVICE = 3  # Set the file limit per device
MAX_MEMORY_USAGE = 80  # Set your memory limit in MB
SERVICE_NAME = "tessystemmd.service"

if DEBUG:
    dataDevice = ['127.0.0.1']
else:
    DBdataMeasurement = db.readDb.m_file_iec_read_by_active(0)
    DBdataDevices = db.readDb.device_list(1)
    DBdataNetwork = db.readDb.network(0)
    DBdataMMesin = db.readDb.m_mesin(0)
    # print(DBdataDevices)
    # print(dir(db.readDb))
    dataDRIEC = db.readDb.data_iec_filedr_all(0)
dataDevice = []
dbMqtt = db.readDb.network_mqtt(0)
# print("data DR IEC: " + str(dataDRIEC))

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
error = []
con = []
model = []
object_read = []
object_FC = []
file_list = []
rack_location = []
type_relay = []
name_alias = []
disturbanceType = []
iecfolder = []
iecFiles = []
maxfilesperdevices = []
reportStatus = {}
reportObject = {}

network_ipserver = DBdataNetwork[0]['ipserver']
mesin_mesin = DBdataMMesin[0]['kode_mesin']
mesin_namaGi = DBdataMMesin[0]['nama_gi']

#disturbanceType = DBdataDevices[0]['disturbance_type']
#print(disturbanceType)


client = None

extension_file_dr = [".cfg", ".dat", ".hdr", ".cev", ".txt", ".zip", ".inf",
                     ".CFG", ".DAT", ".HDR", ".CEV", ".TXT", ".ZIP", ".INF"]
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
    #print("received %i bytes for file: %s" % (bytesRead, filename))
    if bytesRead > 0:
        with open(filename, "ab") as fp:
            bytesbuffer = ctypes.string_at(buffer, bytesRead)
            fp.write(bytesbuffer)  # append bytes to file
    return True


# def ClientFile61850_dir():
# def ClientFile61850_dir():
def ClientFile61850_dir(con, iec_dir):
    listFile = []
    seen = set()
    error_file = lib61850.IedClientError()
    rootDirectory = lib61850.IedConnection_getFileDirectory(con, error_file, iec_dir)
    
    if error_file.value != lib61850.IED_ERROR_OK:
        print("Error retrieving file directory")
        return None
    else:
        directoryEntry = lib61850.LinkedList_getNext(rootDirectory)

        while directoryEntry:
            entry = ctypes.cast(lib61850.LinkedList_getData(directoryEntry), lib61850.FileDirectoryEntry)
            file_name = lib61850.FileDirectoryEntry_getFileName(entry).decode("UTF-8")
            file_size = lib61850.FileDirectoryEntry_getFileSize(entry)
            file_modified = lib61850.FileDirectoryEntry_getLastModified(entry)
            # print("name: %s size: %d modified: %s" % (file_name, file_size, file_modified))
            
            for v in extension_file_dr:
                if v in file_name:
                    listFile.append([file_name, file_modified])
            # Check if the file has one of the valid extensions
            # for ext in extension_file_dr:
            #     if ext in file_name:
            #         # Remove extension from file_name to get the base name for checking uniqueness.
            #         base_name = os.path.splitext(file_name)[0]
            #         if base_name not in seen:
            #             listFile.append([file_name, file_modified])
            #             seen.add(base_name)
            #         break  # Found an extension match, break out of loop
            
            directoryEntry = lib61850.LinkedList_getNext(directoryEntry)
        
        lib61850.LinkedList_destroy(directoryEntry)
        return listFile
    # else:
    #    print("connection issue")

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
            # ipserver[i] = DBdataMeasurement[i]['ipserver']
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

            type_relay.append(
                {'id': dataDevice[i]["type"]})
                
            iecfolder.append(
                {'id': dataDevice[i]["iec_file"]})
                
            disturbanceType.append(
                {'type': dataDevice[i]["disturbance_type"]})
            #print(disturbanceType)

    for i in range(0, max_client):
        iecFiles.append({'id': dataDevice[i]["id_device"], 
                         'files': next((entry["listDR"] for entry in dataDRIEC if entry["id_device"] == dataDevice[i]["id_device"]), None)})
        if not isOpen(hostname[i]['hostname'], tcpport[i]['port']):
                print(f"Port closed for {hostname[i]['hostname']}:{tcpport[i]['port']}. Skipping this device.")
                # con[i]['con'] = None  # Ensure no broken connection remains
                continue  # Skip device if port is closed
        lib61850.IedConnection_connect(
            con[i]['con'], ctypes.byref(error[i]['error']), hostname[i]['hostname'], int(tcpport[i]['port']))
        if (error[i]['error'].value == lib61850.IED_ERROR_OK):
            print("IEC61850 Connection OK in %s:%s" % (
                hostname[i]['hostname'], tcpport[i]['port']))
        else:
            print("IEC61850 Connection error in %s:%s" % (
                hostname[i]['hostname'], tcpport[i]['port']))
        

def CLient61850_itemConfig():
    # for k,v in DBdataMeasurement.items():
    #     if v in object_read['id']
    for v in DBdataMeasurement:
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
                    #print(item_id)
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



def CLient61850_destroyConn():
    for i in range(0, max_client):
        lib61850.IedConnection_release(con[i]['con'], error[i]['error'])
        print("releasing connection")
        if (error[i]['error'].value != lib61850.IED_ERROR_OK):
            print("Release returned error: %d" % error[i]['error'].value)
        else:
            while (lib61850.IedConnection_getState(con[i]['con']) != lib61850.IED_STATE_CLOSED):
                lib61850.Thread_sleep(10)

        lib61850.IedConnection_destroy(con[i]['con'])


def isOpen(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        s.connect((ip, int(port)))
        s.shutdown(socket.SHUT_RDWR)
        # print("IP: %s Port: %d Opened" % (ip, int(port)))
        return True
    except:
        # print("IP: %s Port: %d Closed" % (ip, int(port)))
        return False
    finally:
        s.close()
        

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



def ClientFile61850_getFile(con, fileNameAsal, directory, relayId, max_retries=5, retry_delay=1):
    # Root directory
    rootDir = f"/var/www/html/dms_setting/assets/api/file_dr/{relayId}"

    # Ensure a folder exists for the relay
    if not os.path.exists(rootDir):
        os.mkdir(rootDir)

    # Extract the disturbance file base name (without extension)
    buff = fileNameAsal.replace("\\", "/").split("/")
    dirName = buff[-1][:-4]  # Remove extension
    localfilename = buff[-1]

    # Create directory for this disturbance file inside the relay directory
    disturbanceDir = os.path.join(rootDir, dirName)
    if not os.path.exists(disturbanceDir):
        os.mkdir(disturbanceDir)
        print(f"Created directory: {disturbanceDir}")

    # File path for saving
    newfile = os.path.join(disturbanceDir, localfilename)
    fileNameOutput = bytes(newfile.encode('utf-8'))

    # Create an empty file before writing to it
    open(newfile, "w").close()

    # Retrieve file from IEC 61850 server with retries
    handler = lib61850.IedClientGetFileHandler(_getFileHandler)
    error_getfile = lib61850.IedClientError()

    for attempt in range(1, max_retries + 1):
        print(f"Attempt {attempt} to get file: {fileNameAsal}")
        lib61850.IedConnection_getFile(
            con, error_getfile, os.path.join(directory, fileNameAsal), handler, ctypes.c_char_p(fileNameOutput)
        )

        if error_getfile.value == lib61850.IED_ERROR_OK:
            print(f"File {fileNameAsal} successfully retrieved!")
            return True

        print(f"Failed to get file: {fileNameAsal}, Error: {error_getfile.value}")
        if attempt < max_retries:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)

    print(f"Exceeded maximum retries ({max_retries}). Failed to get file: {fileNameAsal}")
    return False


def newFileMechanism(conn, fileList, directory, relayId):
    # Sort files by timestamp (newest first)
    listFileNew = sorted(fileList, key=lambda fileList: fileList[1], reverse=True)
    print(listFileNew)

    # Determine the base file name
    FileFinal = listFileNew[0][0]
    for e in extension_file_dr:
        if e in FileFinal:
            print(e)
            FileFinal = FileFinal.replace(e, "")

    # Track extensions for this file group
    ExtensionFinal = []
    chosenZip = None

    # Check for zip files, prioritizing ones *without* "h" in the name
    for v in listFileNew:
        fileName = v[0]
        for e in extension_file_dr:
            if FileFinal + e in fileName:
                ExtensionFinal.append(e)

            # Prioritize zip files without 'h'
            if fileName.endswith(".zip"):
                if 'h' not in fileName:
                    chosenZip = fileName
                elif chosenZip is None:  
                    chosenZip = fileName

    # Download only the preferred zip (without 'h') and other related files
    for e in ExtensionFinal:
        if e == '.zip':
            isSuccess = ClientFile61850_getFile(conn, chosenZip, directory, relayId)
            trimmedZip = chosenZip.replace('.zip', "")
            print("File Final: " + str(trimmedZip))
            return trimmedZip, ExtensionFinal, isSuccess
        else:
            isSuccess = ClientFile61850_getFile(conn, FileFinal + e, directory, relayId)

    print("File Final: " + str(FileFinal))
    return FileFinal, ExtensionFinal, isSuccess


def buildZip(dirName, id_device):

    # Extract only the final folder name from dirName
    if "\\" in dirName:
        buff = dirName.split("\\")
        dirName = buff[-1]
    elif "/" in dirName:
        buff = dirName.split("/")
        dirName = buff[-1]
    # Prepend a slash for folder naming consistency
    folderName = "/" + dirName
    
    # Define the root directory for file_dr dynamically
    rootDir = "/var/www/html/dms_setting/assets/api/file_dr/" + str(id_device)
    filesDir = rootDir + folderName
    print("filesDir: " + filesDir)

    # Define the set of desired extensions (lowercase)
    desired_exts = {'.cfg', '.dat', '.hdr', '.zip', '.inf'}

    zipFilePath = filesDir + '.zip'
    with ZipFile(zipFilePath, 'w') as zipObj:
        # Walk the directory, but only add files with desired extensions
        for folder, subfolders, filenames in os.walk(filesDir):
            for filename in filenames:
                ext = os.path.splitext(filename)[1].lower()
                if ext in desired_exts:
                    absname = os.path.abspath(os.path.join(folder, filename))
                    # Create a relative path for the zip archive
                    arcname = os.path.relpath(absname, rootDir)
                    print('zipping %s as %s' % (absname, arcname))
                    zipObj.write(absname, arcname, compress_type=zipfile.ZIP_DEFLATED)
    return zipFilePath

def DFRFailADD(relayId, rack, DFRPath, types):
    now = datetime.now()
    waktus = now.strftime("%d/%m/%Y %H:%M:%S")

    url = 'http://' + str(network_ipserver) + '/mel/dms/fail/add'
    directory = "/var/www/html/dms_setting/assets/api/file_dr/" + relayId
    DFRName = DFRPath.replace(directory, '')
    DFRName = DFRName.replace(".zip", "")
    
    # Normalize the comtrade folder path
    comtradeFolder = os.path.normpath(DFRPath.replace(".zip", ""))
    # print("comtradeFolder: " + comtradeFolder)
    
    # Verify that the directory exists before processing
    if not os.path.exists(comtradeFolder):
        print(f"Error: Directory does not exist: {comtradeFolder}")
        return

    # ret_comtrade = dfr_parse.getDFRvalue(comtradeFolder)
    # print("ret_comtrade: " + str(ret_comtrade))

    d = {
        "machineCode": mesin_mesin,
        "relayId": relayId,
        "lokasi": mesin_namaGi + " " + rack,
        "status": "DFR Available",
        "namaFile": "/"+ relayId+DFRName,
        "waktu": waktus,
        "flag": 0,
        "type": types,
        "portType": "IEC61850",
        "portNumber": 0,
        "dr_metering": 0,
        "dr_event": 0
    }

    print("Query Data: " + str(d))

    try:
        r = requests.post(url, data=d)
        r.raise_for_status()
        print("Success")
        print("status Code: "+ str(r.status_code))
        print("Response: " + r.text)
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

    url = 'http://'+str(network_ipserver)+'/mel/dms/notif'

    fileZip = {'myfile': open(DFRPath, 'rb')}
    # print("DFRPath: "+DFRPath)
    directory = "/var/www/html/dms_setting/assets/api/file_dr/" + str(relayId)
    DFRName = DFRPath.replace(
        directory, '')
    DFRName = DFRName.replace(".zip", "")
    DFRName = "/"+ str(relayId)+DFRName
    #print(DFRName)
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
    print("FileZip: "+ str(fileZip))
    try:
        r = requests.post(url,  data=d, files=fileZip, verify=False)
        r.raise_for_status()
        print("Success")
        print("status Code: "+ str(r.status_code))
        print("Response: " + r.text)
        if r.status_code != 200:
            print('sendErr: '+r.url)
            db.insertDb.m_fileDR_temp(2,relayId,str(relayId),str(d),str(0),DFRName)
        else:
            print(r.text)
            db.insertDb.m_fileDR_temp(2,relayId,str(relayId),str(d),str(1),DFRName)
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
        db.insertDb.m_fileDR_temp(0,'2',str(relayId),str(d),str(0),DFRName)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
        db.insertDb.m_fileDR_temp(0,'2',str(relayId),str(d),str(0),DFRName)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
        db.insertDb.m_fileDR_temp(0,'2',str(relayId),str(d),str(0),DFRName)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)
        db.insertDb.m_fileDR_temp(0,'2',str(relayId),str(d),str(0),DFRName)
        

def check_memory_usage():
    """Check memory usage and restart the service if it exceeds the threshold."""
    process = psutil.Process(os.getpid())  # Get the current process
    mem_usage = process.memory_info().rss / (1024 * 1024)  # Convert to MB
    print(f"Memory usage: {mem_usage:.2f} MB")

    if mem_usage > MAX_MEMORY_USAGE:
        print(f"Memory usage exceeded {MAX_MEMORY_USAGE}MB! Restarting {SERVICE_NAME}...")
        
        try:
            CLient61850_destroyConn()
            subprocess.run(["sudo", "systemctl", "restart", SERVICE_NAME], check=True)
            print(f"{SERVICE_NAME} restarted successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to restart {SERVICE_NAME}: {e}")

def process_disturbance_files(device_index):
    device_index = int(device_index)
    device_id = hostname[device_index]['id']
    device_entry = iecFiles[device_index]['files']


    # Ensure the device is of the correct type
    if disturbanceType[device_index]['type'] != '1':
        return

    # Fetch the current file list from the IEC server
    currentFileList = ClientFile61850_dir(con[device_index]['con'], iecfolder[device_index]['id'])
    # Extract base names from currentFileList and convert to a set for unique entries

    if currentFileList is None:
        print(f"❌ File list retrieval failed for client {device_index}")
        con[device_index]['con'] = None
        return
    
    unique_basenames = {os.path.splitext(os.path.basename(file[0]))[0] for file in currentFileList}
    existing_device = next((d for d in maxfilesperdevices if d['id'] == device_id), None)

    # Track the number of unique files per device
    if existing_device:
        existing_device['max'] = len(unique_basenames)  # Update if device already exists
    else:
        maxfilesperdevices.append({'id': device_id, 'max': len(unique_basenames)})  # Add new entry if missing    

    # print("maxfilesperdevices:", maxfilesperdevices)
    # Extract trimmed base names from the current file list
    current_base_names = [
        re.sub(r'^[\\/]+', '', os.path.basename(os.path.splitext(entry[0])[0]).strip())
        for entry in currentFileList
    ]

    # Get the device ID and check existing records in DB

    # Check if device_entry is a valid string and split it into a list
    existing_bases = (
        device_entry.split('|') if isinstance(device_entry, str) and device_entry.strip() else []
    )

    # print("📁 Existing data:", existing_bases)

    # Determine new files to process by comparing with existing ones
    new_bases = [base for base in current_base_names if base not in existing_bases]
    
    filtered_bases = set()
    for base in new_bases:
        # Check if a version with 'h' exists
        if base.endswith("h") and base[:-1] in new_bases:
            continue  # Skip the "h" version if the non-"h" one exists
        filtered_bases.add(base)

    new_bases = filtered_bases


    # Process only the new files
    if not new_bases:
        print(f"✅ No new files to process for device {device_id}")
        return

    print(f"🛠️ New files detected for device {device_id}: {new_bases}")
    
    new_bases = set(new_bases)


    required_extensions = {".cfg", ".dat"}

    # Rebuild the set, keeping only valid bases OR those that already have a .zip file
    new_bases = {
        base_name for base_name in new_bases
        if ".zip" in {
            os.path.splitext(entry[0])[1]
            for entry in currentFileList if base_name in entry[0]
        } or required_extensions.issubset({
            os.path.splitext(entry[0])[1]
            for entry in currentFileList if base_name in entry[0]
        })
    }
    # failedFiles = []
    successFiles = []

    # Process the remaining valid files
    for base_name in new_bases:
        print(f"✅ Processing new file group: {base_name}")

        entries = [entry for entry in currentFileList if base_name in entry[0]]
        dirName, extFile, isSuccess = newFileMechanism(
            con[device_index]['con'], entries, iecfolder[device_index]['id'], hostname[device_index]['id']
        )
        # isSuccess = False

        if isSuccess:
            dr_file = buildZip(dirName, hostname[device_index]['id'])
            successFiles.append(base_name)
        else:
            print(f"❌ Failed to process {base_name}, marking as failed.")
            break
            # failedFiles.append(base_name)

    # Remove all failed files from new_bases
    # Combine existing and new bases
    updated_base_list = existing_bases + list(successFiles)
    updated_base_list = set(updated_base_list)

    # Enforce file limit *WITHOUT updating the DB if files are deleted*
    enforce_file_limit(device_id, current_base_names)

    # Convert updated list to string format
    updated_base_list_str = "|".join(updated_base_list)

    try:
        # Only update/insert DB if there were new files processed
        if device_entry is not None and isinstance(device_entry, str) and device_entry.strip():
            print(f"🔧 Updating DR data for device {device_id}")
            db.updateDb.data_iec_filedr_update(0, device_id, updated_base_list_str)
            DFRFailADD(con[device_index]['id'], rack_location[device_index]['id'], dr_file, type_relay[device_index]['id'])
            print("UPLOAD FILE TO SERVER")
            DFRUploadFile(con[device_index]['id'], rack_location[device_index]['id'], dr_file, type_relay[device_index]['id'])
        else:
            print(f"🆕 Inserting DR data for device {device_id}")
            db.insertDb.data_iec_filedr_insert(0, device_id, updated_base_list_str)
            

        print(f"✅ All new files processed and DB updated for device {device_id}")

        # Update the local cache
        iecFiles[device_index]['files'] = updated_base_list_str

    except Exception as e:
        print(f"❌ Error updating DB for device {device_id}: {e}")

def process_new_file(device_index, base_name, currentFileList):
    """Process each new file: zip, store, and upload."""
    

    # Upload and track the file

def enforce_file_limit(device_id, current_base_name):
    """Ensure the file count stays within the defined limit (FIFO).
    🚨 **DO NOT** update the DB when files are deleted to prevent duplicates!
    """
    device_folder = f"/var/www/html/dms_setting/assets/api/file_dr/{device_id}/"

    # Check if the device folder exists
    if not os.path.exists(device_folder):
        print(f"⚠️ Device folder not found: {device_folder}")
        return

    # Get a sorted list of zip files in the folder (oldest first)
    files_in_folder = sorted(
        [f for f in os.listdir(device_folder) if f.endswith(".zip")],
        key=lambda f: os.path.getmtime(os.path.join(device_folder, f))
    )

    # Find the max file limit for this device
    max_files = next((entry['max'] for entry in maxfilesperdevices if entry['id'] == str(device_id)), None)

    if max_files is None:
        print(f"⚠️ No file limit set for device {device_id}")
        return

    # Filter out files that are part of new_bases
    valid_files = {f"{base}.zip" for base in current_base_name}  # Convert to .zip format for comparison
    files_to_check = [f for f in files_in_folder if f not in valid_files]

    # Enforce file limit
    if len(files_in_folder) > max_files:
        excess_count = len(files_in_folder) - max_files
        files_to_delete = files_to_check[:excess_count]  # Only delete files not in new_bases
        print("Files to delete: "+ str(files_to_delete))

        print(f"🗑️ Deleting {len(files_to_delete)} old files to maintain the limit:")
        for old_file in files_to_delete:
            try:
                old_file_path = os.path.join(device_folder, old_file)
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
                    print(f"🗑️ Deleted zip file: {old_file_path}")

                folder_name = os.path.splitext(old_file)[0]
                folder_path = os.path.join(device_folder, folder_name)
                if os.path.exists(folder_path) and os.path.isdir(folder_path):
                    shutil.rmtree(folder_path)
                    print(f"🗑️ Deleted folder: {folder_path}")

            except Exception as e:
                print(f"❌ Error deleting file or folder {old_file}: {e}")
    else:
        print("✅ No files to delete.")


def publish_mqtt_data(mqtt_data):
    """Publish collected MQTT data."""
    if mqtt_data is None: 
        return  # Skip if no data to publish
    for topic, dataJson in mqtt_data:
        try:
            # mqtt_publish.single(topic, dataJson, hostname=MQTT_HOST, port=MQTT_PORT)
            mqtt_publish.single(topic, dataJson, hostname='localhost', port=1883)
            mqtt_publish.single(topic, dataJson, hostname=dbMqtt[0]['mqtt_server'],
                                port=dbMqtt[0]['mqtt_port'], auth={'username': dbMqtt[0]['mqtt_username'], 'password': dbMqtt[0]['mqtt_pass']})
        except Exception as e:
            print("MQTT not connected:", e)


def isOpen(ip, port):
    """Check if the given IP and port (default IEC61850: 102) are open."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        s.connect((ip, int(port)))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except:
        return False
    finally:
        s.close()


def iec61850_getIED(id_device):
    """Check if the device is connected, if not, establish a new connection."""
    id_device = str(id_device)
    while len(con) <= int(id_device):  # Make sure list is big enough
        con.append(None)


    if con[int(id_device)] is not None:
        if isOpen(con[id_device]['host']['ip'], con[id_device]['host']['port']):
            return 0  # Connection is valid
        else:
            lib61850.IedConnection_destroy(con[int(id_device)])
            con[int(id_device)] = None
            return -1  # Connection was lost


    if id_device not in con:
        con[id_device] = {"con": None}  # Initialize if not present

    if isOpen(con[id_device]['host']['ip'], con[id_device]['host']['port']):
        hostIP = con[id_device]['host']['ip']
        portIP = int(con[id_device]['host']['port'])
        con = lib61850.IedConnection_create()
        error = lib61850.IedClientError()
        lib61850.IedConnection_connect(con, ctypes.byref(error), hostIP, portIP)

        if error.value == lib61850.IED_ERROR_OK:
            con[id_device]["con"] = con  # Store the active connection
            return 0
        else:
            lib61850.IedConnection_destroy(con)
            con[id_device]["con"] = None
            return -1
    else:
        return -1
    

def ReportHandler_cb(param, report):
    print("Masuk Callback")

    dataset_directory = ctypes.cast(param, ctypes.py_object).value
    print("dataset_directory: ", dataset_directory)
    # dataset_directory = lib61850.LinkedList_getNext(dataset_directory)
    dataset_values = lib61850.ClientReport_getDataSetValues(report)

    if dataset_directory:
        entry = dataset_directory
        index = 0

        while bool(entry):
            reason = lib61850.ClientReport_getReasonForInclusion(report, index)
            # print("reason: "+ str(reason))
            # print("entry: ", entry)

            if reason != 0:  # assuming 0 = IEC61850_REASON_NOT_INCLUDED
                buffer = ctypes.create_string_buffer(500)

                if dataset_values:
                    value = lib61850.MmsValue_getElement(dataset_values, index)
                    # print("value: ", value)
                    if value:
                        lib61850.MmsValue_printToBuffer(value, buffer, 500)
                
                # print("entry: ", entry)

                entry_data = lib61850.LinkedList_getData(entry)
                print("entry Data: ", entry_data)
                entry_data = ctypes.cast(entry_data, c_char_p)
                entry_name = entry_data.value.decode('utf-8') if entry_data else "UnknownEntry"
                # print(f"EntryName: {entry_name}") 
                print(f"  {entry_name} (included for reason {reason}): {buffer.value.decode()}")

            # move to next linked list node
            entry = lib61850.LinkedList_getNext(entry)
            index += 1
            # if index > 5: 
            #     break


def report(con, error, cb, ds):
    print("Calling function report")
    rcb = lib61850.IedConnection_getRCBValues(con,ctypes.byref(error), "BCUCPLCONTROL1/LLN0$BR$brcbST01", None)

    # if error.value != lib61850.IED_ERROR_OK:
    # 	print("getRCBValues service error!")
    # 	exit()

    #/* prepare the parameters of the RCP */
    lib61850.ClientReportControlBlock_setResv(rcb, True)
    lib61850.ClientReportControlBlock_setTrgOps(rcb, lib61850.TRG_OPT_DATA_CHANGED | lib61850.TRG_OPT_QUALITY_CHANGED | lib61850.TRG_OPT_GI)
    lib61850.ClientReportControlBlock_setDataSetReference(rcb, "BCUCPLCONTROL1/LLN0$LLN0BRptStDs")
    lib61850.ClientReportControlBlock_setRptEna(rcb, True)
    lib61850.ClientReportControlBlock_setGI(rcb, True)
    rptid = lib61850.ClientReportControlBlock_getRptId(rcb)
    
    cbRef = lib61850.ReportCallbackFunction(ReportHandler_cb)
    LinkedList = lib61850.IedConnection_getDataSetDirectory(con, ctypes.byref(error),"BCUCPLCONTROL1/LLN0$LLN0BRptStDs",None)
    print("LinkedList: " + str(LinkedList))
    # Lalu pasang:
    lib61850.IedConnection_installReportHandler(con, "BCUCPLCONTROL1/LLN0$BR$brcbST01", rptid, cbRef, id(LinkedList))
    print("cb installed")
    lib61850.IedConnection_setRCBValues(con,ctypes.byref(error), rcb, lib61850.RCB_ELEMENT_RPT_ENA , True) #"""| lib61850.RCB_ELEMENT_GI"""
    print("setRCB called")
    if error.value != lib61850.IED_ERROR_OK:
        print("setRCBValues service error!")

    time.sleep(1)

    #/* Trigger GI Report */
    lib61850.ClientReportControlBlock_setGI(rcb, True)
    lib61850.IedConnection_setRCBValues(con,ctypes.byref(error), rcb,  lib61850.RCB_ELEMENT_RPT_ENA | lib61850.RCB_ELEMENT_GI, True)
    # print("gi send, waiting 5 sec.")
    # err = 0
    # while 1:
    #     print("kene sek ae bro")
    #     time.sleep(1)
    return error.value


def checkReport(device_index):
    """asd"""
    print("id_device")
    device_index = int(device_index)
    device_id = hostname[device_index]['id']
    # con = con[device_index]['con']
    # error = error[device_index]['error']
    status = reportStatus.get(device_index, {}).get('status', None)
    print("status ", status)
    if status is None or status != 0:
        isError = report(con[device_index]['con'], error[device_index]['error'], cb="BCUCPLCONTROL1/LLN0$BR$brcbST01", ds="BCUCPLCONTROL1/LLN0$LLN0BRptStDs")
        print("isError: ", isError)
        reportStatus[device_index] = {'status': isError}
        return


Client61850_config()
CLient61850_itemConfig()

try:
    while True:
        check_memory_usage()
        lib61850.Thread_sleep(1000)  # Sleep for 1 second
        # time.sleep()

        for i in range(0, max_client):
            device_id = hostname[i]['id']
            device_ip = hostname[i]['hostname']
            device_port = int(tcpport[i]['port'])

            if not isOpen(hostname[i]['hostname'], tcpport[i]['port']):
                print(f"Port closed for {hostname[i]['hostname']}:{tcpport[i]['port']}. Skipping this device.")
                con[i]['con'] = None  # Ensure no broken connection remains
                continue  # Skip device if port is closed

            # Try to establish a new connection if necessary
            if con[i]['con'] is None:
                print(f"Re-establishing connection to {device_ip}:{device_port}...")
                error[i]['error'] = lib61850.IedClientError()
                con[i]['con'] = lib61850.IedConnection_create()
                lib61850.IedConnection_connect(
                    con[i]['con'], ctypes.byref(error[i]['error']), hostname[i]['hostname'], device_port)

                if error[i]['error'].value != lib61850.IED_ERROR_OK:
                    print(f"Failed to connect to {device_ip}:{device_port}. Skipping...")
                    con[i]['con'] = None  # Ensure no broken connection remains
                    continue  # Skip this device again
                    # 
            # process_disturbance_files(i)
            rcb_names = [
                "BCUCPLCONTROL1/LLN0$BR$brcbST01",
                "BCUCPLCONTROL1/LLN0$BR$brcbST02"
            ]

            for rcb_ref in rcb_names:
                print(f"Setting up report for {rcb_ref}")

                # Get RCB
                rcb = lib61850.IedConnection_getRCBValues(
                    con[i]['con'],
                    ctypes.byref(error[i]['error']),
                    rcb_ref,
                    None
                )

                if error[i]['error'].value != lib61850.IED_ERROR_OK:
                    print(f"Failed to get RCB values for {rcb_ref}, skipping this RCB.")
                    continue

                # Prepare the RCB parameters
                lib61850.ClientReportControlBlock_setResv(rcb, True)
                lib61850.ClientReportControlBlock_setTrgOps(
                    rcb,
                    lib61850.TRG_OPT_DATA_CHANGED |
                    lib61850.TRG_OPT_QUALITY_CHANGED |
                    lib61850.TRG_OPT_GI
                )
                lib61850.ClientReportControlBlock_setDataSetReference(
                    rcb,
                    "BCUCPLCONTROL1/LLN0$LLN0BRptStDs"
                )
                lib61850.ClientReportControlBlock_setRptEna(rcb, True)
                lib61850.ClientReportControlBlock_setGI(rcb, True)

                rptid = lib61850.ClientReportControlBlock_getRptId(rcb)
                cbRef = lib61850.ReportCallbackFunction(ReportHandler_cb)

                # Get DataSet Directory
                LinkedList = lib61850.IedConnection_getDataSetDirectory(
                    con[i]['con'],
                    ctypes.byref(error[i]['error']),
                    "BCUCPLCONTROL1/LLN0$LLN0BRptStDs",
                    None
                )
                print("LinkedList: " + str(LinkedList))

                # Install Report Handler
                lib61850.IedConnection_installReportHandler(
                    con[i]['con'],
                    rcb_ref,
                    rptid,
                    cbRef,
                    id(LinkedList)
                )
                print(f"Callback installed for {rcb_ref}")

                # Set RCB Values to enable reporting
                lib61850.IedConnection_setRCBValues(
                    con[i]['con'],
                    ctypes.byref(error[i]['error']),
                    rcb,
                    lib61850.RCB_ELEMENT_RPT_ENA,
                    True
                )

                if error[i]['error'].value != lib61850.IED_ERROR_OK:
                    print(f"setRCBValues service error for {rcb_ref}")

                time.sleep(1)

                # Trigger GI Report
                lib61850.ClientReportControlBlock_setGI(rcb, True)
                lib61850.IedConnection_setRCBValues(
                    con[i]['con'],
                    ctypes.byref(error[i]['error']),
                    rcb,
                    lib61850.RCB_ELEMENT_RPT_ENA | lib61850.RCB_ELEMENT_GI,
                    True
                )

                if error[i]['error'].value != lib61850.IED_ERROR_OK:
                    print(f"setRCBValues service error after GI for {rcb_ref}")
                
                time.sleep(10)

# print("gi send, waiting 5 sec.")
            # err = 0
            # while 1:
            #     print("kene sek ae bro")
            #     time.sleep(1)
            
            # mqtt_data = read_monitoring_data(i)
            # publish_mqtt_data(mqtt_data)
        # except Exception as e:
        #     print("Error:", e)

except KeyboardInterrupt:
    CLient61850_destroyConn()
    print("Interrupted!")

# except Exception as e:
#     CLient61850_destroyConn()
#     print("Interrupted!")
    