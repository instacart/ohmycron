from datetime import datetime
import errno
import fcntl
import getpass
import logging
import logging.handlers
import os
import pipes
import tempfile

from argh import arg


log = logging.getLogger(__package__)


@arg('args', nargs='*', help='Command and arguments.')
@arg('--token', help='Unique token for task (defaults to command name).')
@arg('--do-not-lock', help='Disable locking on the token.')
@arg('--debug', help='Log commands that are run (NB: might expose secrets).')
def omc(args, token=None, do_not_lock=False, debug=False):
    token = token if token is not None else args[0]
    token = token.split('/')[-1]
    argv = ['/bin/bash', '-l', '-c', bash_driver(), token] + args

    if debug:
        setup_logger(level=logging.DEBUG)

    log.debug('argv: %s', escape(argv))

    def task():
        os.execlp(argv[0], *argv)

    if not do_not_lock:
        d = os.path.join(tempfile.gettempdir(), 'omc~' + getpass.getuser())
        # Maybe someday, allow shared, explicitly namespaced tokens.
        f = token if '/' in token else os.path.join(d, token)
        log.debug('Would lock: %s', f)
        flock(f, task)
    else:
        log.debug('Not locking.')
        task()


handler = None


def setup_logger(logger=log, level=logging.INFO):
    logger.setLevel(level)
    global handler
    if handler is None:
        dev = '/dev/log' if os.path.exists('/dev/log') else '/var/run/syslog'
        fmt = (logger.name +
               '[%(process)d]: %(name)s.%(funcName)s() %(message)s')
        handler = logging.handlers.SysLogHandler(address=dev)
        handler.setFormatter(logging.Formatter(fmt=fmt))
        logger.addHandler(handler)
    handler.setLevel(level)


def flock(path, fn):
    d = os.path.dirname(path)
    try:
        os.makedirs(d)
    except OSError as e:
        if not (e.errno == errno.EEXIST and os.path.isdir(d)):
            raise Err('Not able to create dir: %s' % d)
    with open(path, 'a+') as handle:
        handle.seek(0)
        try:
            fcntl.flock(handle, fcntl.LOCK_NB | fcntl.LOCK_EX)
        except IOError as e:
            if e.errno not in [errno.EACCES, errno.EAGAIN]:
                raise e
            txt = handle.read().strip()
            if len(txt) > 0:
                log.warning('Last holder: %s', txt)
            raise Err('Not able to lock: %s' % path)
        handle.truncate(0)
        handle.write('pid %d at %s\n' % (os.getpid(), datetime.utcnow()))
        try:
            fn()
        finally:
            handle.truncate(0)


def bash_driver(code=None):
    return '\n'.join(['exec 1> >(exec logger -t "$0[$$]" -p user.info)',
                      'exec 2> >(exec logger -t "$0[$$]" -p user.notice)',
                      'export PATH=/usr/local/bin:"$PATH"',
                      'for f in ~/.bashrc ~/.bash_profile ~/.profile',
                      'do [[ ! -s $f ]] || source "$f"',
                      'done',
                      'exec "$@"' if code is None else code])


def escape(argv):
    # NB: The pipes.quote() function is deprecated in Python 3
    return ' '.join(pipes.quote(_) for _ in argv)


class Err(RuntimeError):
    pass
