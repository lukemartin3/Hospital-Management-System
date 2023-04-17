import unittest
import mysql.connector
from flask import Flask
from app import app

__HOST = 'localhost'
__USERNAME = 'root'
__PASSWORD = '871056'
__DATABASE = 'users'

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

        
class TestLogin(unittest.TestCase):
    @staticmethod
    def connect():
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='871056',
            database='users'
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
      

    def test_invalid_login(self):
        response = self.client.post('/login', data=dict(
            username='testuser',
            password='wrongpass'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
     

if __name__ == '__main__':
    unittest.main()
