import time
import db
import parsexml3
import json
# scl_path="C:/xampp/htdocs/dms_setting/upload"
# path="C:/xampp/htdocs/dms_setting/assets/scl/"
scl_path="/var/www/html/dms_setting/upload"
path="/var/www/html/dms_setting/assets/scl/"
def saveToFile(data, filePath):
        global path
        f = open(path+filePath+".json", "w")
        f.write(data)
        f.close()
def toJson(data,name):
    global file_path
    jsonData=[]
    #print(data)
    for i in range(len(data)):
        buf = data[i].split("-")
        x={"id":f"{i}","domain_id":buf[0],"item_id":buf[1],"all":buf[0]+"$"+buf[1]}
        jsonData.append(x)
    data= json.dumps(jsonData)
    saveToFile(data, name)
    print(name)
while True:
    device_list=db.readDb.device_list(1)
    print("run")
    #print(device_list)
    for i in range(len(device_list)):
        #print(device_list[i]['id_device'])
        if(device_list[i]['scl_flag']==1):
            if(device_list[i]['scl_name']!=None):
                loc=scl_path+"/"+device_list[i]['scl_name']
                id_device=device_list[i]['id_device']
                try:
                    #ied1=loader.IED_PARSING(loc)
                    print("begin parse")
                    all_domain = parsexml3.IED_PARSING(0).getAllDomain(loc)
                    print(all_domain)
                    toJson(all_domain,device_list[i]['id_device'])
                    db.updateDb.scl_flag(1,2,id_device)
                    print(id_device)
                except: 
                     #print(NameError)
                     print("gagal baca scl")
                     db.updateDb.scl_flag(1,3,id_device)
                #print(all_domain)
            time.sleep(0.1)
    time.sleep(3)