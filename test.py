import os
import filecmp
#import shutil
#import sys

concurrent_location = os.path.realpath(os.getcwd())

source_path = concurrent_location + '\\' + 'sourceDirectory'

replica_path = concurrent_location + '\\' + 'replicaDirectory'

synchronization_interval = 1

log_file_path = concurrent_location


def synchronization(source, replica):
    comparison = filecmp.dircmp(source, replica)

    for subdir in comparison.common_dirs:
        synchronization(os.path.join(source, subdir), os.path.join(replica, subdir))
    # Files and directories to copy
    #
    # comparison.left_only

    # Files and directories to eliminate
    #
    # comparison.right_only

    # Files to eliminate and copy
    #
    # comparison.diff_files

    #message


def file_creation():
    pass


def file_copying():
    pass


def file_removal():
    pass


synchronization(source_path, replica_path)
