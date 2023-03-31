import os
import shutil
import glob
from datetime import datetime
import hashlib
import time
import sys
import argparse

"""
This python script implements a program that synchronizes two folders: source and replica. The
program maintains a full, identical copy of source folder at replica folder.  The synchronization
can be performed periodically as per command line interface. File creation, copying, and removal
operations are logged to a specified file and to the console output.  Please note that all files
in the replica folder that do not match the source folder will be deleted.

Call this program in the command line interface by using the following format:
python backup.py /path/to/source/folder /path/to/replica/folder /path/to/log_file_folder {synchronization_interval_in_sec}
ex:  python backup.py /home/code/DevelopmentQA/source /home/code/DevelopmentQA/replica /home/code/DevelopmentQA/log_files 30
"""


def md5_of_file(file, size = 4096):
    """
    This function calculates and returns the MD5 hash of the input file.  This MD5 hash will be
    used to check the integrity of the file, and detect any changes made to that file by the
    attribute that even small changes to the file will result in significantly different hash values.
    """
    hash_md5 = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(size), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def file_backup(sourch_folder_path, replica_folder_path, log_file):
    """
    This function synchronizes the source folder to the replica folder in one-way. After the function
    is complete the synchronization content of the replica folder is modified to exactly match content
    of the source folder.  This is function is called recursively if there is a folder within the
    source folder.
    """

    # Iterate through each file and folder in the source folder
    for file in os.listdir(sourch_folder_path):
        source_path = os.path.join(sourch_folder_path, file)
        replica_path = os.path.join(replica_folder_path, file)


        # If the file is a folder, then call the function recursively with the file as the new source path
        if os.path.isdir(source_path):
            # Make a new replica folder if it does not exsist
            if not os.path.exists(replica_path):
                os.makedirs(replica_path)
            file_backup(source_path, replica_path, log_file)


        # If the file is not a folder
        if os.path.isfile(source_path):

            # If the file is does not exist in the replica folder, then copy to the replica folder
            if not os.path.exists(replica_path):
                shutil.copy2(source_path, replica_path, follow_symlinks=False)
                log_file.write(f"{file} is a new backed up file."+"\n")
                print(f'{file} is a new file to be backed up')

            # If the file exists in the replica folder, check if it has been updated.
            else:
                if md5_of_file(source_path) != md5_of_file(replica_path):
                    # If the files has been updated, copy and replace the file in the replica folder
                    shutil.copy2(source_path, replica_path, follow_symlinks=False)
                    log_file.write(f"{file} is an updated file and backed up."+"\n")
                    print(f'{file} is an updated file backed up to {replica_path}')
                else:
                    # If the files has not been updated, don't copy, but log the status
                    log_file.write(f"{file} has NOT been updated since last backup."+"\n")
                    print(f'{file} has NOT been updated since last backup')

    # Check for deleted files. Please Note: Alternative method woudl be by iterating over the replica folder with os.listdir.
    # Get list of files in Source Folder
    source_files = []
    for filename in glob.iglob(sourch_folder_path + '**/**', recursive=True):
        file_name = filename.split(sourch_folder_path)
        source_files.append(file_name[1])
    source_files=source_files[1:]

    # Get list of files in Replica Folder
    replica_files = []
    for filename in glob.iglob(replica_folder_path + '**/**', recursive=True):
        file_name = filename.split(replica_folder_path)
        replica_files.append(file_name[1])
    replica_files=replica_files[1:]

    # Find deleted files and remove the files in the replica folder
    deleted_files = []
    for file in replica_files:
        if file not in source_files:
            deleted_files.append(file)
            print(f'\n{file} has been delected in {sourch_folder_path} folder\n')

            #Remove deleted Files
            replica_path = os.path.join(replica_folder_path, file[1:])
            if os.path.isfile(replica_path):
                os.remove(replica_path)
            elif os.path.isdir(replica_path):
                shutil.rmtree(replica_path)

    log_file.write(f'\nFiles Deleted since last backup in folder {sourch_folder_path}: \n')
    if len(deleted_files) == 0:
        log_file.write('None'+"\n\n")
    for item in deleted_files:
        log_file.write(item+"\n")


if __name__ == "__main__":
    """
    Define Source, Replica, and Log folders and sycronization interval from command line arguments.
    Create log and call file backup function. Keep performing the backup at the specified time intervals
    """

    # Take and Parse Command Line Arguments
    parser = argparse.ArgumentParser(description="Synchronize two folders.")
    parser.add_argument("source_folder", help="path to the source folder")
    parser.add_argument("replica_folder", help="path to the replica folder")
    parser.add_argument("log_folder", help="path to the log file folder")
    parser.add_argument("sync_interval", type=int, help="Synchronization interval in second:")
    args = parser.parse_args()

    #Alternative method for cleaner user interface by asking user input for each input
    #source_folder = input("Source folder path: ")
    #replica_folder = input("Replica folder path: ")
    #log_folder = input("Log File folder path: ")
    #sync_interval = int(input("Synchronization interval in second: " ))

    # Check that the replica folder exsists, if not, create the folder
    if not os.path.exists(args.replica_folder):
        print('Replica folder did not exist, making a new one')
        os.makedirs(args.replica_folder)

    # Check that the log folder exsists, if not, create the folder
    if not os.path.exists(args.log_folder):
        print('Replica folder did not exist, making a new one')
        os.makedirs(args.log_folder)

    # Create the log file as a .txt with the date and time of starting the program
    log_filename = f'backup_log_{datetime.now().strftime("%Y%m%d_%H%M")}.txt'

    # Open log file for writing
    with open(os.path.join(args.log_folder,log_filename),'w') as log_file:

        # Periodically synchronize folders, with program asleep for the user specified time interval
        while True:

            log_file.write(f'Folder Synchronization started at {datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}'+'\n\n')
            file_backup(args.source_folder, args.replica_folder, log_file)
            print('Backup is finished'+"\n\n\n")
            log_file.write('\n'+f'Backup Finished at {datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}'+'\n\n\n\n\n\n\n')

            time.sleep(args.sync_interval)
            # Please note that a program such as this would probably run in such short time spans as seconds, so the
            # schedule module or alternative may be better when used as a backup system. However for the purposing of
            # a test task, seconds is a sufficient interval for evaluation.
