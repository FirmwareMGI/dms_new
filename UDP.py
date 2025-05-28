# import socket
# 
# 
# while True:
#     UDP_IP_ADDRESS = "192.168.43.160"
#     UDP_PORT_NO = 6789
#     sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#     # address = ((UDP_IP_ADDRESS,UDP_PORT_NO))
#     sock.bind((UDP_IP_ADDRESS,UDP_PORT_NO))
#     data,addr = sock.recvfrom(1024)
# 
#     print(data)
#     print(addr)


import serial
import socket
import time

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
address = ("192.168.43.160",6789)
sock.bind(address)

ser = serial.Serial('/dev/ttyUSB0', baudrate = 19200,timeout=1)

while True:
    data,addr = sock.recvfrom(1024)
    if str(data) != "":
        ser.write(bytes(data))
        print(bytes(data))
#         print(addr)
        
    arduinoData = ser.readline()
    
    sock.sendto(arduinoData,address)
    print(arduinoData)

    