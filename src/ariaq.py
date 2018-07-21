#!/usr/bin/python3
"""
usage: ./ariaq.py [command] [args]
commands:
    add [link] [num]
    status
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
    'status': {'status'}
}

logging.basicConfig(filename='ariaq.log', level=logging.INFO)


def get_status_message(c: sqlite3.Connection) -> str:
    num_jobs: int = c.execute("SELECT COUNT(num) FROM Tasks").fetchone()[0]
    message = [
        f'Output Path: {OUT_PATH}',
        f'Output Format: {FILE_PREFIX}[num].{FILE_SUFFIX}',
        f'{num_jobs} Jobs in the queue'
    ]
    return '\n'.join(message)


def add_job(link: str, num: str, conn: sqlite3.Connection) -> None:
    """
    usage of [add] command:
    ./ariaq.py add [link] [num]
    """

    # defensive programming
    try:
        int(str)
    except ValueError:
        error_msg = 'invalid number for num in [add] command, aborting'
        warning(error_msg)
        raise ValueError(error_msg)

    hyp_filename = f'{FILE_PREFIX}{num}.{FILE_SUFFIX}'
    hyp_full_filename = f'{OUT_PATH}{hyp_filename}'
    if os.path.isfile(hyp_full_filename):
        error_msg = f'file: {hyp_filename} already exists in {OUT_PATH}, aborting'
        warning(error_msg)
        raise ValueError(error_msg)

    duplicate_num = bool(conn.execute(
        "SELECT COUNT(num) from Tasks WHERE num=?", (num,)
    ).fetchone()[0])
    if duplicate_num:
        error_msg = f'Illegal repeated use of num: {num}, aborting'
        warning(error_msg)
        raise ValueError(error_msg)

    info(f'adding job with num: {num}')


def main():
    debug(f'argv is {sys.argv}')
    argv = sys.argv
    argc = len(argv)

    if argc < 2 or argv[1] == 'help':
        print(__doc__)
        sys.exit(0)

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    # check for first run
    if not os.path.isfile(FIRSTRUN_FILE):
        setup(c, conn)

    cmd = argv[1]
    if cmd in cmds['add']:
        if argc != 4:
            print(add_job.__doc__)
        else:
            add_job(argv[3], argv[4], conn)
    elif cmd in cmds['status']:
        print(get_status_message(conn))
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
