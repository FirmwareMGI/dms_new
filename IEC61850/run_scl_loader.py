import time
import db
import ex_scl_loader as loader
import json
import os

scl_path="/var/www/html/dms_setting/upload"
path="/var/www/html/dms_setting/assets/scl/"
def netmask_to_cidr(m_netmask):
    return(sum([ bin(int(bits)).count("1") for bits in m_netmask.split(".") ]))
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
    
def toJson2(jsonData,name):
    global file_path
    #print(data)
    data= json.dumps(jsonData)
    saveToFile(data, name)
    print(name)

def changeNet():
    net = db.readDb.readDataTabel(1,"network")
    if net[0]["flag"]==1:
        db.updateDb.updData(1,"network","flag",0,"flag",1)
        ip = net[0]["iplocal"]
        print(net)
        gateway = net[0]["gateway"]
        netmask = net[0]["netmask"]
        dns = net[0]["dns"]
        
        prefik = netmask_to_cidr(netmask)
        dhcp = net[0]["dhcp"]   

        nmtuiCommand = f"sudo nmcli con mod 'Sambungan kabel 1' ipv4.addresses {ip}/{prefik} ipv4.gateway {gateway} ipv4.dns {dns} ipv4.method 'manual'"
        print(nmtuiCommand)
        os.popen(nmtuiCommand)

        time.sleep(2)
        #program ='sudo ifconfig eth0 down'
        #os.popen(program)
        #time.sleep(15)
        #program ='sudo ifconfig eth0 up'
        #os.popen(program)
        restart_LAN = 'sudo nmcli c down "Sambungan kabel 1" && sudo nmcli c up "Sambungan kabel 1"'
        os.popen(restart_LAN)
        print("LAN RESTARTED")
    
while True:
    device_list=db.readDb.device_list(1)
    cfg = db.readDb.flag_config(1)
    
    cfg_flag=cfg[0]["flag_program_iec"]
    print(cfg_flag)
    changeNet()
    if(cfg_flag==1):
        print("restart program")
      
        #os.system("pm2 restart 3")
        #os.system("pm2 restart 4")
        #os.system("pm2 restart all")
        os.system("sudo systemctl restart iecmonitor.service")
        
        db.updateDb.flag_config(1,0)
        time.sleep(5)
    #print(cfg_flag)
    for i in range(len(device_list)):
       # print(device_list[i]['scl_flag'])
        if(device_list[i]['scl_flag']==1):
            print("upload woy")
            if(device_list[i]['scl_name']!=None):
                loc=scl_path+"/"+device_list[i]['scl_name']
                print(loc)
                id_device=device_list[i]['id_device']
                try:
                    ied1=loader.IED_PARSING(loc)
                    datasets = ied1.getDataSets()
                    for ds in datasets:
                        print(f"LD: {ds['LD']}, Dataset Name: {ds['dataset_name']}")
                    #all_domain = ied1.getAllDomainID()
                    #print(all_domain)
                    #toJson(all_domain,device_list[i]['id_device'])
                    print(ied1.all_domain_dict)
                    toJson2(ied1.all_domain_dict,device_list[i]['id_device'])
                    db.updateDb.scl_flag(1,2,id_device)
                    print(id_device)
                except Exception as e:
                    print(e)
                    # print(NameError)
                    print("gagal baca scl")
                    db.updateDb.scl_flag(1,3,id_device)
                #print(all_domain)
            time.sleep(1)
    time.sleep(5)
