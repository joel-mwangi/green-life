import os
import json

# Path to your Django project folder (use raw string for paths on Windows)
project_folder = r'E:\myproject\project_name'

# Function to remove duplicate items from a list of JSON objects (assuming your JSON contains arrays)


def remove_duplicates(data):
    if isinstance(data, list):
        seen = set()
        unique_data = []
        for item in data:
            # Using json.dumps to handle nested dict comparison
            item_str = json.dumps(item, sort_keys=True)
            if item_str not in seen:
                unique_data.append(item)
                seen.add(item_str)
        return unique_data
    elif isinstance(data, dict):
        # For dictionaries, remove duplicate key-value pairs (if needed)
        return {k: v for k, v in data.items()}
    return data

# Function to process all JSON files recursively in a directory


def process_json_files_in_directory(directory):
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.json'):
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        # Load the JSON data
                        data = json.load(f)

                        # Remove duplicates from the data
                        cleaned_data = remove_duplicates(data)

                        # Save the cleaned data back to the same file
                        with open(file_path, 'w', encoding='utf-8') as f:
                            json.dump(cleaned_data, f, indent=4)

                    print(f"Processed {file_path} for redundancy.")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")


# Run the process on the entire project folder
process_json_files_in_directory(project_folder)
