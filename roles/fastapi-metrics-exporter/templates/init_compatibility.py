#!/usr/bin/env python3
"""
Compatibility initialization script that must be imported before other modules
to patch filesystem operations for Proxmox v9 compatibility.
"""

import os
import sys
import logging

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def init_filesystem_compatibility():
    """Initialize filesystem compatibility patches."""
    try:
        # Import our safe filesystem collector
        from safe_filesystem_collector import safe_collector, patched_disk_usage, patched_disk_partitions
        
        # Apply the monkey patches to psutil
        import psutil
        psutil.disk_usage = patched_disk_usage
        psutil.disk_partitions = patched_disk_partitions
        
        # Log configuration
        exclude_paths = os.environ.get('FILESYSTEM_EXCLUDE_PATHS', '')
        exclude_types = os.environ.get('FILESYSTEM_EXCLUDE_TYPES', '')
        
        logging.info("Filesystem compatibility patches applied")
        logging.info(f"Excluded paths: {exclude_paths}")
        logging.info(f"Excluded types: {exclude_types}")
        
        return True
        
    except ImportError as e:
        logging.warning(f"Could not import filesystem compatibility module: {e}")
        return False
    except Exception as e:
        logging.error(f"Error initializing filesystem compatibility: {e}")
        return False

# Auto-initialize when this module is imported
if __name__ != "__main__":
    init_filesystem_compatibility()
else:
    # Test mode
    print("Testing filesystem compatibility initialization...")
    result = init_filesystem_compatibility()
    print(f"Initialization {'succeeded' if result else 'failed'}")
    
    if result:
        import psutil
        print("Testing patched psutil functions...")
        
        # Test disk_partitions
        partitions = psutil.disk_partitions()
        print(f"Found {len(partitions)} accessible partitions")
        
        # Test disk_usage on safe paths
        for partition in partitions[:3]:  # Test first 3 partitions
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                print(f"  {partition.mountpoint}: {usage.total // (1024**3)} GB")
            except Exception as e:
                print(f"  {partition.mountpoint}: Error - {e}")