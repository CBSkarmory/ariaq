#!/usr/bin/python3
"""
usage: ./ariaq.py [command] [args]
commands:
    add [link] [num]
    status
    help
"""

import logging
import os.path
import sqlite3
import sys
from logging import debug, info, warning, error

from __init__ import *

cmds = {
    'add': {'add', 'a'},
    'status': {'status'},
    'help': {'--help', 'help'}
}

logging.basicConfig(filename=os.getenv("LOGFILE_NAME"), level=logging.INFO)


def get_status_message(conn: sqlite3.Connection) -> str:
    num_jobs: int = conn.execute("SELECT COUNT(num) FROM Tasks").fetchone()[0]
    message = [
        f'Output Path: {OUT_PATH}',
        f'Output Format: {FILE_PREFIX}[num].{FILE_SUFFIX}',
        f'{num_jobs} job(s) in the queue'
    ]
    return '\n'.join(message)


def add_job(link: str, num: str, conn: sqlite3.Connection) -> None:
    """
    usage of [add] command:
    ./ariaq.py add [link] [num]
    """

    # defensive programming
    try:
        int(num)
    except ValueError:
        error_msg = f'invalid arg: ({num}) for num in [add] command, aborting'
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
    try:
        conn.execute('''INSERT INTO Tasks
                        VALUES (?, ?)''', (link, num))
        conn.commit()
    except sqlite3.OperationalError as e:
        error(e.__traceback__)
        raise


def main():  # pragma: no cover
    debug(f'argv is {sys.argv}')
    argv = sys.argv
    argc = len(argv)

    if argc < 2 or argv[1] in cmds["help"]:
        print(__doc__)
        sys.exit(0)

    conn = sqlite3.connect(DB)

    # check for first run
    if not os.path.isfile(FIRSTRUN_FILE):
        setup(conn)

    cmd = argv[1]
    if cmd in cmds['add']:
        if argc != 4:
            print(add_job.__doc__)
        else:
            add_job(argv[3], argv[4], conn)
    elif cmd in cmds['status']:
        print(get_status_message(conn))
    else:
        print(f'Unrecognized command: {cmd}')
        print(__doc__)


def setup(conn: sqlite3.Connection) -> None:
    debug("First run detected, creating Tasks table in DB")
    conn.execute('''CREATE TABLE Tasks
                 (link text, num int)''')
    conn.commit()
    with open(FIRSTRUN_FILE, 'w') as firstrun:
        firstrun.write('first run')


if __name__ == '__main__':  # pragma: no cover
    main()
