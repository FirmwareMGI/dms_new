import db
import os
import time
def saveFile(loc,data):
    f = open(f'/home/pi/dms/DMSv1.2/network/{loc}','w')
    f.write(data)
    f.close()
def changeNet():
    net = db.readDb.readDataTabel(1,"network")
    db.updDb.updData(1,"network","flag",0,"flag",1)
    ip = net[0]["iplocal"]
    print(net)
    gateway = net[0]["gateway"]
    netmask = net[0]["netmask"]
    dns = net[0]["dns"] 
    prefik = net[0]["prefik"]
    dhcp = net[0]["dhcp"]   
    dataSetting=f"\
hostname \n\
clientid \n\
persistent \n\
option rapid_commit \n\
option domain_name_servers, domain_name, domain_search, host_name \n\
option classless_static_routes \n\
option ntp_servers \n\
option interface_mtu \n\
require dhcp_server_identifier \n\
slaac private \n\
#ipbaru \n\
#set ip dari wizard \n\
interface eth0 \n\
static ip_address={ip}/{prefik}\n\
static ip6_address=fd51:42f8:caae:d92e::ff/64 \n\
static routers={gateway}\n\
static domain_name_servers={dns}"
    saveFile('ipstatic.cfg',dataSetting)
    print(dhcp)
    program=""
    print("BEFORE COPY DHCPCD")
    if dhcp==0:
        program = 'sudo cat /home/pi/dms/DMSv1.2/network/ipstatic.cfg > /etc/dhcpcd.conf'
        print("ip static")
    elif dhcp==1:
        program ='sudo cat /home/pi/dms/DMSv1.2/network/ipdynamic.cfg > /etc/dhcpcd.conf'
    os.popen(program)
    print("AFTER COPY DHCPCD")
    time.sleep(2)
    program ='sudo ifconfig eth0 down'
    os.popen(program)
    time.sleep(15)
    program ='sudo ifconfig eth0 up'
    os.popen(program)
    print("LAN RESTARTED")
    
#changeNet()