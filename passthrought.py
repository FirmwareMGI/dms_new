import serial
import threading
import time

# register = [1,3,8,0,0,4,70,105]
# register = [104,3,3,104,64,1,0,65,22]
# register = [104,7,7,104,123,1,0,7,20,1,0,152,22]
# register = [104,7,7,104,91,1,0,7,20,5,0,124,22]
# register = [104,7,7,104,123,1,0,7,20,18,0,169,22]
# register = [104, 7, 7, 104, 123, 1, 0, 7, 20, 2, 191, 88, 22 ]
# register = [104, 7, 7, 104, 91, 1, 0, 7, 20, 1,  180, 44, 22  ]
# register = [104, 10, 10, 104, 123, 1, 0, 7,64, 1, 180, 42, 0, 0, 162, 22  ]

# register = [
#     [104,7,7,104,123,1,0,7,20,2,191,88,22],
#     [104,7,7,104,91,1,0,7,20,1,180,44,22],
#     [104,5,5,104,123,1,0,5,16,145,22],
#     [104,11,11,104,91,1,0,7,20,1,191,7,20,2,191,19,22],
#     [104,7,7,104,123,1,0,7,21,1,180,77,22],
#     [104,10,10,104,91,1,0,7,64,1,180,42,236,255,109,22],
#     [104,5,5,104,123,1,0,5,78,207,22],
#     [104,47,47,104,91,1,0,7,20,5,0,7,20,9,0,7,20,2,179,7,20,1,180,7,20,2,180,7,20,3,180,7,20,4,180,7,20,16,180,7,20,17,180,7,20,18,180,7,20,19,180,56,22],
#     [104,5,5,104,123,1,0,5,16,145,22],
#     [104,7,7,104,91,1,0,7,25,3,180,51,22],
#     [104,5,5,104,123,1,0,5,16,145,22],
#     [104,6,6,104,91,1,0,6,33,0,131,22],
# ]

flag = False
buffer = []
count = 0

ser = serial.Serial(port='/dev/ttyUSB0', baudrate=19200, parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0)


def Writeregister(panjangData, CF, addRTU, TypeID, VSQ, COT, addRTU1):
    register = [0]*(panjangData + 6)

    # ---------------header and CF-------------------
    register[0] = register[3] = 104
    register[1] = register[2] = panjangData
    register[4] = CF
    register[5] = addRTU

    # ----------------ASDU----------------------

    if panjangData >= 5:
        register[6] = TypeID
        register[7] = VSQ
        register[8] = COT

        panjangASDU = panjangData - 5

        register[9 + panjangASDU] = int(register[4])+int(register[5])+int(
            register[6])+int(register[7])+int(register[8])
        register[10 + panjangASDU] = 22

        for i in range(0, panjangASDU):
            register[9+i] = addRTU1[i]
            register[9 + panjangASDU] += register[9+i]

        register[9 + panjangASDU] = register[9 + panjangASDU] % 256

    elif panjangData == 3:
        register[6] = TypeID
        register[7] = (register[4] + register[5] + register[6]) % 256
        register[8] = 22

    ser.write(bytearray(register))
    print(register)


# Writeregister(7, 123, 1, 0, 7, 20, [18,180])
Writeregister(3, 64, 1, 0, 65, 0, [0])
# Writeregister(7, 91, 1, 0, 7, 20, [17,0])

while True:

    # if flag == True :
    #     Writeregister(register[count])
    #     flag = False

    if ser.in_waiting > 0:
        for arduinoData in ser.read():
            buffer.append(arduinoData)
            if arduinoData == 22:
                print(buffer)
                buffer.clear()
                flag = True
                count += 1
