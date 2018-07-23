import sqlite3
import re
import os.path

if os.path.isdir('src'):  # pragma: no cover
    os.chdir('src')
from __init__ import *
import ariaq


def extract_num_jobs(status: str) -> int:
    match = extract_num_jobs.rxp.match(status)
    if match:
        return int(match.group(1))


extract_num_jobs.rxp = re.compile('.*[^\d](\d+) job\(s\) in', re.DOTALL)


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


def test_status_0():
    actual_jobs = 0
    link = "https://example.com"
    with sqlite3.connect(DB) as conn:
        status = ariaq.get_status_message(conn)
        assert actual_jobs == extract_num_jobs(status)
        for _ in range(15):
            actual_jobs += 1
            ariaq.add_job(link, str(actual_jobs), conn)
            status = ariaq.get_status_message(conn)
            assert actual_jobs == extract_num_jobs(status)
