import scl_loader
import scl_loader.scl_loader as scdl
from scl_loader import SCD_handler
from scl_loader import IED
from scl_loader import LD
from scl_loader import LN
from scl_loader import LN0
from scl_loader import DO
from scl_loader import DA
from scl_loader import SCDNode
from scl_loader import DataTypeTemplates
from scl_loader import ServiceType


#scl_path = "sampleModel_with_dataset.cid"
#scl_path="C:/xampp/htdocs/dms_setting/upload"
#scl_path = 'SEL-849 v2.iid'


class IED_PARSING:
    def __init__(self, filePath):
        self.LDFilter = "ALL"
        self.filePath = filePath
        self.scd = scl_loader.SCD_handler(self.filePath, False)
        self.iedName = self.scd.get_IED_names_list()
        self.iedName = self.iedName[0]
        self.ied = self.scd.get_IED_by_name(self.iedName)
        self.ip = self.scd.get_IP_Adr(self.iedName)
        self.ap = self.ip[1]
        self.ip = self.ip[0]
        self.LNobj = self.get_LN_obj()
        self.LD_name = self.get_LN_name()
        # self.LDobj = self.ied.get_LD_by_inst(LDFilter, self.ip)
        self.DAobj = self.ied.get_DA_leaf_nodes()
        self.all_domain_dict = []
        self.all_domain = self.getAllDomainID()

    # def getFC(self):
    #     print(self.ied.get_name_subtree('MX'))

    def getIEDName(self):
        return self.iedName, self.ap

    def getIP(self):
        return self.ip

    def get_LN_obj(self):
        return self.ied.get_children_LDs(self.ap)

    def get_LN_name(self):
        LN_name = [None] * len(self.LNobj)
        for i in range(len(self.LNobj)):
            LN_name[i] = self.LNobj[i].get_path_from_ld()
        return LN_name
    # def DO_obj(self):

    def DA_obj(self):
        # print(self.DAobj.keys())
        return [x for x in list(self.DAobj.keys()) if self.LDFilter in x]

    def DomainID(self):
        return self.iedName+self.LDFilter

    def makeItemID(self, DA, FC):
        obj = DA.split(".")
        obj[1] += '$' + FC
        return "$".join(obj[1:])

    def getItemID(self, FC=None):
        item = []
        if FC == None:
            for k, fc in self.DAobj.items():
                # if 'Measurement' in k:
                obj = k.split(".")
                obj[1] += '$' + fc.get_associated_fc()
                item.append("$".join(obj[1:]))
                # return item
        else:
            for k, fc in self.DAobj.items():
                if FC in k:
                    obj = k.split(".")
                    obj[1] += '$' + fc.get_associated_fc()
                    item.append("$".join(obj[1:]))
        return item

#    def getAllDomainID(self):
#        all_domain = []
#        idx = 0
#        for val in self.LD_name:
#            # print(self.iedName+val)
#            for k, fc in self.DAobj.items():
#                if val in k:
#                    obj = k.split(".")
#                    fcs = fc.get_associated_fc()
#                    obj[1] += '$' + fcs
#                    buffDict = {}
#                    buffDict['id'] = str(idx)
#                    buffDict['domain_id'] = self.iedName + val
#                    buffDict['item_id'] = "$".join(obj[1:])
#                    buffDict['all'] = buffDict['domain_id'] + '$'+buffDict['item_id']
#                    self.all_domain_dict.append(buffDict)
#                    idx += 1
#                    all_domain.append(self.iedName + val+"-"+"$".join(obj[1:]))
#        return all_domain

    def getDataSets(self):
        dataset_info = []
        ld_list = self.ied.get_children_LDs(self.ap)  # list of LD *names*
        for ld in ld_list:
            try:
                ld_inst = ld.get_ld_inst() if hasattr(ld, "get_ld_inst") else ld  # fallback
                ld_obj = self.ied.get_LD_by_inst(ld_inst, self.ap)  # get actual LD object
                lln0 = ld_obj.get_LN0()  # now get LLN0
                if hasattr(lln0, "DataSet"):
                    for ds in lln0.DataSet:
                        dataset_info.append({
                            "LD": ld_inst,
                            "dataset_name": ds.name,
                            "dataset": ds
                        })
            except Exception as e:
                print(f"Error accessing datasets from LD {ld}: {e}")
        return dataset_info




    def getAllDomainID(self):
        all_domain = []
        idx = 0
        for val in self.LD_name:
            for k, fc in self.DAobj.items():
                if val in k:
                    obj = k.split(".")
                    fcs = fc.get_associated_fc()

                    # print(len(obj), end='-')
                    # print(obj)
                    buffDict = {}
                    buffDict['LD'] = obj[0]
                    buffDict['LN'] = obj[1]
                    buffDict['DO'] = obj[2]

                    buffDict['DA'] = obj[3]

                    # if len(obj) == 5:
                    #     buffDict['BDA'] = obj[4]
                    # else:a
                    #     buffDict['BDA'] = ''
                    # print(buffDict)

                    # if fcs == None:
                    #     fcs = 'None'
                    # else:
                    obj[1] += '$' + fcs
                    all_domain.append(
                        self.iedName + val+"-"+"$".join(obj[1:]))

                    buffDict['id'] = str(idx)
                    buffDict['domain_id'] = self.iedName + val
                    buffDict['item_id'] = "$".join(obj[1:])
                    buffDict['all'] = buffDict['domain_id'] + \
                        '$'+buffDict['item_id']
                    self.all_domain_dict.append(buffDict)
                    idx += 1
        return all_domain

    def filterMeasurement(self, data, filter: str):
        return [x for x in data if filter in x]

    def saveToFile(self, filePath):
        f = open(filePath, "w")
        for item in self.all_domain:
            f.write(item+"\n")
        f.close()


# def makeItemID(DA, FC):
#     obj = DA.split(".")
#     obj[1] += '$' + FC
#     return "$".join(obj[1:])


#ied1 = IED_PARSING(scl_path)
#all_domain = ied1.getAllDomainID()  # output list string TEMPLATEMET-METMMXU1$MX$Hz$q
                                    # domainId: TEMPLATEMET
                                    # separator : -
                                    # itemId: METMMXU1$MX$Hz$q

#scl_path = "/home/pi/dms/DMSv1.2/IEC61850/COCACOLA_P142.icd"
#ied1 = IED_PARSING(scl_path)
#ied1.saveToFile(scl_path+".txt")
#print(ied1.all_domain_dict)