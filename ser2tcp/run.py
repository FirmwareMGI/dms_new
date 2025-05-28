
import server_manager as _server_manager
import serial_proxy as _serial_proxy
import sys as _sys
import argparse as _argparse
import logging as _logging
import signal as _signal
import json as _json
import serial_proxy as _serial_proxy
import server_manager as _server_manager
import string
from num2words import num2words


def sigterm_handler(_signo, _stack_frame):
    """Raises SystemExit(0)"""
    _sys.exit(0)


_signal.signal(_signal.SIGTERM, sigterm_handler)
_signal.signal(_signal.SIGINT, sigterm_handler)

_logging.basicConfig(
    format='%(levelname).1s: %(message)s (%(filename)s:%(lineno)s)')
log = _logging.getLogger('ser2tcp')

user = [['/dev/ttyUSB0', '19200', '8', 'N', '1', '2001'],
        ['/dev/ttyUSB1', '19200', '8', 'N', '1', '2002']]

relay_final = ['MICOM P123', 'MICOM P141']
name_micom = ['P123', 'P141']
index_micom = ['0', '1']
mode_micom = ['0', '1']

old_config = []
new_config = []

for i in range(0, len(relay_final)):
    if int(mode_micom[i]) == 1:
        new_config.append({'serial': {'port': user[i][0], 'baudrate': int(user[i][1]), 'parity': user[i][3], 'stopbits': user[i][4]},
                           'servers': [{'address': '0.0.0.0', 'port': int(user[i][5]), 'protocol': 'TCP'}]})
print(new_config)
servers_manager = _server_manager.ServersManager()

for config in new_config:
    servers_manager.add_server(_serial_proxy.SerialProxy(config, log))
print(config)
# while True:
#     servers_manager.process()
# servers_manager.close()
i2 = 0
while True:
    for i in range(0, len(relay_final)):
        print('Not remote')
        # for configg in old_config:
        #     servers_manager.add_server(
        #         _serial_proxy.SerialProxy(configg, log))
        # print(config)
        if int(mode_micom[i]) == 1:
            i2 += 1
            print('remote')
            servers_manager.process()
            print(i2)
            if i2 == 100:
                servers_manager.close()
servers_manager.close()
