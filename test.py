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


if len(sys.argv) == 5 and os.path.isdir(sys.argv[1]) and os.path.isdir(sys.argv[2]) and float(sys.argv[3]) > 0 and \
        os.path.isdir(sys.argv[4]):
    source_path = sys.argv[1]
    replica_path = sys.argv[2] if not os.path.samefile(sys.argv[2], sys.argv[1]) else replica_path
    synchronization_interval = float(sys.argv[3])
    log_file_path = sys.argv[4] if not os.path.samefile(sys.argv[4], sys.argv[1]) and not \
        os.path.samefile(sys.argv[4], sys.argv[2]) else concurrent_location

print(source_path)
print(replica_path)
print(synchronization_interval)
print(log_file_path)

# synchronization(source_path, replica_path)
