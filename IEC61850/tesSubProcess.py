import os
import subprocess
import time
import db

# Configuration
base_service_name = "report-client"
binary_path = "/home/pi/c_dms/lib/libiec61850/examples/iec61850_client_example_reporting/client_example_reporting"
config_dir = "/var/www/html/dms_setting/assets/scl/"
systemd_dir = "/etc/systemd/system"
user = "pi"

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
ExecStart={binary} {config_dir}/{config_file} {instance}
WorkingDirectory={config_dir}
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
    with open(unit_path, "w") as f:
        f.write(content)
    print(f"✅ Created {unit_path}")

def reload_and_enable_start(instance):
    service = f"{base_service_name}@{instance}"
    subprocess.run(["sudo","systemctl", "daemon-reload"], check=True)
    subprocess.run(["sudo","systemctl", "enable", service], check=True)
    subprocess.run(["sudo","systemctl", "start", service], check=True)
    print(f"🚀 Enabled and started {service}")

def check_service_status(instance):
    service = f"{base_service_name}@{instance}"
    result = subprocess.run(
        ["sudo","systemctl", "is-active", service],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.stdout.strip()

device_list=db.readDb.device_list(1)

# Build clients dynamically from device_list
clients = {}
for device in device_list:
    if (str(device.get("port_type")) == "2" and
        int(device.get("scl_flag", 0)) == 2 and
        int(device.get("process_flag", 0)) == 0):
        instance_id = str(device["id_device"])
        config_file = f"scl_{instance_id}"
        clients[instance_id] = config_file

def main():
    # Must be root
    # if os.geteuid() != 0:
    #     print("⚠️ This script must be run as root.")
    #     exit(1)

    # Filter devices
    valid_instances = []
    for device in device_list:
        if (str(device.get("port_type")) == "2" and
            int(device.get("scl_flag", 0)) == 2 and
            int(device.get("process_flag", 0)) == 0):
            instance_id = str(device["id_device"])
            print(f"🔍 Found valid device: {device['type']} (ID: {instance_id})")
            if instance_id in clients:
                valid_instances.append(instance_id)

    if not valid_instances:
        print("⚠️ No valid instances found based on device filtering.")
        return

    # Create and start services
    for instance in valid_instances:
        config_file = clients[instance]
        print(f"🔧 Configuring service for instance {instance} with config {config_file}")
        write_unit_file(instance, config_file)
        reload_and_enable_start(instance)

    # Monitoring loop
    print("🔁 Monitoring service statuses. Press Ctrl+C to stop.")
    try:
        while True:
            for instance in valid_instances:
                status = check_service_status(instance)
                print(f"🔎 {base_service_name}@{instance} → {status}")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user.")


if __name__ == "__main__":
    main()
