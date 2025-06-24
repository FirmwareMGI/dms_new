import os
import subprocess
import time
import db
from subprocess import Popen, PIPE, STDOUT



Qport_id = db.readDb.m_port_grup(1, "IEC61850")
port_id = Qport_id[0]["id"]

# Configuration
base_service_name = "report-client"
binary_path = "/home/mgi/dms/c_dms/lib/libiec61850/examples/iec61850_client_example_reporting/client_example_reporting"
config_dir = "/home/mgi/gipat-config/public/assets/TYPE/{port_id}/".format(port_id=port_id)
systemd_dir = "/etc/systemd/system"
user = "mgi"

temp_path = "/home/mgi/dms/dms_new/IEC61850/output/iec61850_client_example_reporting.service"

password_sudo = "mgi@2025"



# Instances to create and monitor
# device_list=db.readDb.device_list(1)
# print(device_list)
# Template for systemd unit
unit_template = """[Unit]
Description=Report Client Instance {instance}
After=network.target
StartLimitBurst=5
StartLimitIntervalSec=20


[Service]
Type=simple
ExecStart={binary} {config_dir}/{config_file}
WorkingDirectory=/home/mgi/dms/
Restart=always
RestartSec=3
User={user}
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
"""

def write_unit_file(instance, config_file):
    unit_name = f"{base_service_name}@{instance}.service"
    unit_path = os.path.join(systemd_dir, unit_name)
    content = unit_template.format(
        instance=instance,
        binary=binary_path,
        config_dir=config_dir,
        config_file=config_file,
        user=user
    )
    with open(temp_path, "w") as f:
        f.write(content)
        print(f"📝 Written temporary file: {temp_path}")
    
    # subprocess.run(['sudo', 'mv', temp_path, os.path.join(systemd_dir, unit_name)], check=True)
    run_command_with_sudo(f"echo {password_sudo} | sudo -S mv {temp_path} {unit_path}".format(
        password_sudo=password_sudo,
        temp_path=temp_path,
        unit_path=unit_path
    ))
    print(f"✅ Moved to {systemd_dir}")
    
def run_command_with_sudo(command):
    with Popen(
        command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True
    ) as process:
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            print("Command succeeded:")
            print(stdout)
        else:
            print("Command failed:")
            print(stderr)


def reload_and_enable_start(instance):
    service = f"{base_service_name}@{instance}"
    
    daemon_reload_command = f"echo {password_sudo} | sudo -S systemctl daemon-reload"
    enable_service_command = f"echo {password_sudo} | sudo -S systemctl enable {service}"
    start_service_command = f"echo {password_sudo} | sudo -S systemctl start {service}"
    
    run_command_with_sudo(daemon_reload_command)
    run_command_with_sudo(enable_service_command)
    
    result = subprocess.run(
        start_service_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    
    if result.returncode == 0:
        print(f"? Service {service} started successfully.")
        return True
    else:
        print(f"? Failed to start service {service}:\n{result.stderr}")
        return False


def check_service_status(instance):
    service = f"{base_service_name}@{instance}"
    result = subprocess.run(
        ["systemctl", "is-active", service],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.stdout.strip()


def stop_and_disable_service(instance):
    service = f"{base_service_name}@{instance}"
    print(f"?? Stopping and disabling missing service {service}...")

    stop_cmd = f"echo {password_sudo} | sudo -S systemctl stop {service}"
    disable_cmd = f"echo {password_sudo} | sudo -S systemctl disable {service}"

    run_command_with_sudo(stop_cmd)
    run_command_with_sudo(disable_cmd)


def restart_service(instance):
    service = f"{base_service_name}@{instance}"
    restart_cmd = f"echo {password_sudo} | sudo -S systemctl restart {service}"
    print(f"?? Restarting {service}")
    run_command_with_sudo(restart_cmd)



# Build clients dynamically from device_list
clients = {}
device_list=db.readDb.device_list(1)
print("device_list", device_list)
for device in device_list:
    if (str(device.get("port_type")) == "6" and
        int(device.get("scl_flag", 0)) == 2 and
        int(device.get("process_flag", 0)) == 0):
        instance_id = str(device["id_device"])
        # config_dir = os.path.join(config_dir, instance_id)

        config_file = f"scl_{instance_id}"
        clients[instance_id] = config_file

def main():
    clients = {}
    print("?? Scanning and managing IEC61850 clients...")

    while True:
        device_list = db.readDb.device_list(1)
        current_ids = set()
        print("masok sini")

        for device in device_list:
            if str(device.get("port_group_id")) != "16":
                continue

            instance_id = str(device["id_device"])
            process_flag = int(device.get("process_flag", 0))
            config_file = f"scl_{instance_id}"
            current_ids.add(instance_id)

            if process_flag == 0:
                if instance_id in clients:
                    continue  # Already started
                print(f"?? Starting new service for device {instance_id}")
                clients[instance_id] = config_file
                write_unit_file(instance_id, config_file)
                success = reload_and_enable_start(instance_id)
                db.insertDb.update_process_flag(1, instance_id, 1 if success else 2)
            
            
            elif process_flag == 1:
                if instance_id not in clients:
                    print(f"??? Registering running device {instance_id} for monitoring")
                    clients[instance_id] = config_file

            elif process_flag == 2:
              if instance_id not in clients:
                  print(f"?? Retrying failed start for device {instance_id}")
                  clients[instance_id] = config_file
                  write_unit_file(instance_id, config_file)
                  success = reload_and_enable_start(instance_id)
                  db.insertDb.update_process_flag(1, instance_id, 1 if success else 2)
              else:
                  print(f"?? [Flag 2] {base_service_name}@{instance_id} is already running, monitoring only")
                  db.insertDb.update_process_flag(1, instance_id,1)
            
            elif process_flag == 3:
                print(f"?? Restart requested for {instance_id}")
                if instance_id not in clients:
                    clients[instance_id] = config_file
                    write_unit_file(instance_id, config_file)
                restart_service(instance_id)
                db.insertDb.update_process_flag(1, instance_id, 1)
        
        # Detect removed clients
        removed_clients = [cid for cid in clients if cid not in current_ids]
        #print(f"removed clients {removed_clients}")
        for removed in removed_clients:
            stop_and_disable_service(removed)
            del clients[removed]
        
        
        # Periodic status check
        for instance in clients:
            status = check_service_status(instance)
            print(f"?? {base_service_name}@{instance} is {status}")

        time.sleep(5)




if __name__ == "__main__":
    main()
