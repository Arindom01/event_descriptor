import boto3
import pytest
from pathlib import Path
import sqlite3
from src.loadconfig import App_Conf
import os
import src.dbutil as d


def test_hello_world():
    res = d.dbutil()
    path=os.path.join(Path(__file__).parent.parent , App_Conf().config()['db_relative_path'] )
    dbfile = r"{path}".format(path=path)
    assert isinstance(res.create_connection(dbfile), type(sqlite3.connect(dbfile)))