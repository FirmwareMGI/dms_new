import mysql.connector
from pymysqlpool.pool import Pool
import pymysql

conn = pymysql.connect(
    host='localhost',
    user='dms', 
    password='mgi',
    db='dms',
)

#pool = Pool(host='localhost', port=3306,user='root', db='dms')
pool = Pool(host='localhost', port=3306, user='dms', password='mgi', db='dms')
# db = conn
# db = [0]*5
# for i in range(3):
#     db[i] = pool.get_conn()
# print(db)
# print(conn)
# url = []

db = pool.get_conn()


def queryData(x, query):
    global db
    global pool
    try:
        db.ping(reconnect=True)
        cursor = db.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        db.commit()
        cursor.close()
        pool.release(db)
        db = pool.get_conn()
        # print(result)
        return result

    except NameError:
        print(NameError)

# db = [0]*5
# for i in range(3):
#     db[i] = pool.get_conn()


# def queryData(x, query):
#     global db
#     global pool
#     try:
#         db[x].ping(reconnect=True)
#         cursor = db[x].cursor()
#         cursor.execute(query)
#         result = cursor.fetchall()
#         print(result)
#         db[x].commit()
#         cursor.close()
#         pool.release(db[x])
#         db[i] = pool.get_conn()
#         # print(result)
#         return result
#     except NameError:
#         print(NameError)


class readDb:
    def m_file_iec_read_by_active(x):
        query = f"select a.*,b.ipserver from m_file_iec a  cross join network b where active =1"
        try:
            results = queryData(x, query)
            return results
        except:
            print("eror query")

    def m_file_iec_read_by_ID(x, id_device):
        query = f"select domain_id,item_id,alias, active, id_device, data_type from m_file_iec  where active =1 and id_device = {id_device}"
        try:
            results = queryData(x, query)
            return results
        except:
            print("eror query")

    def device_list_by_mode(x):
        query = f"select * from device_list where mode=2"
        try:
            results = queryData(x, query)
            return results
        except:
            print("eror query")

    def device_list(x):
        query = f"select * from device_list"
        try:
            results = queryData(x, query)
            return results
        except:
            print("eror query")

    def device_list_type2(x):
        query = f"select id_device,type,port_address,rack_location,ip_address,iec_file,disturbance_type from device_list WHERE port_type=2"
        try:
            results = queryData(x, query)
            # print(results)
            return results
        except:
            print("eror query")

    def filedr(x, id_device):
        if str(id_device) == 'all':
            query = f"SELECT id_device, data,jumlah_data, extensionDR from filedr WHERE port_device=2"
        else:
            strId = str(id_device)
            query = f"SELECT id_device, data,jumlah_data, extensionDR from filedr WHERE port_device=2 AND id_device = {strId}"
        try:
            results = queryData(x, query)
            return results
        except:
            print("eror query")

    def data_iec_filedr(x, id_device):
        if str(id_device) == 'all':
            query = f"SELECT * from data_iec_filedr"
        else:
            strId = str(id_device)
            query = f"SELECT * from data_iec_filedr WHERE id_device = {strId}"
        try:
            results = queryData(x, query)
            return results
        except:
            print("eror query")

    def network_mqtt(x):
        query = f"select ipserver, mqtt_server, mqtt_username, mqtt_pass, mqtt_port from network b "
        try:
            results = queryData(x, query)
            return results
        except:
            print("eror query")

    def network(x):
        query = f"select * from network "
        try:
            results = queryData(x, query)
            return results
        except:
            print("eror query")

    def m_mesin(x):
        query = f"select * from m_mesin "
        try:
            results = queryData(x, query)
            return results
        except:
            print("eror query")

class insertDb:
    def __init__(self,index):
        self.index = index
    def m_file_iec_insert(x,domainId,itemId,ip,relayId):
        #query= f"insert into m_file_iec (domain_id,item_id,relay_id,ip_address) values('{domainId}','{itemId}','{relayId}','{ip}')"
        query= f"insert into it_file_iec (domain_id,item_id,id_device,ip_address) values('{domainId}','{itemId}','{relayId}','{ip}')"
        
        #print(query)
        
        try:
           results =queryData(x,query)
           return results
        except:
            print("eror query")
    def m_fileDR_temp(x,port,id_device,status,flag,nameFile):
        status=str(status).replace("'", "\"")
        nameFile = str(nameFile)
        #query= f"insert into it_file_iec (domain_id,item_id,id_device,ip_address) values('{domainId}','{itemId}','{relayId}','{ip}')"
        query = f"INSERT INTO fileDR_temp (port_device,id_device,status,flag,nama) values('{port}','{id_device}','{status}','{flag}','{nameFile}')"
        print(query)
        
        try:
           results =queryData(x,query)
           return results
        except:
            print("eror query")


class writeDb:
    def update_data_iec_filedr(x, id_device, listfile, savedPath):
        strId = str(id_device)
        query = f"update data_iec_filedr SET listDR = '" + \
            str(listfile) + \
            "'WHERE id_device='"+str(id_device)+"'"
        # print(query)
        try:
            results = queryData(x, query)
            # print(results)
            return results
        except NameError:
            print("query Error"+NameError)

    def updfileDR(x, listFile, waktu, lokasi, id_device):
        listFileString = [sublist[0] for sublist in listFile]
        jumlahFile = len(listFileString)
        listFileString = '|'.join(listFileString)
        data = f"update fileDR SET data = '"+str(listFileString)+"', jumlah_data = '"+str(jumlahFile)+"', status = '"+str("-")+"', waktu = '"+str(
            waktu)+"', lokasi = '"+str(lokasi)+"' WHERE port_device=2 AND id_device='"+str(id_device)+"'"
        # query=f"update fileDR set kondisi = {kondisi},flag_kondisi={flag_kondisi} where port={port}"
        test = f"update fileDR SET data = 'b', jumlah_data = 'b', status = 'b', waktu = 'b', lokasi = 'b' WHERE port_device=0 AND id_device=1"
        try:
            results = queryData(x, data)
            # print(results)
            return results
        except NameError:
            print("query Error"+NameError)

    def updfileDRNEW(x, id_device, listFile):
        # print(listFile)
        listFileString = ''
        listExt = ''
        for index, v in enumerate(listFile):
            if index == 1:
                listFileString = v
            if index == 2:
                listExt = v
        # listFileString = [sublist[1] for sublist in listFile]
        jumlahFile = len(listFileString)
        listFileString = '|'.join(listFileString)
        # listExt = [sublist[2] for sublist in listFile]
        listExt = '|'.join(listExt)
        data = f"update fileDR SET data = '"+str(listFileString)+"', jumlah_data = '"+str(
            jumlahFile)+"'WHERE port_device=2 AND id_device='"+str(id_device)+"'"
        # query=f"update fileDR set kondisi = {kondisi},flag_kondisi={flag_kondisi} where port={port}"
        try:
            results = queryData(x, data)
            # print(results)
            return results
        except NameError:
            print("query Error"+NameError)

    def inserfileDREmpty(x, id_device):
        data = f"INSERT INTO fileDR(port_device, id_device, data, jumlah_data, status, waktu, lokasi) VALUES('2', '"+str(
            id_device)+"', '""','"+str(0)+"', '""', '""', '""') "
        # query=f"update fileDR set kondisi = {kondisi},flag_kondisi={flag_kondisi} where port={port}"
        try:
            results = queryData(x, data)
            # print(results)
            return results
        except NameError:
            print("query Error"+NameError)

    def inserfileDR(x, id_device, listFile):
        # print(listFile)
        listFileString = ''
        listExt = ''
        for index, v in enumerate(listFile):
            if index == 1:
                listFileString = v
            if index == 2:
                listExt = v
        # listFileString = [sublist[1] for sublist in listFile]
        jumlahFile = len(listFileString)
        listFileString = '|'.join(listFileString)
        # listExt = [sublist[2] for sublist in listFile]
        listExt = '|'.join(listExt)

        # data = f"update fileDR SET data = '"+str(listFileString)+"', jumlah_data = '"+str(jumlahFile)+"', status = '"+str("-")+"', waktu = '"+str(
        #     waktu)+"', lokasi = '"+str(lokasi)+"' WHERE port_device=2 AND id_device='"+str(id_device)+"'"
        # query=f"update fileDR set kondisi = {kondisi},flag_kondisi={flag_kondisi} where port={port}"

        data = f"INSERT INTO fileDR(port_device, id_device, data, jumlah_data, deviceDR, extensionDR) VALUES('2', '"+str(
            id_device)+"', '"+str(listFileString)+"','"+str(jumlahFile)+"', '""', '"+str(listExt)+"') "
        # query=f"update fileDR set kondisi = {kondisi},flag_kondisi={flag_kondisi} where port={port}"
        print(data)
        try:
            results = queryData(x, data)
            # print(results)
            return results
        except NameError:
            print("query Error"+NameError)
