from run import app
from app.modals.account import User
from app import views
from flask import jsonify, json
import unittest

class Test_Auth(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client(self)

    def test_registration(self):
        response = self.app.post("/api/users/register",
                                 content_type='application/json',
                                 data=json.dumps(dict(username="araali", email="araali@email.com", password="Ar$4ali"),)
                                 )
        reply = json.loads(response.data.decode())
        self.assertIn(("araali"),reply.get("New User Created").values())
        self.assertEquals(response.status_code, 201)

    def test_username_exists_registration(self):
        response = self.app.post("/api/users/register",
                                 content_type='application/json',
                                 data=json.dumps(dict(username="araali", email="araali@email.com", password="Ar$4ali"),)
                                 )
        self.assertEquals(response.status_code, 400) 

    def test_wrong_password_registration(self):
        response = self.app.post("/api/users/register",
                                 content_type='application/json',
                                 data=json.dumps(dict(username="araali", email="araali@email.com", password="Ara4ali"),)
                                 )
        self.assertEquals(response.status_code, 400)

    def test_wrong_email_registration(self):
        response = self.app.post("/api/users/register",
                                 content_type='application/json',
                                 data=json.dumps(dict(username="araali", email="araaliemail.com", password="Ar@4ali"),)
                                 )
        self.assertEquals(response.status_code, 400) 

    def test_user_login(self):
        response = self.app.post("/api/users/register",
                                 content_type='application/json',
                                 data=json.dumps(dict(username="araali", email="araaliemail.com", password="Ar@4ali"),)
                                 )
        response2 = self.app.post("/api/users/login",
                                 content_type='application/json',
                                 data=json.dumps(dict(username="araali", email="araali@email.com", password="Ar$4ali"),)
                                 )
        self.assertEquals(response2.status_code, 200)

    def test_user_doesnt_exist_login(self):
        response = self.app.post("/api/users/register",
                                 content_type='application/json',
                                 data=json.dumps(dict(username="araali", email="araaliemail.com", password="Ar@4ali"),)
                                 )
        response2 = self.app.post("/api/users/login",
                                 content_type='application/json',
                                 data=json.dumps(dict(username="araali22", email="araali@email.com", password="Ar$4ali"),)
                                 )
        self.assertEquals(response2.status_code, 404)

    def test_login_failure(self):
        response = self.app.post("/api/users/register",
                                 content_type='application/json',
                                 data=json.dumps(dict(username="araali", email="araaliemail.com", password="Ar@4ali"),)
                                 )
        response2 = self.app.post("/api/users/login",
                                 content_type='application/json',
                                 data=json.dumps(dict( email="araali@email.com", password="Ar$4ali"),)
                                 )
        self.assertEquals(response2.status_code, 400)

    def test_delete_account(self):
        response = self.app.post("/api/users/register",
                                 content_type='application/json',
                                 data=json.dumps(dict(username="araali", email="araali@email.com", password="Ar@4ali"),)
                                 )
        response2 = self.app.post("/api/users/login",
                                 content_type='application/json',
                                 data=json.dumps(dict(username="araali", email="araali@email.com", password="Ar@4ali"),)
                                 )
        reply = json.loads(response2.data.decode())                         
        response3 = self.app.delete("/api/users/delete_account",content_type='application/json', headers=dict(Authorization="Bearer "+reply["access_token"]))
        self.assertEquals(response3.status_code, 200)

    def test_logout(self):
        response = self.app.post("/api/users/register",
                                 content_type='application/json',
                                 data=json.dumps(dict(username="araali3", email="araali@email.com", password="Ar@4ali"),)
                                 )
        response2 = self.app.post("/api/users/login",
                                 content_type='application/json',
                                 data=json.dumps(dict(username="araali3", email="araali@email.com", password="Ar@4ali"),)
                                 )
        reply = json.loads(response2.data.decode())                         
        response3 = self.app.delete("/api/users/logout",content_type='application/json', headers=dict(Authorization="Bearer "+reply["access_token"]))
        reply2 = json.loads(response3.data.decode())
        self.assertEquals(reply2.get("message"), "Successfully logged out")
        self.assertEquals(response3.status_code, 200)
