import unittest
import mysql.connector
from flask import Flask, session
from flask_session import Session
from app import app

_TestLogout__HOST = 'localhost'
#_TestLogout__USERNAME  = 'Topher1028'
#_TestLogout__PASSWORD = 'fsedb'
_TestLogout__USERNAME = 'root'
_TestLogout__PASSWORD = '871056'
_TestLogout__DATABASE = 'fsedb'

TEST_USERNAME = 'testuser' 
TEST_PASSWORD = 'testpass'
TEST_EMAIL = 'testuser@gmail.com'
TEST_UNIQUE_PIN = '1234'
TEST_DOCTOR = 0
TEST_NURSE= 0

class TestLogout(unittest.TestCase):
    @staticmethod

    def connect():
        return mysql.connector.connect(
            host=_TestLogout__HOST,
            user=_TestLogout__USERNAME,
            password=_TestLogout__PASSWORD,
            database=_TestLogout__DATABASE
        )

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

#   Log in using testUser, and checking HTML payload for correct messages. I couldn't get sessions to properly work so to ensure 
#   a user was logged out, it checks for "You are not registered" string after logging out, which is received if properly logged out.        
    def test_logout(self):
        response = self.client.post('/login', data=dict(
            username=TEST_USERNAME,
            password=TEST_PASSWORD
            
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You are registered', response.data)
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You are not registered', response.data)



if __name__ == '__main__':
    unittest.main()
