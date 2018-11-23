#!/usr/bin/env python
"""
usage: ./ariaq.py [command] [args]
commands:
    add [link] [num]
    status
    help
"""

import logging as lg
import os.path
import sqlite3
import subprocess
import sys
from typing import Tuple, Union

from constants import *

cmds = {
    'add': {'add', 'a'},
    'status': {'status'},
    'start': {'start'},
    'help': {'--help', 'help'}
}

lg.basicConfig(filename=os.getenv("LOGFILE_NAME"), level=lg.INFO)
lg.getLogger().addHandler(lg.StreamHandler())


def _get_num_jobs(conn: sqlite3.Connection) -> int:
    num_jobs: int = conn.execute("SELECT COUNT(num) FROM Tasks").fetchone()[0]
    return num_jobs


def _get_highest_priority(conn: sqlite3.Connection) -> str:
    min_key = conn.execute("SELECT  min(num) FROM Tasks").fetchone()[0]
    if not min_key:
        return ""
    else:
        return min_key


def start_working(db_name) -> list:
    failed_jobs = []
    lg.info("Starting a worker")
    # go until queue is empty
    while True:
        with sqlite3.connect(db_name) as conn:
            curr_job = poll(conn)
        if not curr_job:
            break
        link, num = curr_job
        filename = f'{FILE_PREFIX}{num}.{FILE_SUFFIX}'
        full_filename = f'{OUT_PATH}{filename}'
        lg.info(f'Starting download job num {num}')
        p = subprocess.run([
            'aria2c',
            '-x 16',
            '-s 6',
            str(link),
            '-o',
            str(full_filename)
        ], stdout=subprocess.DEVNULL)  # suppress output
        if p.returncode:
            lg.warning(f'Attempt to download num {num} failed, skipping')
            failed_jobs.append((link, num))
        else:
            lg.info(f'Download of num: {num} completed')
    lg.info("Queue is empty, stopping")
    if len(failed_jobs) > 0:
        lg.info(f'failed jobs: {failed_jobs}')
    return failed_jobs


def poll(conn: sqlite3.Connection) -> Union[Tuple[str, str], type(None)]:
    min_key = _get_highest_priority(conn)
    if not min_key:
        return None
    else:
        ret: Tuple[str, str] = conn.execute("SELECT * FROM Tasks WHERE num=?", (min_key,)).fetchone()
        conn.execute("DELETE FROM Tasks WHERE num=?", (min_key,))
        conn.commit()
        return ret


def get_status_message(conn: sqlite3.Connection) -> str:
    num_jobs: int = _get_num_jobs(conn)
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
        lg.warning(error_msg)
        raise ValueError(error_msg)

    hyp_filename = f'{FILE_PREFIX}{num}.{FILE_SUFFIX}'
    hyp_full_filename = f'{OUT_PATH}{hyp_filename}'
    if os.path.isfile(hyp_full_filename):
        error_msg = f'file: {hyp_filename} already exists in {OUT_PATH}, aborting'
        lg.warning(error_msg)
        raise ValueError(error_msg)

    duplicate_num = bool(conn.execute(
        "SELECT COUNT(num) from Tasks WHERE num=?", (num,)
    ).fetchone()[0])
    if duplicate_num:
        error_msg = f'Illegal repeated use of num: {num}, aborting'
        lg.warning(error_msg)
        raise ValueError(error_msg)

    lg.info(f'adding job with num: {num}')
    try:
        conn.execute('''INSERT INTO Tasks
                        VALUES (?, ?)''', (link, num))
        conn.commit()
    except sqlite3.OperationalError as e:
        lg.error(e.__traceback__)
        raise


def main():  # pragma: no cover
    lg.debug(f'argv is {sys.argv}')
    argv = sys.argv
    argc = len(argv)

    if argc < 2 or argv[1] in cmds["help"]:
        print(__doc__)
        sys.exit(0)

    # check for first run
    if not os.path.isfile(FIRSTRUN_FILE):
        setup()

    cmd: str = argv[1]

    if cmd in cmds['add']:
        if argc != 4:
            print(add_job.__doc__)
        else:
            with sqlite3.connect(DB) as conn:
                add_job(argv[2], argv[3], conn)

    elif cmd in cmds['status']:
        with sqlite3.connect(DB) as conn:
            print(get_status_message(conn))

    elif cmd in cmds['start']:
        start_working(DB)

    else:
        print(f'Unrecognized command: {cmd}')
        print(__doc__)


def setup() -> None:
    with sqlite3.connect(DB) as conn:
        lg.debug("First run detected, creating Tasks table in DB")
        conn.execute('''CREATE TABLE Tasks
                        (link text, num text)''')
        with open(FIRSTRUN_FILE, 'w') as firstrun:
            firstrun.write('first run')
        conn.commit()


if __name__ == '__main__':  # pragma: no cover
    main()
