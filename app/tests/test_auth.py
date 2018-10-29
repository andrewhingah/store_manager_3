'''Tests for users'''
# from .base_test import BaseTestCase
import os
import unittest
import json

from app.manage import migrate, reset_migrations

from app.app import create_app

class BaseTestCase(unittest.TestCase):
    """Parent tests class"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        migrate()
    
        self.client = self.app.test_client()

        self.users = {
        'name':'andrew hinga',
        'email': 'andrewhinga5@gmail.com',
        'username': 'andrew5',
        'password': '1234'
        }

        self.new_user = {
        'name': 'john terry',
        'email': 'john@gmail.com',
        'username':'john',
        'password': '1881'
        }

        self.user = {
        'email': 'henry@gmail.com',
        'username': 'henry',
        'password': 'password'
        }

        self.bad_user = {
        "password":"password"
        }


        self.header = {"Content-Type": "application/json"}

        self.s_url = 'api/v2/auth/signup' #signup url
        self.l_url = 'api/v2/auth/login' #login url
        self.p_url = 'api/v2/products' #products url



class UsersTestCase(BaseTestCase): 
    """This class represents Users tests."""

        
    def test_signup_user_with_existing_email(self):
        """Test to register user with existing email."""
        data = self.users
        res1 = self.client.post(self.s_url,
            data=json.dumps(data), headers=self.header)

        res2 = self.client.post(self.s_url,
            data=json.dumps(data), headers=self.header)

        result2 = json.loads(res2.data.decode())

        self.assertEqual(result2['message'], 'Email already exists.')
        self.assertEqual(res2.status_code, 202)

    def test_signup_new_user(self):
        """Test to register new user."""
        data = self.new_user
        response = self.client.post(self.s_url,
            data=json.dumps(data), headers=self.header)

        result = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['message'], 'User created!')


    def test_signin_user(self):
        """Test user sign in to their account."""
        data = self.new_user
        response = self.client.post(self.s_url,
            data=json.dumps(data), headers=self.header)


        self.assertEqual(response.status_code, 201)
        
        res = self.client.post(self.l_url,
            data=json.dumps(data), headers=self.header)

        result = json.loads(res.data.decode())

        self.assertEqual(result['message'], "Logged in successfully!")
        self.assertEqual(res.status_code, 201)


    def test_signin_non_registered_user(self):
        """Test signing in a non-registered user."""
        data = self.new_user
        response = self.client.post(self.l_url,
            data=json.dumps(data), headers=self.header)

        result = json.loads(response.data.decode())

        # assert that this response must contain an error message 
        # and an error status code 401(Unauthorized)
        self.assertEqual(result['message'],
            "Your account does not exist! Please register")

        self.assertEqual(response.status_code, 401)

    def tearDown(self):
        reset_migrations()


if __name__ == "__main__":
    unittest.main()