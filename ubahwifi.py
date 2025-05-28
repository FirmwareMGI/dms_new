import os

def network_setup(ip_add):
        os.system('sudo ifconfig eth0 down')
        os.system('sudo ifconfig eth0 '+ip_add)
#         os.system('sudo ifconfig etho netmask '+net_mask)
#         os.system('sudo ifconfig eth0 broadcast '+broad_add)
        os.system('sudo ifconfig eth0 up')

network_setup('192.168.0.43')