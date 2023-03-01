import tkinter as tk
import mysql.connector
from tkinter import *
import getpass

db_pw = getpass.getpass("Enter database password: ")
__HOST = '127.0.0.1'
__USERNAME = 'root'
__PASSWORD = db_pw
__DATABASE = 'users'

con = mysql.connector.connect(host=__HOST,user=__USERNAME,password=__PASSWORD,database=__DATABASE)

def connect_database(username,password):
    #append password and username in the empty list below for later checkings
    mypassword_queue =[]
    sql_query = "SELECT * FROM logon WHERE username ='%s' AND password ='%s'" % (username, password)
    mycursor = con.cursor()

    try:
        mycursor.execute(sql_query)
        myresults =mycursor.fetchall()
        for row in myresults:
            for x in row:
                mypassword_queue.append(x)
    except:
        print('error occured')

    if (username and password) in mypassword_queue:
        print('Login Successful.')
        root.destroy()
        logged_in()

    else:
        print('ERROR: Username or Password is incorrect.')
        incrow = tk.Label(root, text="Username or Password is incorrect.", )
        incrow.place(x=100, y=90)

    con.close()

def submitact():
    user = Username.get()
    passw = password.get()

    print(f"The name entered by you is {user} {passw}")
    connect_database(user, passw)


def logged_in():
    tt = tk.Tk()
    tt.geometry("900x750")
    newfrstrow = tk.Label(tt, text="Login successful! Welcome to Patient Charting.", )
    newfrstrow.place(x=100, y=50)


root = tk.Tk()
root.geometry("900x750")
root.title("DBMS Login Page")

# Defining the first row
lblfrstrow = tk.Label(root, text="Username -", )
lblfrstrow.place(x=50, y=20)

Username = tk.Entry(root, width=35)
Username.place(x=150, y=20, width=100)

lblsecrow = tk.Label(root, text="Password -")
lblsecrow.place(x=50, y=50)

password = tk.Entry(root, width=35)
password.place(x=150, y=50, width=100)


submitbtn = tk.Button(root, text="Login",
                    bg='blue', command=submitact)
submitbtn.place(x=150, y=135, width=55)

root.mainloop()

