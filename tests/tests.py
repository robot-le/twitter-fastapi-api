from fastapi import status
from conftest import app


class TestAPI:

    async def test_registration(self, ac):
        res = await ac.post(
            app.url_path_for('register'),
            json={
                'username': 'test_username',
                'email': 'test@mail.com',
                'password': 'password',
                'password2': 'password',
            }
        )
        assert res.status_code == status.HTTP_201_CREATED

    async def test_login(self, ac, token):
        login_res = await ac.post(
            app.url_path_for('login'),
            data={
                'username': 'test_username',
                'password': 'password',
            }
        )
        data = login_res.json()
        assert data['status'] == 'success'

    # async def test_create_post(self, ac):
    #     pass
    #
    # async def test_get_post(self, ac):
    #     pass
    #
    # async def test_delete_post(self, ac):
    #     pass
    #
    # async def test_like_post(self, ac):
    #     pass
    #
    # async def test_unlike_post(self, ac):
    #     pass
    #
    # async def test_get_current_user(self, ac):
    #     pass
    #
    # async def test_update_current_user(self, ac):
    #     pass
    #
    # async def test_delete_current_user(self, ac):
    #     pass
    #
    # async def test_get_user(self, ac):
    #     pass
    #
    # async def test_get_user_followers(self, ac):
    #     pass
    #
    # async def test_get_user_following(self, ac):
    #     pass
    #
    # async def test_follow_user(self, ac):
    #     pass
    #
    # async def test_unfollow_user(self, ac):
    #     pass
    #
    # async def test_get_user_posts(self, ac):
    #     pass
    #
    # async def test_get_user_likes(self, ac):
    #     pass
    #
    # async def test_feed(self, ac):
    #     pass
    #
    # async def test_explore(self, ac):
    #     pass
    #
    # async def test_search(self, ac):
    #     pass
