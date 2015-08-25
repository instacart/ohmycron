#!/usr/bin/env python
import logging

import argh

from . import Err, omc, setup_logger


log = logging.getLogger(__package__)


def main():
    setup_logger()
    try:
        argh.dispatch_command(omc)
    except Err as e:
        log.error(e.message)
    except:
        log.exception('Internal error.')


if __name__ == '__main__':
    main()
