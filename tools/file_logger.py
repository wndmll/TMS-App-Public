import os
import argparse
import json

def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)
        # Convert paths with single backslashes to use double backslashes
        if 'exclusions' in config:
            config['exclusions'] = [path.replace('\\', '\\\\') for path in config['exclusions']]
        if 'specific_files' in config:
            config['specific_files'] = [path.replace('\\', '\\\\') for path in config['specific_files']]
        if 'specific_folders' in config:
            config['specific_folders'] = [path.replace('\\', '\\\\') for path in config['specific_folders']]
        return config

def read_file_content(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        try:
            with open(filepath, 'r', encoding='utf-16-le') as file:
                return file.read()
        except Exception as e:
            return f"Error reading file with different encoding: {e}"

def create_log_file(log_path, root_dir, exclusions, excluded_extensions, specific_files=None, specific_folders=None, only_scss=False):
    with open(log_path, 'w', encoding='utf-8') as log_file:
        if specific_files:
            # Process specific files in the given order
            for filepath in specific_files:
                if only_scss and not filepath.endswith('.scss'):
                    continue
                if any(filepath.endswith(ext) for ext in excluded_extensions):
                    continue
                if any(os.path.abspath(filepath).startswith(e) for e in exclusions):
                    continue
                content = read_file_content(filepath)
                if 'Error reading file' in content:
                    log_file.write(f"{content}\n")
                elif content:
                    log_file.write(f"Below you will find the content of: [{filepath}]\n")
                    log_file.write(content + '\n')
                else:
                    log_file.write(f"The following file has been created but has no content: [{filepath}]\n")
                log_file.write("\n")
        elif specific_folders:
            for folder in specific_folders:
                for dirpath, dirnames, filenames in os.walk(folder):
                    # Convert exclusions to absolute paths
                    abs_exclusions = [os.path.abspath(e) for e in exclusions]
                    # Remove excluded directories and their subdirectories
                    dirnames[:] = [d for d in dirnames if not any(os.path.abspath(os.path.join(dirpath, d)).startswith(e) for e in abs_exclusions)]
                    for filename in filenames:
                        filepath = os.path.join(dirpath, filename)
                        if only_scss and not filepath.endswith('.scss'):
                            continue
                        if any(filepath.endswith(ext) for ext in excluded_extensions):
                            continue
                        if any(os.path.abspath(filepath).startswith(e) for e in abs_exclusions):
                            continue
                        content = read_file_content(filepath)
                        if 'Error reading file' in content:
                            log_file.write(f"{content}\n")
                        elif content:
                            log_file.write(f"Below you will find the content of: [{filepath}]\n")
                            log_file.write(content + '\n')
                        else:
                            log_file.write(f"The following file has been created but has no content: [{filepath}]\n")
                        log_file.write("\n")
        else:
            for dirpath, dirnames, filenames in os.walk(root_dir):
                # Convert exclusions to absolute paths
                abs_exclusions = [os.path.abspath(e) for e in exclusions]
                # Remove excluded directories and their subdirectories
                dirnames[:] = [d for d in dirnames if not any(os.path.abspath(os.path.join(dirpath, d)).startswith(e) for e in abs_exclusions)]
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    if only_scss and not filepath.endswith('.scss'):
                        continue
                    if any(filepath.endswith(ext) for ext in excluded_extensions):
                        continue
                    if any(os.path.abspath(filepath).startswith(e) for e in abs_exclusions):
                        continue
                    content = read_file_content(filepath)
                    if 'Error reading file' in content:
                        log_file.write(f"{content}\n")
                    elif content:
                        log_file.write(f"Below you will find the content of: [{filepath}]\n")
                        log_file.write(content + '\n')
                    else:
                        log_file.write(f"The following file has been created but has no content: [{filepath}]\n")
                    log_file.write("\n")

def main():
    parser = argparse.ArgumentParser(description="Log content of all files in the project, excluding specific files and folders.")
    parser.add_argument('--mode', type=str, choices=['complete', 'filtered files', 'filtered folders'], default='complete', 
                        help="Logging mode: 'complete' to log all files except exclusions, 'filtered files' to log only specific files, 'filtered folders' to log only specific folders and their contents.")
    parser.add_argument('--scss-only', action='store_true', help="Only export files with .scss extension")
    args = parser.parse_args()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Determine config file based on mode
    config_filename = 'file_logger_config_filtered.json' if 'filtered' in args.mode else 'file_logger_config_complete.json'
    config_path = os.path.join(script_dir, config_filename)
    
    config = load_config(config_path)
    
    root_dir = os.path.abspath(os.path.join(script_dir, '..'))  # Parent directory of the script
    log_path = os.path.join(root_dir, config['log_file'])

    # Define folders and files to exclude
    exclusions = [os.path.abspath(os.path.join(root_dir, path)) for path in config['exclusions']]

    # Define file extensions to exclude
    excluded_extensions = config['excluded_extensions']

    # Get specific files or folders based on mode
    specific_files = None
    specific_folders = None
    if args.mode == 'filtered files':
        specific_files = [os.path.abspath(os.path.join(root_dir, path)) for path in config['specific_files']]
    elif args.mode == 'filtered folders':
        specific_folders = [os.path.abspath(os.path.join(root_dir, path)) for path in config['specific_folders']]

    create_log_file(log_path, root_dir, exclusions, excluded_extensions, specific_files, specific_folders, args.scss_only)

if __name__ == "__main__":
    main()