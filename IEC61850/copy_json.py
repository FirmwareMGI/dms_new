import json
import os

# Load the base datasets file
with open('scl_12_datasets.json', 'r') as f:
    base_datasets = json.load(f)

# Output directory
output_dir = 'generated_configs'
os.makedirs(output_dir, exist_ok=True)

# Generate scl_20_datasets.json to scl_50_datasets.json
for i in range(1, 4):
    for x in range(20, 50):
        filename = os.path.join(output_dir, f'scl_{i}{x}_datasets.json')
        with open(filename, 'w') as out_f:
            json.dump(base_datasets, out_f, indent=2)

print("✅ Datasets files scl_20_datasets.json to scl_50_datasets.json created.")
