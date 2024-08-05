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

    async def test_login(self, ac):
        login_res = await ac.post(
            app.url_path_for('login'),
            data={
                'username': 'test_username',
                'password': 'password',
            }
        )
        data = login_res.json()
        assert data['status'] == 'success'

    async def test_follow_user(self, ac, access_data):
        res = await ac.post(
            app.url_path_for('follow', user_id=access_data[1].get('user_id')),
            headers={
                'Authorization': f'Bearer {access_data[0].get("user_token")}'
            }
        )
        assert res.json().get('status') == 'success'

    async def test_unfollow_user(self, ac, access_data):
        url = app.url_path_for('unfollow', user_id=access_data[1].get('user_id'))
        res = await ac.post(
            url,
            headers={
                'Authorization': f'Bearer {access_data[0].get("user_token")}'
            }
        )
        assert res.json().get('status') == 'success'
