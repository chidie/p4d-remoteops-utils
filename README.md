# To run codebase:
- Create a virtual environment using ```python -m venv venv```
- Install libraries within the requirements.txt file using ```pip install -r requirements.txt```

>NOTE: Key libraries like Paramiko is for SFTP communication and pythonnet is for loading .DLL file.

## Task 1: 
- Check whether 'path' points to an existing regular folder on the remote host.
- Symbolic links, shortcuts, files or non-existent paths return False
>Note: A Windows junction pointing to an existing folder is treated as a folder

## Task 2: 
- Create the folder at 'folder_path' and any missing parent folders on the remote host.
  * If 'folder_path' already exists and is a folder, nothing happens.
  * If it exists and is NOT a folder, an exception is raised.
>NOTE: The 'create_folder_path_recursively' method does not delete, modify, or overwrite existing filesystem instances.