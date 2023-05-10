import unittest
import flask
# from flask_mysqldb import MySQL
import mysql.connector
from flask_testing import TestCase

import sys
sys.path.append('../')
from src.db_functions import *

users_setup = """
DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `username` varchar(45) NOT NULL,
  `password` varchar(255) NOT NULL,
  `pin` varchar(4) NOT NULL,
  `fname` varchar(45) NOT NULL,
  `lname` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `dob` date NOT NULL,
  `phone` varchar(12) NOT NULL,
  `address` varchar(45) NOT NULL,
  `city` varchar(45) NOT NULL,
  `states` varchar(45) NOT NULL,
  `zip` varchar(5) NOT NULL,
  `insurance` varchar(45) NOT NULL,
  `history` varchar(255) NOT NULL,
  `billing` decimal(10,2) DEFAULT '0.00',
  `roles` tinyint(1) DEFAULT '1',
  `specialization` varchar(45) DEFAULT NULL,
  `prescription` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`username`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        with open("credentials.txt") as f:
            lines = [w.strip() for w in f.readlines()]
            host = lines[0]
            username = lines[1]
            password = lines[2]
            dbname = lines[3]
            
            self.app = flask.Flask(__name__)
            self.app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{username}:{password}@localhost/{dbname}'
            self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

            self.con = mysql.connector.connect(host=host, user=username, password=password, database=dbname)
            self.cursor = self.con.cursor(buffered=True)
            self.con.cursor().execute(users_setup)
            self.con.commit()

    def tearDown(self):
        pass

    def test_function(self):
        return True

class BasicTest(BaseTestCase):
    def test_function(self):
        # Set up a test user and password for the database
        user = 'testuser'
        password = 'testpassword'

        # Create a test table in the database
        self.cursor.execute('CREATE TABLE IF NOT EXISTS test_table (id INT)')
        self.cursor.execute('INSERT INTO test_table (id) VALUES (5)')
        self.con.commit()

        # Test a function that inserts data into the table
        # my_function(user, password)
        self.assertTrue(self.con.cursor() is not None)
        self.assertTrue(self.con.cursor().execute('SELECT * FROM test_table') is not None)
        self.assertTrue(self.con.cursor().execute('SELECT * FROM test_table').fetchOne() is not None)

        # Test a function that selects data from the table
        # result = my_function(user, password)
        # self.assertEqual(result, 'foo')



class RegisterCorrect(BaseTestCase):
    def test_function(self):
        usr_data = {"username": "test", "email": "test@test", "password": "123", "confirm_pass": "123",\
                "unique_pin": "1234", "first_name": "dill", "last_name": "pickle", "dob": "01/01/2001",\
                "phone": "666-777-8888", "address": "Anywhere", "city": "chicago", "state": "NO",\
                "zip": "12345", "insurance": "Pillson Medical", "med_history": "Extensive"}
        do_register(self.con.cursor(), usr_data)
        self.con.commit()

        self.assertTrue(self.con.cursor().execute('SELECT * FROM users') is not None)

class RegisterNonMatchingPassword(BaseTestCase):
    def test_function(self):
        usr_data = {"username": "test", "email": "test@test", "password": "123", "confirm_pass": "000",\
                "unique_pin": "1234", "first_name": "dill", "last_name": "pickle", "dob": "01/01/2001",\
                "phone": "666-777-8888", "address": "Anywhere", "city": "chicago", "state": "NO",\
                "zip": "12345", "insurance": "Pillson Medical", "med_history": "Extensive"}
        do_register(self.con.cursor(), usr_data)
        self.con.commit()

        self.assertTrue(self.con.cursor().execute('SELECT * FROM users') is None)

if __name__ == '__main__':
    unittest.main()

