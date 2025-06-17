import json
import copy
import os

# Load base JSON from file (optional: you can paste it inline too)
with open('scl_12_parsed.json', 'r') as f:
    base_config = json.load(f)

# Create output directory
output_dir = 'generated_configs'
os.makedirs(output_dir, exist_ok=True)

# Generate 30 files with one different report enabled each time

for i in range(1,4):
    
    config_copy = copy.deepcopy(base_config)
    if i == 1:
        config_copy["port"] = "102"
    elif i == 2:
        config_copy["port"] = "9102"
    elif i == 3:
        config_copy["port"] = "9103"
    
    for j in range(20, 50):  # From 20 to 50 inclusive
        report_index = j - 20
        config_copy["idDevice"] = str(i) + str(j)
        
        # Enable only the selected report
        for report in config_copy['reports']:
            report['isEnable'] = (report['id'] == report_index)

        # Save to file
        output_file = os.path.join(output_dir, f'scl_{i}{j}_parsed.json')
        with open(output_file, 'w') as out_f:
            json.dump(config_copy, out_f, indent=2)

print("✅ All files generated in 'generated_configs/' folder.")
