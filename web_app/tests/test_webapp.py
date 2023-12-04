"""Module for Testing Python Functions"""
import pytest
import mongomock
from web_app import app

class Tests1:
    """Test Functions for the Web App"""

    @pytest.fixture
    def example_fixture(self):
        """An example of a pytest fixture for"""
        yield

    # Test functions
    def test_sanity_check(self):
        """Run a simple test for the webapp side that always passes."""
        actual = True
        expected = True
        assert actual == expected, "Expected True to be equal to True!"

    @pytest.fixture
    def mock(self):
        # Mock database
        with mongomock.patch(servers=(('server.example.com', 27017),)):
            yield app

    @pytest.fixture
    def client(self, mock):
        """Create a test client for the Flask application."""
        return mock.test_client()
    
    @pytest.fixture
    def runner(self, mock):
        """Create a test command-line runner for the Flask application."""
        return mock.test_cli_runner()
    
    def test_signup_page(self, client):
        """Test that the signup page renders correctly"""
        response = client.get('/signup')
        assert response.status_code == 200
        assert b'Sign Up' in response.data

    def test_signup_with_existing_username(self, client):
        """Test signup with an existing username"""
        # Assume 'existing_user' is already in the database
        new_user = {
            'username': 'existing_user',
            'password': 'Password123',
            'confirm_password': 'Password123',
            'email': 'exis_user@email.com'
        }
        response = client.post('/signup', data=new_user)
        assert response.status_code == 200  
        assert b'Username already exists!' in response.data

    def test_signup_successful(self, client):
        """Test successful signup"""
        new_user = {
            'username': 'newuser',
            'password': 'Password123',
            'confirm_password': 'Password123',
            'email': 'new_user@email.com'
        }
        response = client.post('/signup', data=new_user)
        assert response.status_code == 302
        assert b'/login' in response.headers['Location']

    def test_signup_password_too_short(self, client):
        """Test signup with a password that is too short"""
        data = {
            'username': 'user',
            'password': 'Zx25',
            'confirm_password': 'Zx25',
            'email': 'user@email.com'
        }
        response = client.post('/signup', data=data)
        assert response.status_code == 200
        assert b'Password must be between 8 and 20 characters long!' in response.data


    def test_signup_password_too_long(self, client):
        """Test signup with a password that is too long"""
        data = {
            'username': 'user',
            'password': 'PasswordPass12345678912345',  
            'confirm_password': 'PasswordPass12345678912345',
            'email': 'user@email.com'
        }
        response = client.post('/signup', data=data)
        assert response.status_code == 200
        assert b'Password must be between 8 and 20 characters long!' in response.data

    def test_signup_password_no_digit(self, client):
        """Test signup with a password that has no digits"""
        data = {
            'username': 'user',
            'password': 'PassyPass',
            'confirm_password': 'PassyPass',
            'email': 'user@email.com'
        }
        response = client.post('/signup', data=data)
        assert response.status_code == 200
        assert b'Password should have at least one number!' in response.data

    def test_signup_password_no_alphabet(self, client):
        """Test signup with a password that has no alphabets"""
        data = {
            'username': 'user',
            'password': '12345678',
            'confirm_password': '12345678',
            'email': 'user@email.com'
        }
        response = client.post('/signup', data=data)
        assert response.status_code == 200
        assert b'Password should have at least one alphabet!' in response.data

    def test_login_page_not_logged_in(self, client):
        """Test that the login page is rendered when not logged in"""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'login.html' in response.data

    def test_login_page_redirect_when_logged_in(self, client):
        """Test that user is redirected to the home page when logged in"""
        with client:
            with client.session_transaction() as sess:
                sess['user_id'] = 'some_user_id'

            response = client.get('/login')
            assert response.status_code == 302
            assert b'/index' in response.headers['Location']
