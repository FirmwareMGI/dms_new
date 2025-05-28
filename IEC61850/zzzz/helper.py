#from msilib import datasizemask
from re import T
import struct
import array
import binascii
class iecHelper:
    def parseDataFloat(x) :
        serRespond=x[-4:]
        fhex=""
        for i in range(4):
        #     dthex=(serRespond[reg[i]+j])
            fhex+="%02x" % serRespond[i]
        # dataMon= struct.unpack(('!f',bytes.fromhex(x[:4])))
        dataFloat=struct.unpack('!f', bytes.fromhex(fhex))[0]
        return dataFloat
    def convertRequest(req,domainId,itemId):
        #domainId=b'SRGN_1Measurements'
       # itemId =b'SecFouMMXU1$CF$TotPF$db'
        arrItemId=list(itemId)
        arrdomainId=list(domainId)
        arrdomainId.insert(0,len(domainId))#menambahkan len
        arrdomainId.insert(0,26)#menambahkan 0x1a
        arrItemId.insert(0,len(itemId))#menambahkan len
        arrItemId.insert(0,26)#menambahkan 0x1a
        reqData=req+arrdomainId+arrItemId
        totalData=len(reqData)
        high, low = bytesx(totalData)
        reqData[2]=high
        reqData[3]=low
        reqData[12]=totalData-13
        reqData[14]=totalData-15
        reqData[19]=totalData-20
        reqData[21]=totalData-22
        reqData[27]=totalData-28
        reqData[32]=totalData-33
        reqData[34]=totalData-35
        reqData[36]=totalData-37
        reqData[38]=totalData-39
        reqData[40]=totalData-41
        #print(reqData)
        return reqData
def bytesx(integer):
    return divmod(integer, 0x100)

