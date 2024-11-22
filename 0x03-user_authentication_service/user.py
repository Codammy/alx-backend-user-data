#!/usr/bin/env python3
"""User module
"""

from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer, String, Column
Base = declarative_base()


class User(Base):
    """User model"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, max_length=250)
    hashed_password = Column(String, nullable=False, max_length=250)
    session_id = Column(String, max_length=250)
    reset_token = Column(String, max_length=250)
