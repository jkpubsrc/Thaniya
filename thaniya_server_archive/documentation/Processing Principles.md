The archive will use three directories:

a) A temp directory
b) A data directory
c) A job directory

Important: The directory for temporary files and directories and the data directory **must** reside on the same file system. (This is checked on instatiation.) The reason for this is that the archive performs an import of data in an indempotent way where there is only a practicable way of importing the data if temp directory and data directory reside on the same file system.

This is how an import is performed:

* The archive learns about an import because it scans its job directory. All files ending with ".json" or ".jsonc" are recognized as a job. The first job is always the job with the lowest order in alphabetical sorting.
* The job file is read. If it violates required standards, an error message is written to the log and the job file is discarded (= deleted).
* A subdirectory is created in the temporary directory with the same name as the job. Then all data from the source is copied (!!) to this temporary directory. Packing is performed as required during this process.
* The subdirectory is then moved to its destination in the data directory. If there is already such a directory the old one will silently be discarded.
* The current backup archive object is invalidated. (= The object will drop all cached data.)
* The source directory is removed completely. If this fails an error log message is created.
* The job file is deleted.

These jobs are processed in a single background thread. So jobs are processed one after the other, never in parallel. (In parallel doesn't make too much sense as a job will utilize a single CPU core and I/O capabilities to the fullest: The first if data requires packing, the second if data is copied without change.

This processing scheme is indempotent. All aspects of processing are performed in a deterministic way. Therefore if the process is killed, everything still will be fine and on the next start the system will process everything as exepected again.

Q: How can we "nice" a background thread? Maybe: Very short delay between larger blocks of data copied/compressed to allow other processes to run?



