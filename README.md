# Junior Developer in QA: Test Task

This is **S. Shimizu's** technical task for the **Junior Developer in QA**.  


Call the program **backup.py**, in the command line interface by using the following format:

**python backup.py /path/to/source/folder /path/to/replica/folder /path/to/log_file_folder {synchronization_interval_in_sec}**

ex: *python backup.py /home/code/DevelopmentQA/source /home/code/DevelopmentQA/replica /home/code/DevelopmentQA/log_files 30*

### Usage
The program, **backup.py**, completes the following using Python:

- Synchronizes two folders: source and replica. The program maintains a full, identical copy of source folder at replica folder.
- Synchronization is one-way: after the synchronization content of the replica folder is modified to exactly match content of the source
folder.
- Synchronization is performed periodically. 
- File creation, copying, and removal operations are logged to a txt, file located in the log file folder, and to the console output.
- Folder paths, synchronization interval and log file path are provided using the command line arguments.


