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

    def getAllDomainID(self):
        all_domain = []
        for val in self.LD_name:
            # print(self.iedName+val)
            for k, fc in self.DAobj.items():
                if val in k:
                    obj = k.split(".")
                    obj[1] += '$' + fc.get_associated_fc()
                    all_domain.append(self.iedName + val+"-"+"$".join(obj[1:]))
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
#ied1.saveToFile(scl_path+".txt")
