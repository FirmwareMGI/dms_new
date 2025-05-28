from ast import Name

import asyncio
import json
#import grequests
from time import gmtime, strftime
import requests
from datetime import datetime
from pymysqlpool.pool import Pool
import pymysql.cursors
pool = Pool(host='localhost', port=3306, user='dms', password='mgi', db='dms')
db=[0]*5
for i in range(3):
    db[i] = pool.get_conn()

url=[]
def queryData(x,query):
    global db
    global pool
    try:
        db[x].ping(reconnect=True)
        cursor = db[x].cursor()
        cursor.execute(query)
        result = cursor.fetchall()     
        db[x].commit()
        cursor.close()
        pool.release(db[x])
        db[i] = pool.get_conn()
        #print(result)
        return result 
    
    except NameError:
        print(NameError)
class updateDb:
    def updData(x,tabel,row,val,where,val2):
        query =f"update {tabel} set {row} = {val} where {where} = {val2}"
       # print(query)
        try:
            results =queryData(x,query)
            return results
        except NameError:
            print("query Error"+NameError)
    def upd_flag(x,id):
        query= f"UPDATE fileDR_temp set flag = 1 where id = "+str(id)
        print(query)
        try:
            results =queryData(x,query)
            return results
        except:
            print("eror query")
    def scl_flag(x,flag,id):
        query= f"UPDATE device_list set scl_flag = "+str(flag) +" where id_device = "+str(id)
        print(query)
        try:
            results =queryData(x,query)
            return results
        except:
            print("eror query")
    def flag_config(x,flag):
        query= f"UPDATE flag_config set flag_program_iec  = {flag}"
        print(query)
        try:
            results =queryData(x,query)
            return results
        except:
            print("eror query")
           
    def data_iec_filedr_update(x, relayId, listFile):
        # Split the string by "|"
        countData = listFile.split("|")
        # Count the number of items
        countList = len(countData)
        query = f"UPDATE data_iec_filedr SET jumlahDR = '{countList}', listDR = '{listFile}' WHERE id_device = '{relayId}'"
        try:
            results = queryData(x, query)
            return results
        except Exception as e:
            print(f"Error executing update query: {e}")

class readNUpdateDb:
    def network(x):
        query= f"select a.*,b.ipserver from m_file_iec a  cross join network b where active =1"
        try:
           results =queryData(x,query)
           return results
        except:
            print("eror query")


class readDb:
    def readDataTabel(x,tb):
        query= f"select * from {tb}"
        try:
           results =queryData(x,query)
           return results
        except:
            print("eror query")
    def fileDr_fail(x):
        query = "SELECT * FROM fileDR_temp WHERE flag =0 and time_stamp <= DATE_SUB(NOW(), INTERVAL 10 MINUTE)"
        try:
           results =queryData(x,query)
           return results
        except:
            print("eror query")
        
    def last_fileDr(x):
        query = "SELECT * FROM fileDR_temp WHERE flag =1 and time_stamp <= DATE_SUB(NOW(), INTERVAL 1 MONTH)"
        try:
           results =queryData(x,query)
           return results
        except:
            print("eror query")
            
    def m_file_iec_read_by_active(x):
        query= f"select a.*,b.ipserver from m_file_iec a  cross join network b where active =1"
        try:
           results =queryData(x,query)
           return results
        except:
            print("eror query")
    def m_file_iec_read_by_active(x):
        query= f"select a.*,b.ipserver from m_file_iec a  cross join network b where active =1"
        try:
           results =queryData(x,query)
           return results
        except:
            print("eror query")
    def flag_config(x):
        query= f"Select * from flag_config"
        try:
           results =queryData(x,query)
           return results
        except:
            print("eror query")
    def device_list_by_mode(x):
        query= f"select * from device_list where mode=2"
        try:
            results =queryData(x,query)
            return results
        except:
            print("eror query")
    def device_list(x):
        query= f"select * from device_list "
        try:
            results =queryData(x,query)
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
    
    def data_iec_filedr(x, id_device):
        if str(id_device) == 'all':
            query = f"SELECT * from data_iec_fileDr"
        else:
            strId = str(id_device)
            query = f"SELECT * from data_iec_fileDr WHERE id_device = {strId}"
        try:
            results = queryData(x, query)
            return results
        except:
            print("eror query")

    def data_iec_filedr_all(x):
        query = "SELECT * FROM data_iec_filedr"
        try:
            results = queryData(x, query)  # Assuming queryData fetches and returns results
            return results
        except Exception as e:
            print(f"Error executing read all query: {e}")
            return None  # Return None on error

    
    def network_mqtt(x):
        query= f"select ipserver, mqtt_server, mqtt_username, mqtt_pass, mqtt_port from network b "
        try:
            results =queryData(x,query)
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
    def data_iec_filedr_insert(x,relayId, listFile):
        countData = listFile.split("|")
        # Count the number of items
        countList = len(countData)        
        query = f"INSERT INTO data_iec_filedr (id_device, jumlahDR, listDR) VALUES ('{relayId}', '{countList}', '{listFile}')"
        try:
            results = queryData(x, query)
            return results
        except Exception as e:
            print(f"Error executing query: {e}")
            
class deleteDb:
    def __init__(self,index):
        self.index = index
    def fileDr_temp_by_id(x,id):
        query= f"delete from fileDR_temp where id='{id}'"
        try:
           results =queryData(x,query)
           return results
        except:
            print("eror query")
    def m_file_iec_delete_by_domain_id(x,domainId):
        query= f"delete from  it_file_iec where domain_id='{domainId}'"
        #print(query)
        
        try:
           results =queryData(x,query)
           return results
        except:
            print("eror query")
    def it_file_iec_delete_by_id(x,Id):
        query= f"delete from  it_file_iec where domain_id='{Id}'"
        #print(query)
        
        try:
           results =queryData(x,query)
           return results
        except:
            print("eror query")
   


