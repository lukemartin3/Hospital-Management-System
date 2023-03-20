import tkinter as tk
import mysql.connector 
from tkinter import *
import getpass
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

db_pw = getpass.getpass("Enter database password: ")
__HOST = '127.0.0.1'
__USERNAME = 'root'
__PASSWORD = db_pw
__DATABASE = 'users'

con = mysql.connector.connect(host=__HOST,user=__USERNAME,password=__PASSWORD,database=__DATABASE)
mycursor = con.cursor()

####################
# CONFIRM LOGIN
def connect_database(username,password):
    mypassword_queue =[]
    sql_query = "SELECT * FROM logon WHERE username ='%s' AND password ='%s'" % (username, password)

    try:
        mycursor.execute(sql_query)
        myresults = mycursor.fetchall()
        for row in myresults:
            for x in row:
                mypassword_queue.append(x)
    except:
        print('error occured')

    if (username and password) in mypassword_queue:
        print('Login Successful.')
        root.destroy()
        logged_in()
    elif username in [x for i, x in enumerate(myresults) if i % 2 == 0]:
        print("Your password has been reset. Please check your email for a new password.")
    else:
        print('ERROR: Username or Password is incorrect.')
        incrow = tk.Label(root, text="Username or Password is incorrect.", )
        incrow.place(x=100, y=90)

####################
# GET USERNAME/PASSWORD FOR LOGIN
def submitact():
    user = Username.get()
    passw = password.get()

    print(f"The name entered by you is {user} {passw}")
    connect_database(user, passw)

####################
# CHARTING HOME PAGE 
def logged_in():
    tt = tk.Tk()
    tt.geometry("900x750")
    tt.title("Patient Charting Home")
    newfrstrow = tk.Label(tt, text="Login successful! Welcome to Patient Charting.", )
    newfrstrow.place(x=100, y=50)

####################
# ACCOUNT CREATION CLASS
class Creation: 

    def create_account(self):
        self.ca = tk.Tk()
        self.ca.geometry("700x500")
        self.ca.title("Account Creation")
        ca_row1 = tk.Label(self.ca, text="Create your account", )
        ca_row1.place(x=100, y=110)   

        ca_user = tk.Label(self.ca, text="New username -", )
        ca_user.place(x=50, y=20)

        self.new_user = tk.Entry(self.ca, width=35)
        self.new_user.place(x=200, y=20, width=100)

        ca_pass = tk.Label(self.ca, text="New password -")
        ca_pass.place(x=50, y=50)

        self.new_pass = tk.Entry(self.ca, show="*", width=35)
        self.new_pass.place(x=200, y=50, width=100)

        ca_conf = tk.Label(self.ca, text="Confirm password -")
        ca_conf.place(x=50, y=80)

        self.confirm_pass = tk.Entry(self.ca, show="*", width=35)
        self.confirm_pass.place(x=200, y=80, width=100)

        submitbtn = tk.Button(self.ca, text="Create",
                            bg='blue', command = self.db_create)
        submitbtn.place(x=150, y=150, width=55)

    def db_create(self):
        user = self.new_user.get()
        passwr = self.new_pass.get()
        confpss = self.confirm_pass.get()
        val = (user, passwr)

        if passwr != confpss:
            ca_err = tk.Label(self.ca, text="PASSWORDS DO NOT MATCH: Close the window and try again.", )
            ca_err.place(x=100, y=180)
        else:
            create_acct_sql = "INSERT INTO logon (username, password) VALUES (%s, %s)"
            mycursor.execute(create_acct_sql, val)
            con.commit()
            self.ca.destroy()

#######################
# FORGOT PASSWORD CLASS
class ForgotPassword:

    def __init__(self, master):
        self.master = master
        master.title("Forgot Password")

        # Create widgets
        self.email_label = tk.Label(master, text="Email:")
        self.email_entry = tk.Entry(master, width=30)
        self.new_password_label = tk.Label(master, text="New Password:")
        self.new_password_entry = tk.Entry(master, show="*", width=30)
        self.confirm_password_label = tk.Label(master, text="Confirm Password:")
        self.confirm_password_entry = tk.Entry(master, show="*", width=30)
        self.submit_button = tk.Button(master, text="Submit", command=self.submit)

        # Layout widgets
        self.email_label.grid(row=0, column=0)
        self.email_entry.grid(row=0, column=1)
        self.new_password_label.grid(row=1, column=0)
        self.new_password_entry.grid(row=1, column=1)
        self.confirm_password_label.grid(row=2, column=0)
        self.confirm_password_entry.grid(row=2, column=1)
        self.submit_button.grid(row=3, column=1)

    def submit(self):
        email = self.email_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if new_password != confirm_password:
            tk.messagebox.showerror("Error", "Passwords do not match.")
        else:
            # Update password in the database
            sql_query = f"UPDATE logon SET password='{new_password}' WHERE email='{email}'"
            mycursor.execute(sql_query)
            con.commit()

            # Send email with new password
            sender_email = "your_email@example.com"  # Update this with your email address
            sender_password = "your_password"  # Update this with your password
            recipient_email = email
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = recipient_email
            message['Subject'] = "Password Reset Requested"
            body = f"Dear user,\n\nYour password has been reset to:\n\n{new_password}\n\nPlease log in with this new password and change it immediately.\n\nBest regards"
            message.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(sender_email, sender_password)
                smtp.send_message(message)

            tk.messagebox.showinfo("Success", "Password reset. Please check your email for your new password.")
            self.master.destroy()

#################
# FORGOT PASSWORD
def forgot_password():
    ForgotPassword((tk.Tk()))

####################
# HOME PAGE 
root = tk.Tk()
root.geometry("900x750")
root.title("DBMS Login Page")

lblfrstrow = tk.Label(root, text="Username -", )
lblfrstrow.place(x=50, y=20)

Username = tk.Entry(root, width=35)
Username.place(x=150, y=20, width=100)

lblsecrow = tk.Label(root, text="Password -")
lblsecrow.place(x=50, y=50)

password = tk.Entry(root, show="*", width=35)
password.place(x=150, y=50, width=100)

submitbtn = tk.Button(root, text="Login",
                    bg='blue', command=submitact)
submitbtn.place(x=150, y=135, width=55)

####################
# ACCOUNT CREATION 
crt = Creation()
crt_button = tk.Button(root, text="Create Account",
                    bg='green', command = crt.create_account)
crt_button.place(x = 150, y = 170, width = 125)


forgot_password_btn = tk.Button(root, text="Forgot Password?",
                    bg='yellow', command=forgot_password)
forgot_password_btn.place(x=150, y=220, width=140)


####################
# ROOT
root.mainloop()
con.close()