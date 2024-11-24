#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self):
        "Initializes a new DB instance"
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine, expire_on_commit=False)
            self.__session = DBSession
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """creates a new user"""
        user = User(email=email, hashed_password=hashed_password)
        session = self._session()
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Takes in arbituary keyword argument
           and returns the first row found in the users table
        """
        session = self._session()
        user = session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound
        return user
