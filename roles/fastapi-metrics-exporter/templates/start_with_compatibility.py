#!/usr/bin/env python3
"""
Wrapper script to start the metrics exporter with filesystem compatibility patches.
"""

import os
import sys
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
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
            # Execute the main.py file
            with open(main_py_path, 'r') as f:
                exec(f.read(), {'__file__': main_py_path})
        else:
            logger.error(f"Could not find main.py at {main_py_path}")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Error starting metrics exporter: {e}")
        raise

if __name__ == "__main__":
    main()