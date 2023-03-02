import tkinter as tk
import mysql.connector
from tkinter import *
import getpass

# db_pw = getpass.getpass("Enter database password: ")
__HOST = '127.0.0.1'
__USERNAME = 'root'
__PASSWORD = "5crNoOdN1331"
__DATABASE = 'users'

con = mysql.connector.connect(host=__HOST,user=__USERNAME,password=__PASSWORD,database=__DATABASE)

mycursor = con.cursor()

sql = "INSERT INTO logon (username, password) VALUES (%s, %s)"
val = ("ajkds", "213")
mycursor.execute(sql, val)
con.commit()

print(mycursor.rowcount, "record inserted.")