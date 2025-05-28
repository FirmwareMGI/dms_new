# import json
# import os
# from pathlib import Path
# from scl_loader import SCD_handler
# # from collection import defaultdict

# class IED_Parser:
#     def __init__(self, scl_path, ip=None, port=None):
#         self.scl_path = scl_path
#         self.ied_name = None
#         self.ip = ip          # <-- set via constructor
#         self.port = port      # <-- set via constructor
#         self.ied = None
#         self.lds = []
#         self.ap = None
#         self.control_list = []
#         self.report_list = []
#         self.report_id_counter = 0
#         self.control_id_counter = 0
#         self.temp_dict = {}
#         self.datasets_info_grouped = []

#     def load(self):
#         try:
#             scd = SCD_handler(self.scl_path, False)
#             self.ied_name = scd.get_IED_names_list()[0]
#             self.ied = scd.get_IED_by_name(self.ied_name)
#             ip_info = scd.get_IP_Adr(self.ied_name)
#             self.ap = ip_info[1]
#             if not self.ip or not self.port:
#                 self.ip = self.ip or ip_info[0]
#             self.lds = self.ied.get_children_LDs(self.ap)
#             return True
#         except Exception as e:
#             print(f"❌ Failed to load SCL '{self.scl_path}': {e}")
#             return False

#     def extract_ctl_models(self):
#         try:
#             da_list = self.ied.get_DA_leaf_nodes()
#             for da in da_list.values():
#                 if da.name == 'ctlModel' and hasattr(da, 'Val'):
#                     obj_path = str(da.get_path_from_ld()).replace(".ctlModel", "")
#                     ctl_path = f"{self.ied_name}{obj_path}"
#                     self.control_list.append({
#                         "id": self.control_id_counter,
#                         "object": ctl_path,
#                         "ctlModel": da.Val,
#                     })
#                     self.control_id_counter += 1
#         except Exception as e:
#             print(f"❌ Error extracting ctlModel: {e}")

#     def extract_report_controls(self):
#         try:
#             for ld in self.lds:
#                 ld_name = ld.name
#                 report_controls = ld.get_reportcontrols()
#                 data_set = ld.get_datasets()
                
#                 # for data in data_set:
#                 #     print(f"Processing dataset: {data.name}")
#                 #     lnclass = getattr(data.parent(), "lnClass", "")
#                 #     for fcda in data.FCDA:
#                 #         lnInst = getattr(fcda, 'lnInst', '')
#                 #         print(f"Processing FCDA: {fcda.name} in LN: {lnclass} with lnInst: {lnInst}")
#                 #         base = f"{self.ied_name[0]}{ld.name}/{fcda.lnClass}"
#                 #         if lnInst:
#                 #             base += f"{lnInst}"

#                 #         full_path = f"{base}.{fcda.doName}[{fcda.fc}]"
#                 #         dataset_key = f"{self.ied_name[0] + ld_name}/{lnclass}${data.name}"
#                 #         print("RAMPUNG")

#                 #         self.temp_dict[dataset_key].append(full_path)

#                 # # Then: Format with reset `id` per key
#                 # self.datasets_info_grouped = [
#                 #     {
#                 #         "dataSetReference": dataset_key,
#                 #         "listData": [
#                 #             {"id": idx, "fcda": fcda}
#                 #             for idx, fcda in enumerate(fcda_list)
#                 #         ]
#                 #     }
#                 #     for dataset_key, fcda_list in self.temp_dict.items()
#                 # ]
                
#                 if not report_controls:
#                     print(f"  LD: {ld_name} → No ReportControls found.")
#                     continue

#                 for rc in report_controls:
#                     lnclass = getattr(rc.parent(), "lnClass", "")
#                     dataset = rc.datSet
#                     dataset_ref = f"{self.ied_name[0]}{ld_name}/{lnclass}${dataset}"
#                     self._process_rc_block(rc, ld_name, dataset_ref)
#         except Exception as e:
#             print(f"❌ Error processing ReportControls in {self.scl_path}: {e}")

#     def _process_rc_block(self, rc, ld_name, dataset_ref):
#         try:
#             if rc.RptEnabled and hasattr(rc.RptEnabled, 'max'):
#                 max_val = int(rc.RptEnabled.max)
#                 prefix = f"{self.ied_name[0]}{ld_name}/LLN0$BR$"
#                 for i in range(1, max_val + 1):
#                     index = f"{i:02}"
#                     cb_ref = f"{prefix}{rc.name}{index}"

#                     self.host_reports.append({
#                         "id": self.report_id_counter,
#                         "dataSetReference": dataset_ref,
#                         "rcb": cb_ref,
#                         "isEnable": False
#                     })
#                     self.report_id_counter += 1
#         except Exception as e:
#             print(f"❌ Error in RC block processing for {rc.name}: {e}")

#     def save_to_json(self, output_path):
#         try:
#             os.makedirs(os.path.dirname(output_path), exist_ok=True)
#             output = {
#                 "iedName": self.ied_name,
#                 "localIP": self.ip,
#                 "port" : self.port,
#                 "control": self.control_list,
#                 "reports": self.report_list
#             }
#             with open(output_path, "w") as f:
#                 json.dump(output, f, indent=2)
#             print(f"✅ Saved to {output_path}")
#         except Exception as e:
#             print(f"❌ Failed to write output file: {e}")
            
#     def export_dataset_info(self, dataset_filename="datasets.json"):
#         try:
#             os.makedirs(os.path.dirname(dataset_filename), exist_ok=True)
#             with open(dataset_filename, "w") as f:
#                 json.dump(self.datasets_info_grouped, f, indent=4)
#             print(f"✅ Exported datasets to '{dataset_filename}'.")
#         except Exception as e:
#             print(f"❌ Failed to export datasets: {e}")


# def process_scl_folder(folder_path, output_dir="output_combined"):
#     supported_exts = ('.icd', '.cid', '.iid')

#     for subdir, _, files in os.walk(folder_path):
#         for file in files:
#             if file.lower().endswith(supported_exts):
#                 scl_path = os.path.join(subdir, file)
#                 print(f"🔍 Processing: {scl_path}")

#                 parser = IED_Parser(scl_path)
#                 if parser.load():
#                     parser.extract_ctl_models()
#                     parser.extract_report_controls()

#                     base_name = os.path.splitext(file)[0]
#                     output_path = os.path.join(output_dir, f"{base_name}_parsed.json")
#                     parser.save_to_json(output_path)
#                 else:
#                     print(f"⚠️ Skipped: {scl_path}")
# def process_single_scl_file(scl_path, ip=None, port=None, output_dir="output_combined"):
#     """
#     Processes a single SCL file (.icd, .cid, .iid), extracts control and report info,
#     and saves it into a combined JSON.

#     Args:
#         scl_path (str): Full path to the SCL file.
#         ip (str): Optional. IP address to be added in the output.
#         port (str/int): Optional. Port number to be added in the output.
#         output_dir (str): Directory where output JSON will be saved.

#     Returns:
#         bool: True if processed successfully, False otherwise.
#     """
#     try:
#         print(f"🔍 Processing single file: {scl_path}")
#         parser = IED_Parser(scl_path, ip=ip, port=port)
        
#         if not parser.load():
#             print(f"⚠️ Failed to load: {scl_path}")
#             return False

#         parser.extract_ctl_models()
#         parser.extract_report_controls()

#         base_name = os.path.splitext(os.path.basename(scl_path))[0]
#         output_path = os.path.join(output_dir, f"{base_name}_parsed.json")
#         parser.save_to_json(output_path)
        
#         dataset_path = os.path.join(output_dir, f"{base_name}_datasets.json")
#         parser.export_dataset_info(dataset_filename=dataset_path)

#         return True
#     except Exception as e:
#         print(f"❌ Error processing {scl_path}: {e}")
#         return False



import json
import os
from scl_loader import SCD_handler
from collections import defaultdict


class IEDPARSER:
    def __init__(self, scl_path, ip=None, port=None):
        self.scl_path = scl_path
        self.ied_name = None
        self.ip = ip
        self.port = port
        self.ied = None
        self.lds = []
        self.host_reports = []
        self.control_list = []
        self.report_id_counter = 0
        self.control_id_counter = 0
        self.temp_dict = defaultdict(list)
        self.datasets_info_grouped = []

    def load_scl(self):
        try:
            handler = SCD_handler(self.scl_path)
            self.ied_name = handler.get_IED_names_list()
            ip_info = handler.get_IP_Adr(self.ied_name[0])
            self.ied = handler.get_IED_by_name(self.ied_name[0])
            self.lds = self.ied.get_children_LDs(ip_info[1])

            # Default to IP from SCL unless overridden
            if not self.ip:
                self.ip = ip_info[0]
            if not self.port:
                self.port = "102"  # default port

            print(f"✅ IED Loaded: {self.ied_name[0]}")
            return True
        except Exception as e:
            print(f"❌ Failed to load SCL '{self.scl_path}': {e}")
            return False

    def extract_ctl_models(self):
        try:
            da_list = self.ied.get_DA_leaf_nodes()
            for da in da_list.values():
                if da.name == 'ctlModel' and hasattr(da, 'Val'):
                    obj_path = str(da.get_path_from_ld()).replace(".ctlModel", "")
                    ctl_path = f"{self.ied_name[0]}{obj_path}"
                    self.control_list.append({
                        "id": self.control_id_counter,
                        "object": ctl_path,
                        "ctlModel": da.Val,
                    })
                    self.control_id_counter += 1
        except Exception as e:
            print(f"❌ Error extracting ctlModel: {e}")


    def process_report_controls(self):
        try:
            for ld in self.lds:
                ld_name = ld.name
                report_controls = ld.get_reportcontrols()
                data_set = ld.get_datasets()
                # print(f"Data Set: {data_set}")

                for data in data_set:
                    lnclass = getattr(data.parent(), "lnClass", "")
                    for fcda in data.FCDA:
                        lnInst = getattr(fcda, 'lnInst', '')
                        base = f"{self.ied_name[0]}{ld.name}/{fcda.lnClass}"
                        if lnInst:
                            base += f"{lnInst}"

                        full_path = f"{base}.{fcda.doName}[{fcda.fc}]"
                        dataset_key = f"{self.ied_name[0] + ld_name}/{lnclass}${data.name}"

                        self.temp_dict[dataset_key].append(full_path)

                # Then: Format with reset `id` per key
                self.datasets_info_grouped = [
                    {
                        "dataSetReference": dataset_key,
                        "listData": [
                            {"id": idx, "fcda": fcda}
                            for idx, fcda in enumerate(fcda_list)
                        ]
                    }
                    for dataset_key, fcda_list in self.temp_dict.items()
                ]


                        

                if not report_controls:
                    print(f"  LD: {ld_name} → No ReportControls found.")
                    continue

                for rc in report_controls:
                    lnclass = getattr(rc.parent(), "lnClass", "")
                    dataset = rc.datSet
                    dataset_ref = f"{self.ied_name[0]}{ld_name}/{lnclass}${dataset}"
                    self._process_rc_block(rc, ld_name, dataset_ref)
        except Exception as e:
            print(f"❌ Error processing ReportControls in {self.scl_path}: {e}")

    def _process_rc_block(self, rc, ld_name, dataset_ref):
        try:
            if rc.RptEnabled and hasattr(rc.RptEnabled, 'max'):
                max_val = int(rc.RptEnabled.max)
                prefix = f"{self.ied_name[0]}{ld_name}/LLN0$BR$"
                for i in range(1, max_val + 1):
                    index = f"{i:02}"
                    cb_ref = f"{prefix}{rc.name}{index}"

                    self.host_reports.append({
                        "id": self.report_id_counter,
                        "dataSetReference": dataset_ref,
                        "rcb": cb_ref,
                        "isEnable": False
                    })
                    self.report_id_counter += 1
        except Exception as e:
            print(f"❌ Error in RC block processing for {rc.name}: {e}")

    def export_to_files(self, host_filename="host_reports.json"):
        try:
            hosts_json = {
                "hostname": self.ip[0],
                "reports": self.host_reports
            }

            os.makedirs(os.path.dirname(host_filename), exist_ok=True)
            with open(host_filename, "w") as f:
                json.dump(hosts_json, f, indent=4)

            print(f"✅ Exported to '{host_filename}'.")
        except Exception as e:
            print(f"❌ Failed to export files: {e}")
            
    def export_dataset_info(self, dataset_filename="datasets.json"):
        try:
            os.makedirs(os.path.dirname(dataset_filename), exist_ok=True)
            with open(dataset_filename, "w") as f:
                json.dump(self.datasets_info_grouped, f, indent=4)
            print(f"✅ Exported datasets to '{dataset_filename}'.")
        except Exception as e:
            print(f"❌ Failed to export datasets: {e}")


def process_all_scl_files_in_folder(folder_path):
    supported_extensions = {'.cid', '.icd', '.iid'}

    for root, _, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in supported_extensions):
                scl_path = os.path.join(root, file)
                print(f"🔍 Processing: {scl_path}")

                builder = IEDPARSER(scl_path)
                if builder.load_scl():
                    builder.process_report_controls()

                    base_name = os.path.splitext(file)[0]
                    builder.export_to_files(
                        host_filename=f"output/{base_name}_host_reports.json"
                    )
                else:
                    print(f"⚠️ Failed to load {scl_path}")


def process_single_scl_file(scl_path, ip=None, port=None, output_dir="output"):
    try:
        print(f"🔍 Processing: {scl_path}")
        builder = IEDPARSER(scl_path, ip=ip, port=port)

        if builder.load_scl():
            builder.extract_ctl_models()
            builder.process_report_controls()

            base_name = os.path.splitext(os.path.basename(scl_path))[0]

            # Combine all info into one file
            combined_output = {
                "iedName": builder.ied_name[0],
                "localIP": builder.ip,
                "port": builder.port,
                "control": builder.control_list,
                "reports": builder.host_reports
            }

            os.makedirs(output_dir, exist_ok=True)
            combined_path = os.path.join(output_dir, f"{base_name}_parsed.json")
            with open(combined_path, "w") as f:
                json.dump(combined_output, f, indent=2)

            print(f"✅ Exported to '{combined_path}'.")

            # Optional: separate dataset file
            dataset_path = os.path.join(output_dir, f"{base_name}_datasets.json")
            builder.export_dataset_info(dataset_filename=dataset_path)
            return True
        else:
            print(f"⚠️ Failed to load {scl_path}")
            return False
    except Exception as e:
        print(f"❌ Unexpected error processing {scl_path}: {e}")
        return False



# # 🔧 Example usage
# if __name__ == "__main__":
#     # folder_path = "scl_files"
#     # process_all_scl_files_in_folder(folder_path)

#     # Or test single file
#     process_single_scl_file("/var/www/html/dms_setting/upload/scl_1.icd")
