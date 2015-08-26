# `ohmycron` -- all those things you always do for cron

Frequently when debuggin cron jobs, one finds that:

* One needs to use locks to keep more than one copy of frequently running jobs
  from running at the same time.

* One wishes to load the user environment -- `/etc/profile` as well as RC
  files in `HOME`.

* The path should include `/usr/local/bin`.

* The output of the cron job should be logged to Syslog, which both prevents
  cron from raising errors about mailers and allows you to see what went wrong
  if something did.

`ohmycron` does all this and more, managing locks with a POSIX API, so that
the OS takes care of cleaning up locks for failed proceseses.


# `ohmycron` as a wrapper

Prepending `ohmycron` to the commands in your crontab keeps your crontab clean
and transparently adds logging, locking and environment loading.

```crontab
* * * * *  root  ohmycron sleep 10
* * * * *  root  ohmycron --tag update:ohmycron -- curl -sSfL 'https://raw.githubusercontent.com/instacart/ohmycron/master/ohmycron' -o /usr/bin/ohmycron
```

# Installation

```bash
sudo curl -sSfL 'https://raw.githubusercontent.com/instacart/ohmycron/master/ohmycron' -o /usr/bin/ohmycron
sudo chmod a+rx /usr/bin/ohmycron
```
