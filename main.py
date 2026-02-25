import logging
from src.remote_ops.dll_interop import inspect_mitsubishi_dll


logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger=logging.getLogger(__name__) # logger instance


def main():
    dll_file_path = r"paste your dll file path here"
    methods = None
    logger.info("Starting DLL Inspection Task ...")
    try:
        methods = inspect_mitsubishi_dll(dll_path=dll_file_path)
        if methods:
            logger.info(f"Successfully found {len(methods)} methods! \n{methods}")
    except FileNotFoundError as e:
        logger.error(f"DLL file missing: {e}")
    except ImportError as e:
        logger.error(f"Namespace or library error: {e}")
    except Exception as e:
        logger.error(f"Unexpected failure during DLL inspection: {e}")





if __name__ == "__main__":
    main()
    