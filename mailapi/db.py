""" Module containing database operations

See: http://docs.sqlalchemy.org/en/rel_0_9/orm/extensions/declarative.html#using-reflection-with-declarative # noqa
See: http://docs.sqlalchemy.org/en/rel_0_9/orm/extensions/declarative.html#sqlalchemy.ext.declarative.DeferredReflection # noqa
"""
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import DeferredReflection

from .models import Base


# Don't use the DBSession directly since it may not be initialized, use the
# factory method instead.
_DBSession = Session()


def init_db(conn_str):
    """ Initialize a connection to the database

    :param conn_str: SQLAlchemy database URL
    :return:
    """

    engine = create_engine(conn_str)
    _DBSession.bind = engine
    Base.metadata.bind = engine

    # we can reflect it ourselves from a database, using options
    # such as 'only' to limit what tables we look at...
    metadata = MetaData()
    metadata.reflect(engine, only=['domain', 'mailbox', 'alias'])

    # calling prepare() just sets up mapped classes and relationships.
    DeferredReflection.prepare(engine)
    Base.prepare(engine)


def get_db_session():
    """ Get the database session object as long as it's bound to an engine

    :return: SQLAlchemy ORM Session object
    :raises: RuntimeError if the session is not bound to an engine
    """
    if not _DBSession.bind:
        raise RuntimeError('You must initialize the database connection before'
                           ' attempting to use it.')
    else:
        return _DBSession
