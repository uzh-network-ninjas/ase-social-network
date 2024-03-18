# Some example code to setup the test environment for FastAPI
# taken from 
# https://testdriven.io/blog/fastapi-crud/


import pytest
from fastapi.testclient import TestClient
from app.UserController import app  # Ensure this points to your FastAPI app instance

# TODO there is still some warning, if want to avoid use explicit verion of httpx (under February 2024)
@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client  # testing happens here





#  code from https://www.fastapitutorial.com/blog/unit-testing-in-fastapi/ - has also database

# from typing import Any
# from typing import Generator
    
# import pytest
# from fastapi import FastAPI
# from fastapi.testclient import TestClient
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
#this is to include backend dir in sys.path so that we can import from db,main.py

# from db.base import Base
# from db.session import get_db
# from apis.base import api_router


# def start_application():
#     app = FastAPI()
#     # app.include_router(api_router)
#     return app


# SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
# engine = create_engine(
    # SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# Use connect_args parameter only with sqlite
# SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# @pytest.fixture(scope="function")
# def app() -> Generator[FastAPI, Any, None]:
#     """
#     Create a fresh database on each test case.
#     """
#     # Base.metadata.create_all(engine)  # Create the tables.
#     _app = start_application()
#     yield _app
    # Base.metadata.drop_all(engine)


# @pytest.fixture(scope="function")
# def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
#     connection = engine.connect()
#     transaction = connection.begin()
#     session = SessionTesting(bind=connection)
#     yield session  # use the session in tests.
#     session.close()
#     transaction.rollback()
#     connection.close()


# @pytest.fixture(scope="function")
# def client(
#     app: FastAPI, db_session: SessionTesting
# ) -> Generator[TestClient, Any, None]:
#     """
#     Create a new FastAPI TestClient that uses the `db_session` fixture to override
#     the `get_db` dependency that is injected into routes.
#     """

#     def _get_test_db():
#         try:
#             yield db_session
#         finally:
#             pass

#     app.dependency_overrides[get_db] = _get_test_db
#     with TestClient(app) as client:
#         yield client
    
