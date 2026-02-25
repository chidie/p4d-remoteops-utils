import os
import sys
import logging

logger=logging.getLogger(__name__) # logger instance
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

try:
    import clr
except ImportError:
    logger.error(f"Error: 'pythonnet' library is required.")


def inspect_mitsubishi_dll(dll_path: str):
    """Loads the target 64-bit DLL file and inspect the Managed Factory Methods"""
    # Verification to ensure file exists
    if not os.path.exists(dll_path):
        raise FileNotFoundError(f"DLL not found at {dll_path}")
    
    sys.path.append(os.path.dirname(dll_path))  # Adds directory to sys.path so dependencies can be resolved
    try:
        clr.AddReference(dll_path) # loads the DLL file as a python module using pythonnet
    except Exception as e:
        logger.error(f"Failed to load DLL: {e}")
        return
    
    try: 
        from MitsubishiElectric.FA.PLC import GXW3OpenIFManagedFactory # misubishi namespace import

        # Using .NET reflection to inspect object
        factory = GXW3OpenIFManagedFactory() # instance of the factory
        all_attributes = dir(factory) # the dir() returns a list of strings containing attribute, variable, and method name
        methods = [attr for attr in all_attributes if not attr.startswith('__') and callable(getattr(factory, attr))] # Ignores components that starts with '__' and returns a list of methods that can be called with parenthesis ().
        return sorted(methods)
    except ImportError:
        logger.error(f"Namespace MitsubishiElectric.FA.PLC not found in DLL.")
    except Exception as e:
        logger.error(f"Error during factory instantiation: {e}")