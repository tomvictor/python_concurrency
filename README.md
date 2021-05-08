# python_concurrency
 Reference code 


Notes
=====

Process start threads
one gil for every python process


Process
=======

* It is created by the parent process.
* It can not create new child process.
* It is suitable for background tasks
* By default (If not specified while creating a Process), type of process is inherited from the creating process.

Daemon process
--------------

* When a process exits, it terminates all its child daemon processes.

Non daemon process
-------------------
* If the process has child processes which are not daemon processes, the process will not exit until all its child process are exited