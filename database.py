import mysql.connector
import datetime


mydb = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="mgi",
  database="dms"
)

mycursor = mydb.cursor()

sql = "SELECT DISTINCT it_ia.ia,it_ib.ib,it_ic.ic,it_ie.ie,it_f.f,it_relay.relay,it_ia.id_pool FROM it_ia \
    inner JOIN it_ib ON it_ib.period = it_ia.period\
    inner JOIN it_ic ON it_ic.period = it_ia.period\
    inner JOIN it_ie ON it_ie.period = it_ia.period\
    inner JOIN it_f ON it_f.period   = it_ia.period\
    inner JOIN it_relay ON it_relay.period = it_ia.period WHERE \
    it_ia.id_pool = '0'  and\
    it_ib.id_pool =  '0' and\
    it_ic.id_pool = '0' and\
    it_ie.id_pool =  '0' and\
    it_f.id_pool =  '0' and\
    it_relay.id_pool =  '0' and\
    it_ia.flag = 0  and\
    it_ib.flag = 0 and\
    it_ic.flag = 0 and\
    it_ie.flag = 0 and\
    it_f.flag = 0 and\
    it_relay.flag = 0\
    GROUP BY it_ia.period ORDER BY it_ia.period and\
    it_ib.period and\
    it_ic.period and\
    it_ie.period and\
    it_f.period and\
    it_relay.period asc"

mycursor.execute(sql)
dbDR = mycursor.fetchall()


timeCurrent = datetime.datetime.now()


tes=[0,0,0,0,0,0,0]
tes1=''
tes2=''
count = 0
timefreq = 0 
for i in range(0,len(dbDR)) :
  for j in range(0,(len(dbDR[i]))) :
    tes[j] = dbDR[i][j].split('*')
    
  for k in range(0,len(tes[0])):
      count += 1
      tes[5][k] = ','.join(str(bin(int(tes[5][k])))[:1:-1]+"000000000")
      
      tes2 = tes[0][k]
      if tes2[0] == '-':
          tes[0][k] = '-'+str(tes[0][k])[1:].rjust(5,'0')
      else :
          tes[0][k] = str(tes[0][k]).rjust(6,'0')
      
      tes2 = tes[1][k]
      if tes2[0] == '-':
          tes[1][k] = '-'+str(tes[1][k])[1:].rjust(5,'0')
      else :
          tes[1][k] = str(tes[1][k]).rjust(6,'0')
          
      tes2 = tes[2][k]
      if tes2[0] == '-':
          tes[2][k] = '-'+str(tes[2][k])[1:].rjust(5,'0')
      else :
          tes[2][k] = str(tes[2][k]).rjust(6,'0')    
          
      tes2 = tes[3][k]
      if tes2[0] == '-':
          tes[3][k] = '-'+str(tes[3][k])[1:].rjust(5,'0')
      else :
          tes[3][k] = str(tes[3][k]).rjust(6,'0')
      
      tes1+= str(count).rjust(10,'0')+ ","+str(timefreq).rjust(10,'0')+","+str(tes[0][k])+ ","+ str(tes[1][k])+ ","+ str(tes[2][k])+ ","+ str(tes[3][k])+ ","+ str(int(10000 - (int(tes[4][k])/125*1000))).rjust(6,'0')+ ","+ str(tes[5][k])+""+"\n"
      timefreq +=int(tes[4][k])
      
print(tes1)
f = open("/home/pi/Desktop/DMSv1.2/fileDR/"+str(timeCurrent)+".dat","w")
f.write(tes1)
f.close()

tes1 = ''
count = 0


waktu=''

mycursor = mydb.cursor()
sql = "SELECT * FROM it_cfg WHERE port_device='"+str(0)+"' AND id_device='"+str(0)+"' AND id_pool='"+str(0)+"' "
mycursor.execute(sql)
dbDR = mycursor.fetchall()
mydb.commit()

for i in dbDR:
    waktu = i[1]
    

tes1 += 'MiCOM '+str('P123') +' BXXXXXX V12.E,'+ str('1')+'\n'
tes1 += '19,5A,14D\n'
tes1 += '01,Ia,,, A,' +str('0.001768') +'0.000000,0,-32768,32767\n'
tes1 += '02,Ib,,, A,' +str('0.001768') +'0.000000,0,-32768,32767\n'
tes1 += '03,Ic,,, A,' +str('0.001768') +'0.000000,0,-32768,32767\n'
tes1 += '04,Ie,,, A,' +str('0.000432') +'0.000000,0,-32768,32767\n'
tes1 += '05,Frequency,,, Hz,' +str('0.010000') +'0.000000,0,-32768,32767\n'
tes1 += '01,Relay 1 (Trip),0\n'
tes1 += '02,Relay 2,0\n'
tes1 += '03,Relay 3,0\n'
tes1 += '04,Relay 4,0\n'
tes1 += '05,Relay 0 (Watchdog),0\n'
tes1 += '06,Relay 5,0\n'
tes1 += '07,Relay 6,0\n'
tes1 += '08,Relay 7,0\n'
tes1 += '09,Relay 8,0\n'
tes1 += '10,Digital Input 1,0\n'
tes1 += '11,Digital Input 2,0\n'
tes1 += '12,Digital Input 3,0\n'
tes1 += '13,Digital Input 4,0\n'
tes1 += '14,Digital Input 5,0\n'
tes1 += str('50') + '\n'
tes1 += str('0') + '\n'
tes1 += '0,'+str('4804') + '\n'
tes1 += str(waktu) + '\n'
tes1 += str(timeCurrent) + '\n'
tes1 += str('ASCII') + '\n'

f = open("/home/pi/Desktop/DMSv1.2/fileDR/"+str(timeCurrent)+".cfg","w")
f.write(tes1)
f.close()

tes1 = ''