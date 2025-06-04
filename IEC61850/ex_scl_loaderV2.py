import json
import os
from scl_loader import SCD_handler
from scl_loader import LN
from collections import defaultdict

BR_list = ["brcb", "brep", "bcrb", "bcrep"]


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
                # ld_childern = ld.get_children_LDs(self.ied.ap)  # Ensure LD is fully loaded
                # ld_ln = ld.get_children()
                # print("ld Name:", ld_ln[0].get_children()[0].name)
                # break
                report_controls = ld.get_reportcontrols()
                # print(f"Processing LD: {ld_name} with {len(report_controls)} ReportControls")
                # break
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
                    print(f"Processing ReportControl: {rc.name}")
                    lnclass = getattr(rc.parent(), "lnClass", "")
                    dataset = rc.datSet
                    dataset_ref = f"{self.ied_name[0]}{ld_name}/{lnclass}${dataset}"
                    self._process_rc_block(rc, ld_name, dataset_ref, lnclass)
        except Exception as e:
            print(f"❌ Error processing ReportControls in {self.scl_path}: {e}")

    def _process_rc_block(self, rc, ld_name, dataset_ref, ln_class):
        try:
            if rc.RptEnabled and hasattr(rc.RptEnabled, 'max'):
                max_val = int(rc.RptEnabled.max)
                if any(x in rc.name.lower() for x in BR_list):
                    prefix = f"{self.ied_name[0]}{ld_name}/{ln_class}$BR$"
                else:
                    prefix = f"{self.ied_name[0]}{ld_name}/{ln_class}$RP$"
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
            else:
                if any(x in rc.name.lower() for x in BR_list):
                    prefix = f"{self.ied_name[0]}{ld_name}/{ln_class}$BR$"
                else:
                    prefix = f"{self.ied_name[0]}{ld_name}/{ln_class}$RP$"
                cb_ref = f"{prefix}{rc.name}"
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


def process_single_scl_file(scl_path, ip=None, port=None, output_dir="output", machine_code=None, id_device=None):
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
                "machineCode": machine_code,
                "idDevice": id_device,
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



# 🔧 Example usage
if __name__ == "__main__":
    folder_path = "scl_files"
    process_all_scl_files_in_folder(folder_path)
    upload_dir = "/var/www/html/dms_setting/upload"

    # Or test single file
    process_single_scl_file("/var/www/html/dms_setting/upload/D101_2.icd")
    # for filename in os.listdir(upload_dir):
    #     file_path = os.path.join(upload_dir, filename)

    #     # Make sure it's a file (not a subdirectory)
    #     if os.path.isfile(file_path):
    #         process_single_scl_file(file_path)
    # process_all_scl_files_in_folder("/var/www/html/dms_setting/upload")

