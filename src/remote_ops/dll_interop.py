import os
import sys
import logging

logger=logging.getLogger(__name__) # logger instance
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

try:
    import clr
except ImportError:
    logger.error(f"Error: 'pythonnet' library is required.")

def load_mitsubishi_dll(dll_path: str):
    """Loads the target 64-bit DLL file and inspect the Managed Factory"""
    if not os.path.exists(dll_path):
        raise FileNotFoundError(f"DLL not found at {dll_path}")
    
    sys.path.append(os.path.dirname(dll_path))
    try:
        clr.AddReference("GXW3OpenIF64")
    except Exception as e:
        print(f"Failed to load DLL: {e}")
        return
    
    try: 
        from MitsubishiElectric.FA.PLC import GXW3OpenIFManagedFactory

        factory = GXW3OpenIFManagedFactory()
        all_attributes = dir(factory)
        methods = [attr for attr in all_attributes if not attr.startswith('__') and callable(getattr(factory, attr))]

        return sorted(methods)
    except ImportError:
        logger.error(f"Namespace MitsubishiElectric.FA.PLC not found in DLL.")
    except Exception as e:
        logger.error(f"Error during factory instantiation: {e}")