import logging
import typing
import pathlib
import stat
import paramiko

class RemoteHost:
    """ Utilities for interacting with a remote host via SFTP"""

    @classmethod
    def is_path_a_regular_folder(
        cls,
        path: typing.Union[str, pathlib.Path],
        sftp: "paramiko.sftp_client.SFTPClient",
        logger: typing.Union[None, logging.Logger]=None,
        description_str: str=""
    ) -> bool:
        """
        :param path: the 'path' (either as a 'str' or as a 'pathlib.Path') for which it is to be checked whether it points to an EXISTING FOLDER.
        :param sftp: the SFTP client providing the connection to the remote host.
        :param logger: a 'logging.Logger' instance - if logging is wished; 'None' otherwise.
        :param description_str: this is a string used as a prefix (just) for the logging messages - if 'logger' is not 'None'.
        :return: 'True' if 'path' is an EXISTING FOLDER.
        """
        # Normalize path for SFTP and ensure compartibiity even if remote host is Windows
        path_str = str(path).replace('\\', '/') 
        log_prefix = f"{description_str}: " if description_str else ""

        if logger:
            logger.debug(f"{log_prefix}-Checking if remote path is a regular folder: {path_str!r}")

        try:
            # Retrieval of Metadata
            # sftp.lstat() is used specifically because it does not follow symbolic links and explicitly reject symlinks as per the method requirements
            attrs = sftp.lstat(path_str)
            mode = attrs.st_mode

            # Check for symbolic links to strictly adhere to the requirements that symlinks are not deemed regular folders
            if stat.S_ISLNK(mode):
                if logger:
                    logger.debug(f"{log_prefix}-Path is a symbolic link: {path_str!r}.")
                return False
            
            # Check for directory or junction
            if stat.S_ISDIR(mode):
                if logger:
                    logger.debug(f"{log_prefix}-Path is a regular folder/Windows junction: {path_str!r}")
                return True
            
            # If path exists but is a file, socker or pipe, it returns False
            if logger:
                logger.debug(f"{log_prefix}-Path exists but is not a folder (mode: {mode:o}): {path_str!r}") # mode logged in octal for easier debugging of permissions
            return False
        except OSError as e:
            # catch and log OS errors like Permission denied or Connection loss and re-raise to ensure the caller is aware of the execution failure
            if logger:
                logger.error(f"{log_prefix}-OS Error accessing {path_str!r}: {e}")
            raise
            
    
   
    @classmethod
    def create_folder_path_recursively(
        cls,
        folder_path: typing.Union[str, pathlib.Path],
        sftp: "paramiko.sftp_client.SFTPClient",
        logger: typing.Union[None, logging.Logger]=None
    ) -> int:
        # Normalization and splitting - converting all backslashes to forward slashes as SFTP prefers forward slashes.
        path_str = str(folder_path).replace('\\', '/')
        parts = [p for p in path_str.split('/') if p]   # breaks the path into a list of folder names.

        if logger:
            logger.info(f"Creating remote folder recursively: {path_str!r}")

        if cls.is_path_a_regular_folder(path_str, sftp, logger, "created_folder_path_recursively"):
            if logger:
                logger.debug(f"Target folder already exists: {path_str!r}")
            return 0

        current_path = "/" if path_str.startswith('/') else ""
        creation_count = 0

        # Checks if all folders including current as path exists or not
        for part in parts:
            current_path = f"{current_path.rstrip('/')}/{part}"
            try:
                attrs = sftp.lstat(current_path)
                if not stat.S_ISDIR(attrs.st_mode): # Prevents the error of creating a folder inside a file
                    raise OSError(f"Path component exists but is not a folder: {current_path}")
            except FileNotFoundError:
                if logger:
                    logger.info(f"Creating remote folder: {current_path}")
                sftp.mkdir(current_path) # If lstat fails with a FileNotFoundError, i.e. folder is missing, then it gets created
                creation_count += 1 # number of new folders added
            except OSError:
                raise
        return creation_count 
        


