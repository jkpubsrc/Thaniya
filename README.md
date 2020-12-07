Thaniya Server / Thaniya Client
===============================

Introduction
------------

This is the group of python modules and programs that implement the Thaniya backup server and the Thaniya backup client module.

The Thaniya backup server consisist of an *upload server*, an *archive server* and a *server management command line tool*. These programs orchestrate standard functionality of a Linux system, such as managing system accounts and other things to receive uploads from backup clients via SCP. And this is a main differences to other backup solutions: By managing well tested and readily available capabilities of a Linux operting system reliability and security of the backup solution can be achieved.

For performing backups typically a GUI is provided. Not in this specific case: The Thaniya backup system (currently) comes only with a *client library*. This again is one of the main differences to other backup solutions: By not providing a GUI but a client library we enable other projects to include support of the Thaniya backup system. Additionally users can write custom backup scripts perfectly tailored to their needs that run in the command line, taking full advantage of Python as they effectively write python programs. Further more following this concept of modularity performing backups can even be integrated into other tasks such as build scripts or other forms of automated data processing. In general: In any kind of activity where creating a backup of some kind of data in an automated way might be a good idea.

So the focus for the Thaniya backup is a bit different than many other backup systems: It's not only for regular end users, it's for system adminstrators, for scientists doing some kind of data processing and for programmers of various kind that would like to interface a backup infrastructure directly. At the same time Thaniya backup focuses on maximizing compatibility with current and future systems as only existing compression and data transfer standards are (and should be) used.

Thaniya will *not* maximize the use of storage capacities by storing data in a proprietary way. Though of course this approach would have its advantages the Thaniya backup intentionally makes use of standrd file system and standard archiving and compression tools only: It facilitates `tar`, `gzip`, `bzip2` and `xz` to perform backups. By focusing on that kind of simplicity Thaniya maximizes your chances of recovering from a desaster situation: In the case of all cases you necessarily wouldn't even need the Thaniya backup system itself for recovery.

Current State of Development
----------------------------

Right now the following operating systems are supported:

* Server: Ubuntu Linux. (Other Linuxes should work out of the box.)
* Client: Everything Linux-like operating system that supports Python. (A port to other programming languages and other operating systems should not be too difficult.)

The project is in an alpha stage. Though the data formats used are pretty stable and the code is of quite good quality the code will undergo some refactoring until a beta version can be released. That means: In theory the Thaniya backup system can be used right now "out of the box". However aspects of installation and operation are likely to change to some extent untill the first release is commplete.

Feel free to contact the author of this backup system if you're interested in using it or contributing to it.

Installation
----------------------

This description has not yet been completed.

Documentation
----------------------

This description has not yet been completed.

Contact
-------

This work is open source. Therefore you can use this work for free.

We - the subspecies of software developers - can make great things. However, the more we collaborate the more fantastic the things we create can get. Therefore, please contact the authors listed below to give feedback, to leave a comment, to provide hints and ideas, to suggest improvements or to initiate possible collaborations.

* Jürgen Knauth: pubsrc@binary-overflow.de"

License
-------

This software is provided under the following license:

* Apache Software License 2.0



