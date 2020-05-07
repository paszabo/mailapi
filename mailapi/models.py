""" Data model definitions go in here.

Note: This setup is done using SQLAlchemy's reflection feature.

See: http://docs.sqlalchemy.org/en/rel_0_9/orm/extensions/declarative.html#using-reflection-with-declarative # noqa
See: http://docs.sqlalchemy.org/en/rel_0_9/orm/extensions/declarative.html#sqlalchemy.ext.declarative.DeferredReflection # noqa
"""
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection


# Declarative base class using deferred reflection
# See: http://docs.sqlalchemy.org/en/rel_0_9/orm/extensions/declarative.html#sqlalchemy.ext.declarative.DeferredReflection # noqa
Base = declarative_base(cls=DeferredReflection)


class Mailbox(Base):
    __tablename__ = 'mailbox'


class Domain(Base):
    __tablename__ = 'domain'


class Alias(Base):
    __tablename__ = 'alias'


class UsedQuota(Base):
    __tablename__ = 'used_quota'
