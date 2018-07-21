import sqlite3

import pytest

import ariaq
from __init__ import *


def setup_function(function):
    global DB
    DB = "ariaq_test.sqlite"
    with sqlite3.connect(DB) as conn:
        try:
            conn.execute("DROP TABLE Tasks")
        except sqlite3.OperationalError:
            pass  # already DNE
        conn.execute("CREATE TABLE Tasks (link text, num text)")
        conn.commit()


def test_add_0():  # expected input
    with sqlite3.connect(DB) as conn:
        link, num = "http://example.com", "05"
        assert 0 == conn.execute('''SELECT COUNT(num) FROM Tasks
                                    WHERE link=? AND num=?''', (link, num)).fetchone()[0]
        ariaq.add_job(link, num, conn)
        assert 1 == conn.execute('''SELECT COUNT(num) FROM Tasks
                                    WHERE link=? AND num=?''', (link, num)).fetchone()[0]


def test_add_1():  # not a number
    with sqlite3.connect(DB) as conn:
        with pytest.raises(ValueError):
            link, num = "http://example.com", "not_a_number"
            ariaq.add_job(link, num, conn)


def test_add_2():  # file already exists
    with sqlite3.connect(DB) as conn:
        link, num = "http://example.com", "05"
        filename = f'{FILE_PREFIX}{num}.{FILE_SUFFIX}'
        full_filename = f'{OUT_PATH}{filename}'
        with open(full_filename, 'w') as f:
            f.write('blah blah')
        with pytest.raises(ValueError):
            ariaq.add_job(link, num, conn)
        os.remove(full_filename)


def test_add_3():  # entry in db with matching num
    with sqlite3.connect(DB) as conn:
        link, num = "http://example.com", "05"
        ariaq.add_job(link, num, conn)
        with pytest.raises(ValueError):
            ariaq.add_job(link, num, conn)
