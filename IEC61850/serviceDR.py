import db
import time
import os
import requests
import json
network =db.readDb.network(1)
url = 'http://'+network[0]["ipserver"]+'/mel/dms/fail/add'
url2='http://'+network[0]["ipserver"]+'/mel/dms/notif'

def clearDr():
    req = db.readDb.last_fileDr(1)
    print("Jumlah yang dihapus :",len(req))
    for i in range (len(req)):
        print(req[i]["nama"])
        try:
            #remove1 = os.remove("/home/pi/dms/DMSv1.2/IEC61850/DR_FILES/"+req[i]["nama"])
            loc="/var/www/html/dms_setting/assets/api/file_dr/"+req[i]["nama"]+".zip"
            loc2="/var/www/html/dms_setting/assets/api/file_dr/"+req[i]["nama"]
            loc3="/var/www/html/dms_setting/assets/api/file_dr/"+req[i]["nama"]+".zip"
            
            try:
                remove1=os.remove(loc)
            except:
                print("failed to delete" + loc)
            try:
                remove2=os.remove(loc)
            except:
                print("failed to delete" + loc2)
            try:
                remove3=os.remove(loc)
            except:
                print("failed to delete" + loc3)
            
            id= req[i]["id"]
            try:
                deldb=db.deleteDb.fileDr_temp_by_id(1,id)
                print(deldb)
            except:
                print("failed to del db")
        except NameError:
           # print(NameError)
            print ("fail to delete All")        
        time.sleep(1)
        
def DFRUploadFile(DFRPath,status):
    global url2
    
    path='/var/www/html/dms_setting/assets/api/file_dr/'+DFRPath
    fileZip = {'myfile': open(path, 'rb')}
    print(DFRPath)

    DFRName = DFRPath.replace(
        '/var/www/html/dms_setting/assets/api/file_dr/', '')
    DFRName = DFRName.replace(".zip", "")
    print(DFRName)
    #filesDir+".zip"
    d = status
    print(d)

    r = requests.post(url2,  data=d, files=fileZip, verify=False)
    if r.status_code != 200:
        print('sendErr: '+r.url)
    else:
        print(r.text)
    return r.status_code
def resendDr():
    global url
    req = db.readDb.fileDr_fail(1)
    #print(req)
    
    for i in range(len(req)):
        print("Sending :", req[i]["nama"])
        try:
            dataDb=str(req[i]["status"])
            d=json.loads(dataDb)
            #print(jsond)
            r = requests.post(url, data=d)
            if r.status_code == 200:
                print("Permintaan berhasil. Status code:", r.status_code)
                fileName=req[i]["nama"]+".zip"
                try:
                    resp=DFRUploadFile(fileName,d)
                    if(resp==200):
                        db.updateDb.upd_flag(1,req[i]["id"])
                except:
                    print("fail toupload file")
            else:
                print("Permintaan gagal. Status code:", r.status_code)
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
                    

if __name__ =="__main__":
    while True:
        clearDr()
        resendDr()    
        time.sleep(10)
