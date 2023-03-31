# Junior Developer in QA: Test Task

This is **S. Shimizu's** technical task for the **Junior Developer in QA**.  


Call the program **backup.py**, in the command line interface by using the following format:

**python backup.py /path/to/source/folder /path/to/replica/folder /path/to/log_file_folder {synchronization_interval_in_sec}**

ex: *python backup.py /home/code/DevelopmentQA/source /home/code/DevelopmentQA/replica /home/code/DevelopmentQA/log_files 30*

### Prompt
The program, **backup.py**, completes the following prompt using Python:

*Please implement a program that synchronizes two folders: source and replica. The program should maintain a full, identical copy of source folder at replica folder.*

- *Synchronization must be one-way: after the synchronization content of the replica folder should be modified to exactly match content of the source
folder;*
- *Synchronization should be performed periodically.File creation/copying/removal operations should be logged to a file and to the
console output;*
- *Folder paths, synchronization interval and log file path should be provided using the command line arguments;*
- *It is undesirable to use third-party libraries that implement folder synchronization;*
- *It is allowed (and recommended) to use external libraries implementing other well-known algorithms. For example, there is no point in implementing yet another function that calculates MD5 if you need it for the task – it is perfectly acceptable to use a third-party (or built-in) library.*



