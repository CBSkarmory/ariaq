# ariaq
[![Build Status](https://travis-ci.org/CBSkarmory/ariaq.png)](https://travis-ci.org/CBSkarmory/ariaq)
[![codecov](https://codecov.io/gh/CBSkarmory/ariaq/branch/master/graph/badge.svg)](https://codecov.io/gh/CBSkarmory/ariaq)


Dependencies
------------

#### Core
- Python 3.6.5+
- python-dotenv
#### Tests
- pytest-cov
- codecov

To install python dependencies,
```
pip3 install python-dotenv pytest-cov codecov
``` 

Make sure sqlite3 module is installed 
(should be built in to python) with
`echo "import sqlite3" | python3`
and making sure no errors occur.


Usage
-----

#### Core

Use `./ariaq --help` for more information (from `src/`)
Adding a job
```
./ariaq.py add [link] [num]
```



#### Tests

Run tests with `python3 -m pytest`.

Run tests and see code coverage with 
`python3 -m pytest --cov=./` 
from project root.