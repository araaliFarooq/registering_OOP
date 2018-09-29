from run import app
from app.modals.task import Task
from app import views
from flask import jsonify, json
import unittest

class Test_Task_Views(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client(self)

    def test_add_task(self):
        response = self.app.post("/api/users/register",
                                 content_type='application/json',
                                 data=json.dumps(dict(username="araali2", email="araali@email.com", password="Ar@4ali"),)
                                 )
        reply2 = json.loads(response.data.decode())                   
        response2 = self.app.post("/api/users/login",
                                 content_type='application/json',
                                 data=json.dumps(dict(username="araali2", email="araali@email.com", password="Ar@4ali"),)
                                 )
        reply = json.loads(response2.data.decode())                      
        response3 = self.app.post("/api/tasks/add",
                                content_type='application/json', headers=dict(Authorization='Bearer '+reply['access_token']),
                                data=json.dumps(dict(title="General cleaning"),)   
                            )
        reply2 = json.loads(response3.data.decode())
        self.assertIn(("General cleaning"),reply2.get("New task Created").values())                   
        self.assertEquals(response3.status_code, 201)

    def test_delete_a_task(self):
        response = self.app.post("/api/users/register",
                                 content_type='application/json',
                                 data=json.dumps(dict(username="araali2", email="araali@email.com", password="Ar@4ali"),)
                                 )
        reply2 = json.loads(response.data.decode())                   
        response2 = self.app.post("/api/users/login",
                                 content_type='application/json',
                                 data=json.dumps(dict(username="araali2", email="araali@email.com", password="Ar@4ali"),)
                                 )
        reply = json.loads(response2.data.decode())                  
        response3 = self.app.post("/api/tasks/add",
                                content_type='application/json', headers=dict(Authorization='Bearer '+reply['access_token']),
                                data=json.dumps(dict(title="General cleaning"),)   
                            )
        response3 = self.app.delete("/api/tasks/delete/1",content_type='application/json', headers=dict(Authorization="Bearer "+reply["access_token"]))
        reply2 = json.loads(response3.data.decode())
        self.assertEquals(reply2.get("message"), "Task successfully deleted")
        self.assertEquals(response3.status_code, 200)

    def test_delete_a_task_failure(self):
        response = self.app.post("/api/users/register",
                                 content_type='application/json',
                                 data=json.dumps(dict(username="araali2", email="araali@email.com", password="Ar@4ali"),)
                                 )
        reply2 = json.loads(response.data.decode())                   
        response2 = self.app.post("/api/users/login",
                                 content_type='application/json',
                                 data=json.dumps(dict(username="araali2", email="araali@email.com", password="Ar@4ali"),)
                                 )
        reply = json.loads(response2.data.decode())                  
        response3 = self.app.post("/api/tasks/add",
                                content_type='application/json', headers=dict(Authorization='Bearer '+reply['access_token']),
                                data=json.dumps(dict(title="General cleaning"),)   
                            )
        response3 = self.app.delete("/api/tasks/delete/3",content_type='application/json', headers=dict(Authorization="Bearer "+reply["access_token"]))
        reply2 = json.loads(response3.data.decode())
        self.assertEquals(reply2.get("message"), "Task not deleted or doesn't exist")
        self.assertEquals(response3.status_code, 400)
        
    def test_delete_user_tasks(self):
        response = self.app.post("/api/users/register",
                                 content_type='application/json',
                                 data=json.dumps(dict(username="araali2", email="araali@email.com", password="Ar@4ali"),)
                                 )
        reply2 = json.loads(response.data.decode())                   
        response2 = self.app.post("/api/users/login",
                                 content_type='application/json',
                                 data=json.dumps(dict(username="araali2", email="araali@email.com", password="Ar@4ali"),)
                                 )
        reply = json.loads(response2.data.decode())                  
        response3 = self.app.post("/api/tasks/add",
                                content_type='application/json', headers=dict(Authorization='Bearer '+reply['access_token']),
                                data=json.dumps(dict(title="General cleaning"),)   
                            )
        response3 = self.app.delete("/api/tasks/delete",content_type='application/json', headers=dict(Authorization="Bearer "+reply["access_token"]))
        reply2 = json.loads(response3.data.decode())
        self.assertEquals(reply2.get("message"), "Your tasks successfully deleted")
        self.assertEquals(response3.status_code, 200)

    def test_delete_user_tasks_failure(self):
        response = self.app.post("/api/users/register",
                                 content_type='application/json',
                                 data=json.dumps(dict(username="araali2", email="araali@email.com", password="Ar@4ali"),)
                                 )
        response1 = self.app.post("/api/users/register",
                                 content_type='application/json',
                                 data=json.dumps(dict(username="araali22", email="araali@email.com", password="Ar@4ali"),)
                                 )                                    
        login1 = self.app.post("/api/users/login",
                                 content_type='application/json',
                                 data=json.dumps(dict(username="araali2", email="araali@email.com", password="Ar@4ali"),)
                                 )
        login1_reply = json.loads(login1.data.decode())
        login2 = self.app.post("/api/users/login",
                                 content_type='application/json',
                                 data=json.dumps(dict(username="araali22", email="araali@email.com", password="Ar@4ali"),)
                                 )
        login2_reply = json.loads(login2.data.decode())                    
        response3 = self.app.post("/api/tasks/add",
                                content_type='application/json', headers=dict(Authorization='Bearer '+login1_reply['access_token']),
                                data=json.dumps(dict(title="General cleaning"),)   
                            )
        response3 = self.app.delete("/api/tasks/delete",content_type='application/json', headers=dict(Authorization="Bearer "+login2_reply["access_token"]))
        reply2 = json.loads(response3.data.decode())
        self.assertEquals(reply2.get("message"), "Tasks not deleted or list is empty")
        self.assertEquals(response3.status_code, 400)

    def test_finish_user_task(self):
        response = self.app.post("/api/users/register",
                                 content_type='application/json',
                                 data=json.dumps(dict(username="araali2", email="araali@email.com", password="Ar@4ali"),)
                                 )
        reply2 = json.loads(response.data.decode())                   
        response2 = self.app.post("/api/users/login",
                                 content_type='application/json',
                                 data=json.dumps(dict(username="araali2", email="araali@email.com", password="Ar@4ali"),)
                                 )
        reply = json.loads(response2.data.decode())                  
        response3 = self.app.post("/api/tasks/add",
                                content_type='application/json', headers=dict(Authorization='Bearer '+reply['access_token']),
                                data=json.dumps(dict(title="General cleaning"),)   
                            )
        response3 = self.app.put("/api/tasks/finish/2",content_type='application/json', headers=dict(Authorization="Bearer "+reply["access_token"]))
        reply2 = json.loads(response3.data.decode())
        self.assertEquals(reply2.get("message"), "Task successfully finished")
        self.assertEquals(response3.status_code, 200)

    def test_finish_user_task_failure(self):
        response = self.app.post("/api/users/register",
                                 content_type='application/json',
                                 data=json.dumps(dict(username="araali2", email="araali@email.com", password="Ar@4ali"),)
                                 )
        reply2 = json.loads(response.data.decode())                   
        response2 = self.app.post("/api/users/login",
                                 content_type='application/json',
                                 data=json.dumps(dict(username="araali2", email="araali@email.com", password="Ar@4ali"),)
                                 )
        reply = json.loads(response2.data.decode())                  
        response3 = self.app.post("/api/tasks/add",
                                content_type='application/json', headers=dict(Authorization='Bearer '+reply['access_token']),
                                data=json.dumps(dict(title="General cleaning"),)   
                            )
        response3 = self.app.put("/api/tasks/finish/6",content_type='application/json', headers=dict(Authorization="Bearer "+reply["access_token"]))
        reply2 = json.loads(response3.data.decode())
        self.assertEquals(reply2.get("message"), "Task not finished or doesn't exist")
        self.assertEquals(response3.status_code, 400)         

    