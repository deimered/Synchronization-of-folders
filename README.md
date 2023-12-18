# Synchronization-of-folders
A program designed to synchronize two folders: the source and the replica.

When executing the synchronization.py file, it will periodically synchronize the folders "sourceDirectory" and "replicaDirectory" every 1 second, logging the changes in the "log.txt" file.

The source folder, replica folder, synchronization interval, and log file path can be defined using five command-line arguments. These arguments must be passed in the following order with these restrictions:

Source folder: Must be a directory.
Replica folder: Must be a directory.
Synchronization interval: Must be greater than 0.
Log file path: Must be a directory.

If any of these conditions is not met, the program will use default values for the source folder, replica folder, synchronization interval, and log file path.

The libraries used in this program include:
os
filecmp
shutil
sys
time

