import unittest
import mysql.connector
from flask import Flask, session
from app import app

_TestLogout__HOST = 'localhost'
#_TestLogout__USERNAME  = 'Topher1028'
#_TestLogout__PASSWORD = 'fsedb'
_TestLogout__USERNAME = 'root'
_TestLogout__PASSWORD = 'Topher1028'
_TestLogout__DATABASE = 'fsedb'

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
        self.cursor.execute('CREATE TABLE IF NOT EXISTS usersTest (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))')
        self.conn.commit()
        self.cursor.execute('INSERT INTO usersTest (username, password) VALUES (%s, %s)', ('testuser', 'testpass'))
        self.conn.commit()
        self.client = app.test_client()

    def tearDown(self):
        self.cursor.execute('DROP TABLE usersTest')
        self.conn.close()
        
    def test_valid_login(self):
        response = self.client.post('/login', data=dict(
            username='testuser',
            password='testpass'
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['username'] = 'testuser'

            response = self.client.get('/logout', follow_redirects=True)

            self.assertNotIn(b'testuser', session.values())
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
