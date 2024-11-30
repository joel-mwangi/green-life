import json

# Load the JSON file
with open(".vscode/PythonImportHelper-v2-Completion.json", "r") as file:
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
with open(".vscode/PythonImportHelper-v2-Completion.json", "w") as file:
    json.dump(unique_data, file, indent=4)

print("Duplicates removed!")
