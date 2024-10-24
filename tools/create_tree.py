import os
import json

# Define the base path and configuration file path
base_path = r'D:\www\TMS-App'
config_path = r'D:\www\TMS-App\tools\file_logger_config_complete.json'

# Load configuration file
with open(config_path, 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

# Extract exclusions, excluded extensions, and log file location
exclusions = config.get('exclusions', [])
excluded_extensions = config.get('excluded_extensions', [])
log_tree = config.get('log_tree', 'D:/www/TMS-App/data/log/project.log')

def is_excluded(path):
    for exclusion in exclusions:
        if exclusion in path:
            return True
    for ext in excluded_extensions:
        if path.endswith(ext):
            return True
    return False

def create_tree(base_path, prefix=""):
    items = sorted(os.listdir(base_path))
    lines = []
    for i, item in enumerate(items):
        path = os.path.join(base_path, item)
        if is_excluded(path):
            continue
        connector = "├── " if i < len(items) - 1 else "└── "
        lines.append(prefix + connector + item)
        if os.path.isdir(path):
            extension = "│   " if i < len(items) - 1 else "    "
            lines.extend(create_tree(path, prefix + extension))
    return lines

def main():
    tree = create_tree(base_path)
    tree_str = "\n".join(tree)
    
    # Print the tree to console
    print(tree_str)
    
    # Write the tree to the log file
    log_tree_path = log_tree.replace('/', os.sep)  # Ensure compatibility with OS path separator
    os.makedirs(os.path.dirname(log_tree_path), exist_ok=True)
    with open(log_tree_path, 'w', encoding='utf-8') as log_file:
        log_file.write(tree_str)

if __name__ == "__main__":
    main()
