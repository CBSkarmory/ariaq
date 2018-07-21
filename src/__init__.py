from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

OUT_PATH = os.getenv("OUT_PATH")
if OUT_PATH[-1] != '/':
    OUT_PATH += '/'

FILE_PREFIX = os.getenv("FILE_PREFIX")
FILE_SUFFIX = os.getenv("FILE_SUFFIX")

FIRSTRUN_FILE = '.firstrun'
DB = 'ariaq.sqlite'
