#!/usr/bin/env python3
"""
Wrapper script to start the metrics exporter with filesystem compatibility patches.
"""

import os
import sys
import logging

# Setup logging
log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main wrapper function."""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Add to Python path
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    
    # Initialize compatibility patches
    logger.info("Initializing filesystem compatibility patches...")
    try:
        import init_compatibility
        logger.info("Filesystem compatibility patches loaded successfully")
    except Exception as e:
        logger.warning(f"Could not load compatibility patches: {e}")
        logger.info("Continuing without patches...")
    
    # Import and run the main application
    logger.info("Starting metrics exporter application...")
    try:
        # Import the main module from the same directory
        main_py_path = os.path.join(script_dir, 'main.py')
        if os.path.exists(main_py_path):
            # Change to the script directory
            os.chdir(script_dir)
            
            # Try multiple approaches to run the main module
            try:
                # Method 1: Import as module
                import importlib.util
                spec = importlib.util.spec_from_file_location("main", main_py_path)
                main_module = importlib.util.module_from_spec(spec)
                sys.modules["main"] = main_module
                
                # Set __name__ to __main__ so the main module thinks it's being run directly
                main_module.__name__ = "__main__"
                
                # Execute the main module
                spec.loader.exec_module(main_module)
                
            except Exception as import_error:
                logger.warning(f"Import method failed: {import_error}")
                logger.info("Trying direct execution method...")
                
                # Method 2: Direct execution with proper globals
                with open(main_py_path, 'r') as f:
                    code = f.read()
                
                # Set up globals as if this was run directly
                main_globals = {
                    '__file__': main_py_path,
                    '__name__': '__main__',
                    '__package__': None,
                }
                main_globals.update(globals())
                
                exec(code, main_globals)
            
        else:
            logger.error(f"Could not find main.py at {main_py_path}")
            sys.exit(1)
            
    except SystemExit:
        # Allow clean exits
        raise
    except Exception as e:
        logger.error(f"Error starting metrics exporter: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise

if __name__ == "__main__":
    main()