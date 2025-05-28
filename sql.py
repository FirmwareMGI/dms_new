# import mysql.connector
# 
# mydb = mysql.connector.connect(
#     host = "localhost",
#     user = "admin",
#     password = "mgi",
#     database = "dms"
#     )
# 
# mycursor = mydb.cursor()
# sql = "SELECT * FROM dataRegister WHERE port_device=0 AND id_device=0 "
# mycursor.execute(sql)
# dbDR = mycursor.fetchall()
# mydb.commit()

# mycursor = mydb.cursor()
# sql = "DELETE FROM dataRegister"
# mycursor.execute(sql)
# mydb.commit()

# if len(dbDR) == 0:
#     sql = "INSERT INTO dataRegister(port_device, id_device, geser_register, geser_param, period, id_pool, jumlah_data, indexDR) VALUES('"+str(0)+"', '"+str(0)+"', '"+str(0)+"', '"+str(0)+"', '"+str(0)+"','"+str(30)+"', '"+str(4800)+"', '"+str(0)+"') "
#     mycursor.execute(sql)
#     mydb.commit()
# else:
#     for i in dbDR:
#         print(i[7])
    
fileDR = [[[1,2,3,4,5,6,7,8,9,10],[11,12,13,14,15,16,17,18,19,20]],[21,22,23,24,25,26,27,28,29,30]]

data = 11

for i in range(1,10):
    fileDR[0][0][i-1] = fileDR[0][0][i]
    
    if i == 9:
        fileDR[0][0][i] = data
        
print(fileDR[0][0])