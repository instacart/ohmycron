# `ohmycron` -- Cron simplified

Frequently when debugging cron jobs, one finds that:

* One needs to use locks to keep more than one copy of frequently running jobs
  from running at the same time.

* One wishes to load the user environment -- `/etc/profile` as well as RC
  files in `HOME`.

* Generally, one would `cd` to `HOME` for application specific users.

* The path should include `/usr/local/bin`.

* The output of the cron job should be logged to Syslog, which both prevents
  `cron` from raising errors about mailers and allows you to see what went
  wrong if something did.

`ohmycron` does all this and more, managing locks with a POSIX API, so that
the OS takes care of cleaning up locks for failed proceseses.


# `ohmycron` as a wrapper

Prepending `ohmycron` to the commands in your crontab keeps your crontab clean
and transparently adds logging, locking and environment loading.

```crontab
* * * * *  root  ohmycron sleep 10
* * * * *  root  ohmycron --tag update:ohmycron -- curl -sSfL 'https://raw.githubusercontent.com/instacart/ohmycron/master/ohmycron' -o /usr/local/bin/ohmycron
```

# `ohmycron` as the cron shell

Setting `SHELL=/usr/local/bin/ohmycron` (or another path if you have installed
`ohmycron` elsewhere) transparently adds locks, logging and environment setup
to all the jobs in a cron file. (Tasks are actually run with Bash.) It is does
something the wrapper can't do, too: support multi-statement commands which
use the shell operators `&&`, `|`, `||` and so forth.

```crontab
SHELL=/usr/local/bin/ohmycron
* * * * *  root  sleep 10
* * * * *  root  : update:ohmycron ; curl -sSfL 'https://raw.githubusercontent.com/instacart/ohmycron/master/ohmycron' -o /usr/local/bin/ohmycron
```

You can explicitly name a cron job with a Bash "no-op comment": `: <some
words> ;`. (In Bash, `:` is a no-op; the arguments to the no-op command are
ignored.)

# Installation

```bash
sudo curl -sSfL 'https://raw.githubusercontent.com/instacart/ohmycron/master/ohmycron' -o /usr/local/bin/ohmycron
sudo chmod a+rx /usr/local/bin/ohmycron
```
