import time
import db
import ex_scl_loaderV2 as loader
import json
import os

path="/home/mgi/gipat-config/public/assets/TYPE"
scl_path="/home/mgi/gipat-config/public"


def netmask_to_cidr(m_netmask):
    """
    Convert a netmask in dotted decimal format to CIDR notation.
    Args:
        m_netmask (str): The netmask in dotted decimal format (e.g., 
    """
    return(sum([ bin(int(bits)).count("1") for bits in m_netmask.split(".") ]))

def changeNet():
    """
    Change network configuration based on the database settings.
    This function reads the network settings from the database, updates the network configuration using nmcli,
    and restarts the LAN connection.
    """
    net = db.readDb.readDataTabel(1,"network")
    if net[0]["flag"]==1:
        db.updateDb.updData(1,"network","flag",0,"flag",1)
        ip = net[0]["iplocal"]
        # print(net)
        gateway = net[0]["gateway"]
        netmask = net[0]["netmask"]
        dns = net[0]["dns"]
        prefik = netmask_to_cidr(netmask)
        nmtuiCommand = f"sudo nmcli con mod 'Sambungan kabel 1' ipv4.addresses {ip}/{prefik} ipv4.gateway {gateway} ipv4.dns {dns} ipv4.method 'manual'"
        # print(nmtuiCommand)
        os.popen(nmtuiCommand)
        time.sleep(2)
        restart_LAN = 'sudo nmcli c down "Sambungan kabel 1" && sudo nmcli c up "Sambungan kabel 1"'
        os.popen(restart_LAN)
        # print("LAN RESTARTED")
    
while True:
    """
    Main loop to process SCL files for devices.
    This function retrieves the device list and configuration from the database,
    checks if the IEC program needs to be restarted, and processes each device's SCL file.
    If the SCL file is successfully processed, it updates the device's SCL flag in the database.
    If an error occurs during processing, it updates the SCL flag to indicate failure.
    """
    device_list=db.readDb.device_list(1)
    cfg = db.readDb.flag_config(1)
    m_mesin = db.readDb.m_mesin(1)
    machine_code = m_mesin[0]["kode_mesin"]
    # print("machine code: ", machine_code)
    cfg_flag=cfg[0]["flag_program_iec"]
    print(cfg_flag)
    changeNet()
    # if(cfg_flag==1):
    #     os.system("sudo systemctl restart iecmonitor.service")
        
    #     db.updateDb.flag_config(1,0)
    #     time.sleep(5)
    #print(cfg_flag)
    for i in range(len(device_list)):
       # print(device_list[i]['scl_flag'])
        if(device_list[i]['scl_flag']==1):
            print("upload woy")
            if(device_list[i]['scl_name']!=None):
                id_device=device_list[i]['id_device']
                ip_device=str(device_list[i]['ip_address'])
                port_device=str(device_list[i]['port_number'])
                port_id = str(device_list[i]['port_group_id'])
                
                # loc=scl_path+"/"+port_id+"/"+device_list[i]['scl_name']
                loc = scl_path + device_list[i]['scl_name']
                output_path = "{path}/{port_id}".format(
                    path=path, 
                    port_id=port_id
                )

                print("processing scl file: ", loc)
                try:
                    prosecessSuccess = loader.process_single_scl_file(
                        scl_path=loc,
                        output_dir=output_path, 
                        ip=ip_device, 
                        port=port_device, 
                        machine_code = machine_code, 
                        id_device =id_device,
                        port_id=port_id) 
                    if not prosecessSuccess:
                        print("gagal baca scl")
                        db.updateDb.scl_flag(1,3,id_device)
                        continue
                        
                    db.updateDb.scl_flag(1,2,id_device)
                    # print(id_device)
                except Exception as e:
                    print(e)
                    # print(NameError)
                    print("gagal baca scl")
                    db.updateDb.scl_flag(1,3,id_device)
                #print(all_domain)
            time.sleep(1)
    time.sleep(2)
