import pytest
from app import models


@pytest.fixture()
# Test if an user can vote on a post.
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()

# Test if an user can vote on their own post. In this scenario you can.
def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post(
        "/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 201

# Test if an user voted a post twice.
def test_vote_twice_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 409

# Test if an user can delete their vote on a post.
def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 201

# Test if an user can delete a vote if they didn't vote before.
def test_delete_vote_non_exist(authorized_client, test_posts):
    res = authorized_client.post(
        "/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 404

# Test if an user can vote on a non-existent post.
def test_vote_post_non_exist(authorized_client, test_posts):
    res = authorized_client.post(
        "/vote/", json={"post_id": 80000, "dir": 1})
    assert res.status_code == 404

# Test if an user who is not authenticated can vote.
def test_vote_unauthorized_user(client, test_posts):
    res = client.post(
        "/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 401