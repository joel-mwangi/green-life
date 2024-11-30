import json
import os

# Define file paths
json_file = ".vscode/PythonImportHelper-v2-Completion.json"
txt_file = "requirements.txt"

# Function to deduplicate JSON file
def deduplicate_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

    # Deduplicate based on 'label' and 'importPath'
    seen = set()
    unique_data = []
    for item in data:
        key = (item["label"], item["importPath"])
        if key not in seen:
            seen.add(key)
            unique_data.append(item)

    # Save the cleaned JSON back to the file
    with open(file_path, "w") as file:
        json.dump(unique_data, file, indent=4)

    print(f"Duplicates removed from JSON file: {file_path}")

# Function to deduplicate text file
def deduplicate_txt(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found!")
        return

    with open(file_path, "r") as file:
        lines = file.readlines()

    # Deduplicate lines
    unique_lines = sorted(set(line.strip() for line in lines if line.strip()))

    # Save the cleaned text back to the file
    with open(file_path, "w") as file:
        file.write("\n".join(unique_lines) + "\n")

    print(f"Duplicates removed from text file: {file_path}")

# Run deduplication for both files
if os.path.exists(json_file):
    deduplicate_json(json_file)

if os.path.exists(txt_file):
    deduplicate_txt(txt_file)
