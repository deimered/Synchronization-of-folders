import os
import filecmp
import shutil
import sys

concurrent_location = os.path.realpath(os.getcwd())

source_path = concurrent_location + '\\' + 'sourceDirectory'

replica_path = concurrent_location + '\\' + 'replicaDirectory'

synchronization_interval = 1

log_file_path = concurrent_location


def synchronization(source, replica):
    comparison = filecmp.dircmp(source, replica)

    # Test without os.path.basename

    for to_eliminate in comparison.right_only + comparison.diff_files:
        content_removal(os.path.join(replica, os.path.basename(to_eliminate)))

    for to_add in comparison.left_only + comparison.diff_files:
        content_creation(os.path.join(source, os.path.basename(to_add)), replica)

    for file in comparison.common_files:
        if not filecmp.cmp(os.path.join(source, file), os.path.join(replica, file), shallow=False):
            content_removal(os.path.join(replica, os.path.basename(file)))

    for subdir in comparison.common_dirs:
        synchronization(os.path.join(source, subdir), os.path.join(replica, subdir))


def content_creation(content_path, destination):
    if os.path.isdir(content_path):
        shutil.copytree(content_path, os.path.join(destination, os.path.basename(content_path)))
    else:
        shutil.copy2(content_path, destination)


def content_removal(content_path):
    if os.path.isdir(content_path):
        shutil.rmtree(content_path)
    else:
        os.remove(content_path)


synchronization(source_path, replica_path)