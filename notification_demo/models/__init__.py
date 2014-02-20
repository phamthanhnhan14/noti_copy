__author__ = 'mariozx'

from sqlalchemy import (
    engine_from_config,
    Column,
    Index,
    types,
    desc,
    ForeignKey,
    )
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    relation,
    backref,
    )
from sqlalchemy.util import ThreadLocalRegistry
from zope.sqlalchemy import ZopeTransactionExtension

class my_scoped_session(scoped_session):
    def attach_session_factory(self, factory):
        self.session_factory = factory
        self.registry = ThreadLocalRegistry(self.session_factory)

DBSession = my_scoped_session(None)
Base = declarative_base()
engine = None

def _initialize_database(settings):
    global engine
    global DBSession
    global Base

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

def initialize_web_database(settings):
    global DBSession
    DBSession.attach_session_factory(sessionmaker(extension=ZopeTransactionExtension()))
    _initialize_database(settings)

def initialize_non_web_database(settings, autocommit=True):
    global DBSession
    DBSession.attach_session_factory(sessionmaker(autoflush=True, autocommit=autocommit))
    _initialize_database(settings)

import user
from user import User