# ariaq
[![Build Status](https://travis-ci.org/CBSkarmory/ariaq.png)](https://travis-ci.org/CBSkarmory/ariaq)
[![codecov](https://codecov.io/gh/CBSkarmory/ariaq/branch/master/graph/badge.svg)](https://codecov.io/gh/CBSkarmory/ariaq)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

Dependencies
------------

#### Core
- [Python 3.6.5+](https://www.python.org/downloads/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [aria2](https://github.com/aria2/aria2)
#### Tests
- [pytest-cov](https://pypi.org/project/pytest-cov/)
- [codecov](https://pypi.org/project/codecov/)

To install python dependencies,
``` bash
pip3 install -r requirements.txt
```

or 

``` bash
pip3 install python-dotenv pytest-cov codecov
``` 

To get aria2,
``` bash
sudo apt install aira2
```

Usage
-----
#### Setup
Create a `.env` file modeled after `.env.example`

#### Core

Use `./ariaq --help` for more information (from `src/`)
Adding a job
```
./ariaq.py add [link] [num]
```
Starting a worker
```
./ariaq.py start
```


#### Tests

Run tests with `python3 -m pytest`.

Run tests and see code coverage with 
`python3 -m pytest --cov=./` 
from project root.
