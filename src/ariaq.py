#!/usr/bin/python3
"""
usage: ./ariaq.py [command] [args]
commands:
    add [link] [num]
    setpath [path]
    help
"""

import sqlite3
import os.path
import sys
import logging
from logging import debug, info, warning, error
from __init__ import *

cmds = {
    'add': {'add', 'a'},
    'setpath': {'setpath'}
}

logging.basicConfig(filename='ariaq.log', level=logging.INFO)


def main():
    debug(sys.argv)
    # handle cmds
    argv = sys.argv
    argc = len(argv)

    if argc < 2 or argv[1] == 'help':
        print(__doc__)

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    # check for first run
    if not os.path.isfile(FIRSTRUN_FILE):
        setup(c, conn)

    cmd = argv[1]
    if cmd in cmds['add']:
        pass
    elif cmd in cmds['setpath']:
        pass
    else:
        error_msg = f'Unrecognized command: {cmd}'
        error(error_msg)
        raise ValueError(error_msg)


def setup(c: sqlite3.Cursor, conn: sqlite3.Connection) -> None:
    debug("First run detected, creating Tasks table in DB")
    c.execute('''CREATE TABLE Tasks
                 (link text, num int)''')
    conn.commit()
    with open(FIRSTRUN_FILE, 'w') as firstrun:
        firstrun.write('first run')


if __name__ == '__main__':
    main()
