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
        path_str = str(path).replace('\\', '/') # Normalize for SFTP
        log_prefix = f"{description_str}: " if description_str else ""

        if logger:
            logger.debug(f"{log_prefix}-Checking if remote path is a regular folder: {path_str!r}")

        try:
            attrs = sftp.lstat(path_str)
            mode = attrs.st_mode

            if stat.S_ISLNK(mode):
                if logger:
                    logger.debug(f"{log_prefix}-Path is a symbolic link: {path_str!r}.")
                return False
            
            if stat.S_ISDIR(mode):
                if logger:
                    logger.debug(f"{log_prefix}-Path is a regular folder/Windows junction: {path_str!r}")
                return True
            if logger:
                logger.debug(f"{log_prefix}-Path exists but is not a folder (mode: {mode:o}): {path_str!r}")
            return False
        except OSError as e:
            if logger:
                logger.error(f"{log_prefix}-OS Error accessing {path_str!r}: {e}")
            raise
            
    
   


