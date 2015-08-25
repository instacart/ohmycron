=======================================================
OhMyCron -- a wrapper for simple, predictable cron tabs
=======================================================

OhMyCron takes care of those noisome details -- ensuring only one instance of
a job runs at a time, logging job output, loading the expected environment --
that bedevil those of us running cron jobs in production.

.. code:: bash

  pip install omc

OhMyCron can be used as a wrapper.

.. code:: bash

  * * * * *  root  /usr/local/bin/omc command to run
  * * * * *  root  /usr/local/bin/omc -t first_sleep sleep 10
  * * * * *  root  /usr/local/bin/omc -t second_sleep sleep 10

It requires no configuration. (The shell used is always Bash; the "application
environment" is always loaded by using a login shell.)

OhMyCron locks the job by using ``flock``, a kernel API for locking files.
When a process terminates, all of its locks are cleaned up; and the kernel
ensures that only one process (or its children) holds the lock at a time.
Normally, the name of the token that is locked is the first word of the
command. To set the lock explicitly, use ``-t`` or ``--token``. Different
users have different lock namespaces.
