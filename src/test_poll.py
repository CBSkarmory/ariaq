import sqlite3
import os.path

if os.path.isdir('src'):  # pragma: no cover
    os.chdir('src')
from __init__ import *
import ariaq


def setup_function(function):
    global DB
    DB = os.getenv("TEST_DB_NAME")
    if os.path.isfile(DB):  # pragma: no cover
        os.remove(DB)
    with sqlite3.connect(DB) as conn:
        conn.execute("CREATE TABLE Tasks (link text, num text)")
        conn.commit()


def teardown_function(function):
    with open(os.getenv("LOGFILE_NAME"), 'w') as log:
        log.write('[logfile cleared after test run]\n')


def test_poll_0():
    link = "https://example.com"
    with sqlite3.connect(DB) as conn:
        for job_num in range(15):
            ariaq.add_job(link, str(job_num).zfill(2), conn)
        order = sorted(map(lambda x: str(x).zfill(2), range(15)))
        for job_num in order:
            curr = ariaq.poll(conn)
            assert curr
            assert len(curr) == 2
            assert curr[0] == link
            assert curr[1] == str(job_num)


def test_poll_1():  # empty case
    with sqlite3.connect(DB) as conn:
        assert ariaq.poll(conn) is None
