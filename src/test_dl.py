import sqlite3
import os
import subprocess
import hashlib

if os.path.isdir('src'):  # pragma: no cover
    os.chdir('src')
from constants import *
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


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def test_dl_0():
    link = "http://example.com"
    subprocess.run(['wget', '-q', link, '-O', 'foo'], stdout=subprocess.DEVNULL)
    correct_hash = md5('foo')
    os.remove('foo')
    with sqlite3.connect(DB) as conn:
        for job_num in range(3):
            ariaq.add_job(link, str(job_num), conn)
    fails = ariaq.start_working(DB)
    assert len(fails) == 0
    for job_num in range(3):
        filename = f'{FILE_PREFIX}{str(job_num)}.{FILE_SUFFIX}'
        full_filename = f'{OUT_PATH}{filename}'
        assert correct_hash == md5(full_filename)
        os.remove(full_filename)


def test_dl_1():  # bad protocol
    bad_link, num = "httpnotrealprotocol://example.com", '01'
    with sqlite3.connect(DB) as conn:
        ariaq.add_job(bad_link, num, conn)
    fails = ariaq.start_working(DB)
    assert len(fails) == 1
    assert (bad_link, num) == fails[0]
