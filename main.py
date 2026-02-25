from src.remote_ops.dll_interop import load_mitsubishi_dll
import logging

logger=logging.getLogger(__name__) # logger instance
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')







if __name__ == "__main__":
    # dll_file_path = r"C:\Users\paste correct dll file path here\GXW3OpenIF32.dll"
    dll_file_path = r"C:\Users\chidi\Documents\p4d-remoteops-utils\dlls\GXW3OpenIF32.dll"
    methods = None

    try:
        methods = load_mitsubishi_dll(dll_path=dll_file_path)
    except FileNotFoundError as e:
        logger.error(f"DLL file missing: {e}")
    except ImportError as e:
        logger.error(f"Namespace or library error: {e}")
    except Exception as e:
        logger.error(f"Unexpected failure during DLL inspection: {e}")

    if methods:
        logger.info(f"Successfully found {len(methods)} methods! \n{methods}")
    else:
        logger.warning(f"No methods were extracted. See logs for details.")