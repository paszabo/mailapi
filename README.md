# iRedAdmin API

A programmer friendly interface for iRedAdmin (OSE version)

# Known Limitations

- Only supports MD5 passwords
- Only supports MySQL


# Getting Started

1. `$ virtualenv -p $(which python2.7) venv`
2. `$ source venv/bin/activate`
3. `(venv)$ python setup.py develop`

# Usage

Before you can start making API calls, you must initialize a connection to the database back end you wish to manage.

To do so simply call the `init_db` method with a SQLAlchemy database URL.  If you're unclear on how to create one, see: http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls

Example:

            import mailapi

            mailapi.domain.get_all_domains() # throws a RuntimeError

            mailapi.init_db('mysql://scott:tiger@192.168.0.1:3306/vmail') # Initialize the db connection

            mailapi.domain.get_all_domains() # works!

# Need Help?

I suggest you look at the test cases in ./tests as they illustrate how this package should be used and the expected outcomes.

# Running Unit Test Suite

Easy...

`(venv)$ TEST_DB_CONN_STR='mysql://scott:tiger@192.168.0.1:3306/vmail' python setup.py test`

# I Need Feature x, y, z

Lol, fork me bro
