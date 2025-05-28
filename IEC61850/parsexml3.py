import xmltodict
import pprint
import json
IEDNames=''
class IED_PARSING:

    def __init__(self,index):
        self.index = index
    def setIED(self,x,y):
        data=''
        for i in x:
           if(i["name"]==y):
               data=i['IED']
           
        return data
   
    def getIED(self,x):
        IEDName=[]
        IED=x
 
        if (type(IED) is dict):
            LD_list=IED["AccessPoint"]["Server"]["LDevice"]
            LN0= (LD_list[0]['LN0']['@lnType'])
            IEDName.append({"name":LN0,"IED":IED["@name"]})
            LN_buff=(LD_list[0]['LN'])
            for i in range(len(LN_buff)):
                LN=LN_buff[i]['@lnType']
                IEDName.append({"name":LN,"IED":IED["@name"]})
                #LN=(LD_list[1]['LN'])
               

        elif(type(IED) is list):
            for i in IED:
               
                IEDName.append(i["@name"])
       
        return IEDName

    def getAllDomain(self,path):
        global IEDName
        f=open(path, "r")
        pp = pprint.PrettyPrinter(indent=4)
        dtJson=xmltodict.parse(f.read())
        self.dt=dtJson['SCL']['DataTypeTemplates']
        #IEDName =self.getIED(dtJson['SCL']['IED'])
        #IED=dtJson['SCL']['IED']
       
      
        keys=list(self.dt.keys())
        LNodeType=self.dt['LNodeType']
        self.DOType =self.dt['DOType']
        
        all_domain = []
        for i in range(len(LNodeType)):
            DO_buf= (LNodeType[i]["DO"])
        
            if(type(DO_buf) is dict):
                
                DO_name=f"{DO_buf['@name']}"
                DO_type=DO_buf['@type']
               
                fc,GetType,rek=self.getDOType(DO_type)
                if len(DO_type)!=0:
                    for k in range (len(GetType)):
                        obj=(f"{fc[k]}.{DO_name}.{GetType[k]}").split(".")
                        if(len(obj[0])<1):
                            obj[0]="MX"
                        #if(obj[1].indexOf("/">-1)):
                        #    domain_id=obj[1].replace("", "Great") 
                        val=obj[1]+"-"+obj[2]+"$"+obj[0]+"$"+"$".join(obj[3:])
                        all_domain.append(val)
                        #print(val)
                        
                       
            elif(type(DO_buf) is list):
                for j in range(len(DO_buf)):
                    
                    DO_name=f"{LNodeType[i]['@id']}.{DO_buf[j]['@name']}"
                   
                    DO_type=DO_buf[j]['@type']
                    fc,GetType,rek=self.getDOType(DO_type)
                    if len(DO_type)!=0:
                        for k in range (len(GetType)):
                            obj=(f"{fc[k]}.{DO_name}.{GetType[k]}").split(".")
                            if(len(obj[0])<1):
                                obj[0]="MX"
                            val=obj[1]+"-"+obj[2]+"$"+obj[0]+"$"+"$".join(obj[3:])
                            all_domain.append(val)
                            #print(val)
        return all_domain

    def getDAType(self,x,y):
        dt=self.dt
        data=[]  
        DA= dt["DAType"]
        if(type(DA) is list):
            for i in DA: 
                keys=list(i.keys())
                if(i["@id"].find(y)>-1):
                    for j in (keys):
                        if(j!="@id"):
                            if(type(i[j]) is dict):
                                if(i[j].get("@name")!=None):
                                    res2=[]
                                    if(i[j].get("@type")!=None):
                                        res2= self.getDAType(keys,i[j]["@type"])
                                        if(len(res2)>0):
                                            for k in res2:
                                                res=i[j]["@name"]+'.'+k
                                                data.append(res)
                                    else:
                                        data.append(i[j]["@name"])
                            elif(type(i[j]) is list):
                                for k in (i[j]):
                                    data.append(k["@name"])
                                    if(k.get("@type")!=None):
                                        res2= self.getDAType(keys,k["@type"])
                                   
                                        if(len(res2)>0):
                                            for l in res2:
                                                res=k["@name"]+'.'+l
                                                data.append(res)
                                                
                                    else:
                                        data.append(k["@name"])

        return data
    def getDo2(self,x):
        DOType=self.DOType
        res =[]
        for i in DOType:
            
            if(i["@id"]==x):
                if(type(i["DA"]) is list):
                    for j in i["DA"]:
                        res.append(j)
        return res


    def getDOType(self,x):
        DOType=self.DOType
        data=[]
        fc=[]
        rek=[]
        for i in range(len (DOType)):
            if(DOType[i]["@id"]==x):
                #print(x)  
                Dokeys=list(DOType[i].keys())
                for j in range(len(Dokeys)):
                    if(Dokeys!="@id" or Dokeys!="@cdc"):
                        dt = DOType[i][Dokeys[j]]
                        if(type(dt) is list):
                            for k in (dt):
                                FC=""
                                if(k.get("@fc")!=None):
                                    FC=(k["@fc"])
                                if(k.get("@type")!=None):
                                    #print(k['@type'])
                                    types= k['@type']
                                    rek.append(types)
                                    if(types.find(".")>-1):
                                        res= self.getDo2(k['@type'])
                                        if(len(res)>0):
                                            for a in res:
                                                if (a.get('@type') !=None):
                                                    bufDAType=self.getDAType(a['@fc'],a['@type'])
                                                    if(len(bufDAType)>0):
                                                        for l in bufDAType:
                                                            DODA=f"{k['@name']}.{a['@name']}.{l}"
                                                            data.append(DODA)
                                                            fc.append(FC)
                                                            print(DODA)
                                                            #print(a['@type'])
                                                        

                                              
                                    else:
                                        bufDAType=self.getDAType(Dokeys[j],k['@type'])
                                        if(len(bufDAType)>0):
                                            for l in bufDAType:
                                                DODA=f"{k['@name']}.{l}"
                                                data.append(DODA)
                                                fc.append(FC)
                                                #print(l)
                                   

                                elif(k.get("@type")==None):
                                    DODA=f"{k['@name']}"
                                    data.append(DODA)
                                    fc.append(FC)
                                    #print(DODA)
        
        return fc,data,rek

#if __name__ =="__main__":
   #IED_PARSING(0).getAllDomain("dasp.icd")
#    IED_PARSING(0).getAllDomain("TEMPLATE.icd")
    


            

    
