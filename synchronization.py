import os
import filecmp
import shutil
import sys
import time

# Path to the python file location.
concurrent_location = os.path.realpath(os.getcwd())

# Default source directory.
source_path = concurrent_location + '\\' + 'sourceDirectory'

# Default replica directory.
replica_path = concurrent_location + '\\' + 'replicaDirectory'

# Default synchronization interval.
synchronization_interval = 1

# Default log file path.
log_file_path = concurrent_location + '\\' + 'log.txt'

log_file = None


# Function for the synchronization of the directories.
def synchronization(source, replica):
    # Using the function dircmp to compare the two directories.
    comparison = filecmp.dircmp(source, replica)

    # Deleting the files only present in the replica directory.
    for to_eliminate in comparison.right_only + comparison.diff_files:
        content_removal(os.path.join(replica, to_eliminate))

    # Copying the files only present in the source directory.
    for to_add in comparison.left_only + comparison.diff_files:
        content_creation(os.path.join(source, to_add), replica)

    # The dircmp function executes a "shallow" comparison of the files, neglecting their contents.
    # This part compares the content within the files to determine their similarity.
    for file in comparison.common_files:
        if not filecmp.cmp(os.path.join(source, file), os.path.join(replica, file), shallow=False):
            content_removal(os.path.join(replica, file))

    # Recursive comparison of the subdirectories within the source and replica directories.
    for subdir in comparison.common_dirs:
        synchronization(os.path.join(source, subdir), os.path.join(replica, subdir))


# Function for copying the content from the source directory to the replica directory.
def content_creation(content_path, destination):
    if os.path.isdir(content_path):
        shutil.copytree(content_path, os.path.join(destination, os.path.basename(content_path)))
        log('Copying the directory ' + os.path.basename(content_path))
    else:
        shutil.copy2(content_path, destination)
        log('Copying the file ' + os.path.basename(content_path))


# Function for removing content from the replica directory.
def content_removal(content_path):
    if os.path.isdir(content_path):
        shutil.rmtree(content_path)
        log('Removing the directory ' + os.path.basename(content_path))
    else:
        os.remove(content_path)
        log('Removing the file ' + os.path.basename(content_path))


# Function for logging information into the console and the log file.
def log(text):
    if log_file is not None:
        print(text)
        log_file.write(text + '\n')


# Verification that command line arguments are valid.
try:
    if len(sys.argv) == 5 and os.path.isdir(sys.argv[1]) and os.path.isdir(sys.argv[2]) and float(sys.argv[3]) > 0 and \
            os.path.isdir(sys.argv[4]):
        source_path = sys.argv[1]
        replica_path = sys.argv[2]
        synchronization_interval = float(sys.argv[3])
        log_file_path = sys.argv[4] + '\\' + 'log.txt'
except ValueError:
    pass


# Displaying the current source and replica directories, synchronization interval, and log file location.
print("Source: " + source_path)
print("Replica: " + replica_path)
print("Synchronization Interval: " + str(synchronization_interval))
print("Log file: " + log_file_path)

print("The synchronization is starting, you can stop this process by pressing CTRL + C.")


if __name__ == "__main__":
    # Creating a log.txt file or
    # appending new information to an existing log.txt file.
    log_file = open(log_file_path, 'a')
    try:
        # Periodical synchronization of the directories.
        while True:
            synchronization(source_path, replica_path)
            time.sleep(synchronization_interval)
    # Exiting the program by pressing CTRL + C.
    except KeyboardInterrupt:
        log_file.close()

