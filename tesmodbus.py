from pymodbus.client.sync import ModbusSerialClient as ModbusClient

for i in range(8):
    print('/dev/ttyUSB'+str(i))
    buff_client = ModbusClient(method='rtu', port='/dev/ttyUSB'+str(i),
                           stopbits=1, bytesize=8, parity='N', baudrate=19200, timeout=.1000)

    connection = buff_client.connect()        
    if connection:
        baca = buff_client.read_holding_registers(address = 0,count =10,unit= 1)
    
        if baca.isError():
            print('Port'+str(i)+' RS-485 tidak dapat menerima data')
        else:
            print(baca)
    else:
        print('RS485 tidak terhubung')