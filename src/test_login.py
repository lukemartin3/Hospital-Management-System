import unittest
import mysql.connector
from flask import Flask
from app import app

_TestLogout__HOST = 'localhost'
#_TestLogout__USERNAME  = 'Topher1028'
#_TestLogout__PASSWORD = 'fsedb'
_TestLogout__USERNAME = 'root'
_TestLogout__PASSWORD = '871056'
_TestLogout__DATABASE = 'fsedb'

#def connect():
#        try:
#            conn = mysql.connector.connect(
#                host=__HOST,
#                user=__USERNAME,
#                password=__PASSWORD,
#                database=__DATABASE
#            )
#            print("Connected to database successfully!")
#            return conn
#        except mysql.connector.Error as error:
#            print("Failed to connect to database: {}".format(error))
#            return None

#test User
TEST_USERNAME = 'testuser' 
TEST_PASSWORD = 'testpass'
TEST_EMAIL = 'testuser@gmail.com'
TEST_UNIQUE_PIN = '1234'
TEST_DOCTOR = 0
TEST_NURSE= 0
        
class TestLogin(unittest.TestCase):
    @staticmethod
    def connect():
        return mysql.connector.connect(
            host=_TestLogout__HOST,
            user=_TestLogout__USERNAME,
            password=_TestLogout__PASSWORD,
            database=_TestLogout__DATABASE
        )

#setUp sets up the TestCase object by first connecting to the DB, then inserts a testUser. 
#Then using that testUser, it will run all test_functions()
#After all test_functions() are ran, it will remove testUser from the DB, and closing itself using tearDown()   


    def setUp(self):
        self.conn = self.connect()
        self.cursor = self.conn.cursor()
        self.cursor.execute('INSERT INTO users (username, email, password, pin, doctor, nurse) VALUES (%s, %s, %s, %s, %s, %s)',
                                  (TEST_USERNAME, TEST_EMAIL, TEST_PASSWORD, TEST_UNIQUE_PIN, TEST_DOCTOR, TEST_NURSE))
        self.conn.commit()
        self.client = app.test_client()

    def tearDown(self):
        self.cursor.execute('DELETE FROM users WHERE username = %s', (TEST_USERNAME,))
        self.conn.commit()
        self.conn.close()


#   Send a post request to /login with our testuser, and checking for proper 200 code while also looking for
#   a 'You are registered' text within the response data
#   Same is done for invalid, by prompting it wrong pw, we look for successful 200 code to indicate server functionality, while looking for
#   'Incorrect' error message from the HTML payload
    def test_valid_login(self):
        response = self.client.post('/login', data=dict(
            username='testuser',
            password='testpass'
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You are registered', response.data)
      

    def test_invalid_login(self):
        response = self.client.post('/login', data=dict(
            username='testuser',
            password='wrongpass'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Incorrect username or password', response.data)
     

if __name__ == '__main__':
    unittest.main()
