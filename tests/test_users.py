import pytest
from app import schemas
from jose import jwt
from app.config import settings


# def test_root(client):
#     res = client.get('/')
#     print (res.json().get('message'))
#     assert res.json().get('message') == 'Hello world'
#     assert res.status_code == 200


def test_create_user(client):
    res = client.post('/users/', json={'email': 'hello123@gmail.com', 'password': 'password123'})
    
    new_user = schemas.UserOut(**res.json()) #This will validate that the new user has the fields required by the schema
    assert new_user.email == 'hello123@gmail.com'
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post('/login', data={'username': test_user['email'], 'password': test_user['password']}) #Sends body as 'data' and not 'json'
    login_res = schemas.Token(**res.json())
    
    #Implement logic to validate that the access token is valid.
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    
    #Check if the id corresponds to the user.
    assert id == test_user['id']

    assert login_res.token_type == 'bearer'
    assert res.status_code == 200


@pytest.mark.parametrize('email, password, status_code', [
    ("timbernerslee@noprovider.xyz", "681955", 403),
    ("bobkahn@noprovider.xyz", "insecure123", 403),
    ("guidovanrossum@noprovider.xyz", "changeme!", 403),
    ("vintcerf@noprovider.xyz", "password123", 403),
    (None, "password123", 422),
    ("vintcerf@noprovider.xyz", None, 422),


])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post('/login', data={'username': email, 'password': password})

    assert res.status_code == status_code
    #assert res.json().get('detail') == 'Invalid Credentials'