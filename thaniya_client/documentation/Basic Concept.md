Basic Concept
================================================================

General Workflow
----------------------------------------------------------------

In order to perform a backup a backup script needs to be conform to the following workflow:

* First: Instantiate a backup connector. This backup connector will represent our connection to a server (or at least some kind of target directory).
* Then **initalize** the backup connector. If this is a network based connector it will mount a remote share for writing.
* Now perform the backup. This is done by creating new files in the backup directory and filling them with data.
* After all files have been written **deinitialize** the backup connector. If this is a remote share the share is disconnected.

Why this architecture?
----------------------------------------------------------------

Why this architecture? The reason is simple:

* It is universal. In theory even a bash script could be used to follow this work flow, given that initialization and deinitialization is performed by a specific tool dedicated to this matter.
* There already exist quite a variety of tools that will create backup files. E.g. `mysqldump` is capable of writing data of a database to one or more backup files. Providing a directory where these tools can write data to is the easiest and best way to reuse them.

Backup Driver
----------------------------------------------------------------

The backup driver is 


Mount Point Manager
----------------------------------------------------------------

For mouting a remote network share you have two options:

1. specify a static, fixed directory that will used every time for backup;
2. specify a mount point manager that will handle provisioning of a fresh directory for backups.

This functionality is provided by a mount point manager.


Backup Task
----------------------------------------------------------------






















