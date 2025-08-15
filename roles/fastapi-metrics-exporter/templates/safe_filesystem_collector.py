#!/usr/bin/env python3
"""
Safe filesystem collector wrapper that prevents permission errors
by excluding restricted paths and filesystem types.
"""

import os
import sys
import psutil
import logging

logger = logging.getLogger(__name__)

class SafeFilesystemCollector:
    """Wraps filesystem operations with path/type exclusions."""
    
    def __init__(self):
        self.exclude_paths = self._get_exclude_paths()
        self.exclude_types = self._get_exclude_types()
        
    def _get_exclude_paths(self):
        """Get list of paths to exclude from environment."""
        paths_str = os.environ.get('FILESYSTEM_EXCLUDE_PATHS', '')
        return [p.strip() for p in paths_str.split(',') if p.strip()]
        
    def _get_exclude_types(self):
        """Get list of filesystem types to exclude from environment."""
        types_str = os.environ.get('FILESYSTEM_EXCLUDE_TYPES', '')
        return [t.strip() for t in types_str.split(',') if t.strip()]
    
    def should_exclude_path(self, path):
        """Check if a path should be excluded."""
        # Check path exclusions
        for exclude_path in self.exclude_paths:
            if path.startswith(exclude_path):
                logger.debug(f"Excluding path {path} (matches {exclude_path})")
                return True
        return False
    
    def should_exclude_partition(self, partition):
        """Check if a partition should be excluded."""
        # Check path exclusions
        if self.should_exclude_path(partition.mountpoint):
            return True
            
        # Check filesystem type exclusions
        if partition.fstype in self.exclude_types:
            logger.debug(f"Excluding partition {partition.mountpoint} (fstype: {partition.fstype})")
            return True
            
        return False
    
    def safe_disk_usage(self, path):
        """Safely get disk usage, returning None if excluded or permission denied."""
        try:
            if self.should_exclude_path(path):
                return None
            return psutil.disk_usage(path)
        except PermissionError as e:
            logger.debug(f"Permission denied accessing {path}: {e}")
            return None
        except Exception as e:
            logger.warning(f"Error accessing {path}: {e}")
            return None
    
    def get_disk_partitions(self, all=False):
        """Get disk partitions, excluding restricted ones."""
        try:
            partitions = psutil.disk_partitions(all=all)
            return [p for p in partitions if not self.should_exclude_partition(p)]
        except Exception as e:
            logger.error(f"Error getting disk partitions: {e}")
            return []

# Create global instance
safe_collector = SafeFilesystemCollector()

# Monkey patch psutil functions
original_disk_usage = psutil.disk_usage
original_disk_partitions = psutil.disk_partitions

def patched_disk_usage(path):
    """Patched disk_usage that handles exclusions."""
    result = safe_collector.safe_disk_usage(path)
    if result is None:
        # Return original function for compatibility, but it might fail
        # This preserves the original behavior for non-excluded paths
        return original_disk_usage(path)
    return result

def patched_disk_partitions(all=False):
    """Patched disk_partitions that filters out excluded partitions."""
    return safe_collector.get_disk_partitions(all=all)

# Apply the monkey patches
psutil.disk_usage = patched_disk_usage
psutil.disk_partitions = patched_disk_partitions

if __name__ == "__main__":
    # Test the safe collector
    collector = SafeFilesystemCollector()
    print("Testing safe filesystem collector...")
    
    partitions = collector.get_disk_partitions()
    print(f"Found {len(partitions)} accessible partitions")
    
    for partition in partitions:
        usage = collector.safe_disk_usage(partition.mountpoint)
        if usage:
            print(f"  {partition.mountpoint}: {usage.total // (1024**3)} GB total")
        else:
            print(f"  {partition.mountpoint}: excluded or inaccessible")