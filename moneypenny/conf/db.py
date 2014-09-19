# -*- coding: UTF-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

from moneypenny.conf import settings

engine = create_engine(settings['database']['url'], echo=True)

Session = sessionmaker(bind=engine)
Base = declarative_base()
