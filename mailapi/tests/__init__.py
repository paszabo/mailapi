from os import environ

from ..db import init_db


# Grabs the DB connection string from an environment variable
conn_str = environ.get('TEST_DB_CONN_STR', '')


if not conn_str:
    raise RuntimeError('''

    Woah Nelly!!

    You must provide a SQLAlchemy connection string though the environment
    variable `TEST_DB_CONN_STR` in order to run this test suite.

    Example: (venv)$ TEST_DB_CONN_STR='mysql://scott:tiger@192.168.0.1:3306/\
vmail' python setup.py test

    See: http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls
''')
else:
    init_db(conn_str)
