thaniya_server_sudo
==========

Introduction
------------

This python module is part of the Thaniya server. It provides a way to run scripts via sudo in a controlled way.

Information about this module can be found here:

* [github.org](https://github.com/jkpubsrc/....)
* [pypi.python.org](https://pypi.python.org/pypi/thaniya_server_sudo)

Why this module?
----------------

It would be easy to run the Thaniya backup system as `root` to have best possibilities to reconfigure and control the system. (Background: Thaniya uses system accounts to provide endpoints for uploads.) However this would be a bad design: Running a python application as `root` must be considered as a security problem! There might be at least a theoretical possibility for some kind of bug that could potentionally be exploited by regular users. Therefore the Thaniya server is designed to **not** run as `root`.

But if the server does not run as `root` a problem exists: The server must assign new passwords to system accounts and access data uploaded to that system accounts. To compensate for this problem this module has been written: It provides a simple facility to run bash scripts as `root`.

Limitations of this module
--------------------------

...

How to use this module
----------------------

### Import this module

Please include this module into your application using the following code:

```python
import thaniya_server_sudo
```

...

Contact Information
-------------------

This work is open source. Therefore you can use this work for free.

We - the subspecies of software developers - can make great things. However, the more we collaborate the more fantastic the things we create can get. Therefore, please contact the authors listed below to give feedback, to leave a comment, to provide hints and ideas, to suggest improvements or to initiate possible collaborations.

* Jürgen Knauth: pubsrc@binary-overflow.de"

License
-------

This software is provided under the following license:

* Apache Software License 2.0



