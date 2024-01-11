# The conftest.py file serves as a means of providing fixtures for an entire directory.
# Fixtures defined in a conftest.py can be used by any test in that package without needing to import them
# pytest will automatically discover them.

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models

# _test is added at the end of {settings.database_name} to make use of out testing database.
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)


#Handle logic for the database
@pytest.fixture() #The scope='module' can be set to avoid dropping the table with every test. Allowing the persistance of users for further testing.
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# The client fixture will give us an unauthenticated client
@pytest.fixture()
def client(session): #This fixture will depend on session
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db # Will override the dependency get_deb of our routers
    yield TestClient(app) # Return a new test client

@pytest.fixture
def test_user2(client):
    user_data = {"email": "2@gmail.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user(client):
    user_data = {'email': '1@gmail.com', 'password': '1'}
    res = client.post('/users/', json=user_data)

    assert res.status_code == 201
    new_user = res.json() # We call a dictionary
    new_user['password'] = user_data['password'] #we add a new key called password and we will get the password from the dictionary previously called.
    return new_user

# This fixture will give us an authenticated client.
@pytest.fixture
def token(test_user):
    return create_access_token({'user_id': test_user['id']})

# Add the specific header that we get from the token fixture to the client
@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f'Bearer {token}'
    }
    return client

# Since we work with the database we are going to use 'session' as an parameter
@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "4rd title",
        "content": "4rd content",
        "owner_id": test_user2['id']
    }]


    def create_post_model(post):
        # We convert a diccionary into a post model by expanding post with **
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)

    # Convert the map into a list
    posts = list(post_map)

    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts