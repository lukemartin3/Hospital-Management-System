from flask import Flask, render_template, request, session, url_for, redirect
import mysql.connector

app = Flask(__name__)
app.secret_key = 'mysecretkey'

__HOST = 'localhost'
__USERNAME = 'root'
__PASSWORD = 'Topher1028'
__DATABASE = 'FSEdb'

con = mysql.connector.connect(host=__HOST, user=__USERNAME, password=__PASSWORD, database=__DATABASE)
mycursor = con.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html', username=session['username'])


@app.route('/login', methods=['GET','POST'])
def login():
    msg=''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        mycursor.execute('SELECT * FROM user WHERE username=%s AND password=%s',(username, password))
        record = mycursor.fetchone()
        if record:
            session['loggedin'] = True
            session['username'] = record[0]
            return redirect(url_for('home'))
        else:
            msg="Incorrect username or password"
    return render_template('index.html',msg=msg)


@app.route('/registration', methods=['GET','POST'])
def registration():
    msg=''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_pass = request.form.get('confirm_password')
        if password != confirm_pass:
            msg="Passwords do not match"
        else:
            mycursor.execute('SELECT * FROM user WHERE username=%s',(username,))
            record = mycursor.fetchone()
            if record:
                msg="Username already exists"
            else:
                mycursor.execute('INSERT INTO user (username, password) VALUES (%s, %s)',(username, password))
                con.commit()
                msg="You have successfully registered"
    return render_template('registration.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)