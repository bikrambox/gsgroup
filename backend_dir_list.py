import os

# Function to normalize the path to what's expected for the current operating system
def normalize_path(path):
    return os.path.normpath(path.replace('\\', '/'))

def is_binary_file(file_path):
    """Check if a file is binary."""
    with open(file_path, 'rb') as file:
        chunk = file.read(1024)
        if b'\0' in chunk:
            return True
    return False

def list_files_and_folders(start_path, ignore_folders=None, ignore_files=None):
    if ignore_folders is None:
        ignore_folders = []
    if ignore_files is None:
        ignore_files = []

    start_path = normalize_path(start_path)
    
    for root, dirs, files in os.walk(start_path):
        # Calculate the relative path of the current root directory
        relative_root = normalize_path(os.path.relpath(root, start_path))

        # Remove ignored folders from the dirs list to skip them and their subfolders
        dirs[:] = [d for d in dirs if not any(
            normalize_path(os.path.relpath(os.path.join(root, d), start_path)).startswith(ignore_folder)
            for ignore_folder in ignore_folders
        )]

        for f in files:
            # Calculate the full relative path of the file
            file_path = os.path.join(root, f)
            relative_path = normalize_path(os.path.relpath(file_path, start_path))

            # Check if the file's relative path matches any ignored file path
            if not any(relative_path == ignore_file for ignore_file in ignore_files):
                if not is_binary_file(file_path):
                    print(f"FileName: {relative_path}")
                    print()  # Add line after file name
                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            print(file.read())
                        print()  # Add line after file data
                        print()  # Add line after error message
                    except Exception as e:
                        print(f"Error reading file {relative_path}: {str(e)}")
                        print()  # Add line after the error message

def read_ignore_file(file_path):
    ignore_folders = []
    ignore_files = []
    current_section = None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
            elif line:
                if current_section == 'folders_and_subfolders':
                    ignore_folders.append(normalize_path(line))
                elif current_section == 'files':
                    ignore_files.append(normalize_path(line))

    return ignore_folders, ignore_files

# Specify the path
start_path = r'C:\Users\Hemanta\Documents\Github\gsgroup'  # Replace with the actual path on Windows
start_path = normalize_path(start_path)

# Read the ignores.txt file
ignore_folders, ignore_files = read_ignore_file('backend_ignores.txt')

# Call the function
list_files_and_folders(start_path, ignore_folders, ignore_files)