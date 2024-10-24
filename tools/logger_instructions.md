# File Logger Usage Instructions

This file logger is a Python script that logs the content of files in a project, with options to exclude specific files/folders and filter by file type. Here's how to use it:

## Setup

1. Ensure you have Python installed on your system.
2. Place the script in your project directory.
3. Create configuration files:
   - `file_logger_config_complete.json` for complete logging
   - `file_logger_config_filtered.json` for filtered logging

## Configuration Files

Both JSON files should contain:

- `log_file`: Name of the output log file
- `exclusions`: List of folders/files to exclude
- `excluded_extensions`: List of file extensions to exclude

For filtered logging, also include:
- `specific_files`: List of specific files to log
- `specific_folders`: List of specific folders to log

## Running the Logger

Use the following command structure:

```
python file_logger.py [--mode MODE] [--scss-only]
```

### Arguments

- `--mode`: Choose between 'complete', 'filtered files', or 'filtered folders'
  - 'complete': Logs all files except exclusions
  - 'filtered files': Logs only specific files
  - 'filtered folders': Logs only specific folders and their contents
- `--scss-only`: Optional flag to log only .scss files

### Examples

1. Complete logging:
   ```
   python file_logger.py --mode complete
   ```

2. Log only specific files:
   ```
   python file_logger.py --mode "filtered files"
   ```

3. Log only specific folders:
   ```
   python file_logger.py --mode "filtered folders"
   ```

4. Log only .scss files in complete mode:
   ```
   python file_logger.py --mode complete --scss-only
   ```

## Output

The script will generate a log file in the parent directory of the script, containing the content of the logged files according to the specified mode and options.