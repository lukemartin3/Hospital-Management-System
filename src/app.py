from flask import Flask, render_template, request, session, url_for, redirect, jsonify
import mysql.connector
# Always use Flask.session instead of the Session object for direct access.
from flask_session import Session
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

__HOST = 'localhost'
__USERNAME = 'root'
__PASSWORD = 'Topher1028'
__DATABASE = 'fsedb'

app.config['SECRET_KEY'] = "debug key" 
app.config['SESSION_TYPE'] = 'filesystem' 
app.config['SESSION_PERMANENT']= False
Session(app)

con = mysql.connector.connect(host=__HOST, user=__USERNAME, password=__PASSWORD, database=__DATABASE)
mycursor = con.cursor()


@app.route("/")
def home():
    if not session.get("username"):
        return redirect("/login")
    return render_template('home.html')


@app.route('/assign_roles', methods=["POST", "GET"])
def assign_roles():
    if session.get('role') != 0:
        return redirect('/')
    if request.method == 'POST':
        username = request.form.get('username')
        role = request.form.get('role')
        print(role)
        if role == "3":
            specialty = request.form.get('specialty')
        else:
            None
        mycursor.execute('UPDATE users SET roles=%s, specialization=%s WHERE username=%s', (role, specialty, username))
        con.commit()
        msg = 'Successfully created Nurse/Physician!'
        return render_template('assign.html', msg=msg)
    return render_template('assign.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    msg=''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        mycursor.execute('SELECT * FROM users WHERE username=%s',
                         (username,))
        record = mycursor.fetchone()
        if record and check_password_hash(record[1], password):
            session['loggedin'] = True
            session['username'] = username
            session['role'] = record[15]
            return redirect(url_for('home'))
        else:
            msg="Incorrect username or password"
    return render_template('login.html', msg=msg)


@app.route("/register", methods=["POST", "GET"])
def register_new_user():
    msg = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_pass = request.form.get('password_confirm')
        unique_pin = request.form.get('four_pin')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        dob = request.form.get('dob')
        phone = request.form.get('phone')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        zip = request.form.get('zip')
        insurance = request.form.get('insurance')
        med_history = request.form.get('med_history')

        if unique_pin and len(unique_pin) > 4:
            msg = "Pin can not exceed 4 characters."
        elif password != confirm_pass:
            msg = "Passwords do not match"
        else:
            hashed_password = generate_password_hash(password)
            mycursor.execute('SELECT * FROM users WHERE email=%s OR username=%s',
                              (email, username))
            record = mycursor.fetchone()
            if record:
                if record[5] == email:
                    msg = 'Email already exists'
                else:
                    msg = "Username already exists"
            else:
                mycursor.execute('INSERT INTO users (username, email, password, pin, '
                                 'fname, lname, dob, phone, address, city, states, zip, '
                                 'insurance, history) VALUES (%s, %s, %s, %s, %s, %s, %s, '
                                 '%s, %s, %s, %s, %s, %s, %s)', (username, email,
                                                                 hashed_password, unique_pin,
                                                                 first_name, last_name, dob,
                                                                 phone, address, city, state,
                                                                 zip, insurance, med_history))
                con.commit()
                #session['loggedin'] = True
                session['username'] = username
                return redirect(url_for('home'))
    return render_template('registration.html', msg=msg)


@app.route("/forgot-password", methods=["POST", "GET"])
def forgot_password():
    msg=''
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        unique_pin = request.form.get('four_pin')
        mycursor.execute('SELECT * FROM users WHERE username=%s AND email=%s AND pin=%s',
                         (username, email, unique_pin))
        record = mycursor.fetchone()
        if record:
            session['loggedin'] = True
            session['username'] = username
            print("this is current session username", session['username'])
            return redirect(url_for('reset'))
        else:
            msg="Incorrect username, email, or pin"
        return render_template('forgot-password.html', msg=msg)
    return render_template("forgot-password.html")


@app.route("/reset-password", methods=["POST", "GET"])
def reset():
    msg=''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_pass = request.form.get('password_confirm')
        if password != confirm_pass:
            msg="Passwords do not match"
        else:
            mycursor.execute('UPDATE users SET password = %s WHERE username = %s',
                                (password, username))
            con.commit()
            session['loggedin'] = True
            session['username'] = username  #record[0]
            print("this is current session username", session['username'])
            return redirect(url_for('login'))
    return render_template('reset-password.html', msg=msg)
    

@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect("/")


@app.route("/schedule-appointment", methods=["POST", "GET"])
def schedule():
    if session.get("role") != 0:
        return redirect("/login")
    if request.method == "POST":
        username = request.form.get('username')
        date = request.form.get('date')
        time = request.form.get('time')
        fee = request.form.get('fee')
        mycursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        record = mycursor.fetchone()
        print(record)
        first_name = record[3]
        last_name = record[4]
        specialty = record[16]
        mycursor.execute('INSERT INTO appointments (dr_fname, dr_lname, specialization, date, time, fee) '
                         'VALUES (%s, %s, %s, %s, %s, %s)',
                         (first_name, last_name, specialty, date, time, fee))
        con.commit()
        return render_template("home.html")
    return render_template("scheduling.html")


# @app.route("/see-appointments", methods=['POST', 'GET'])
# def see_appointments():
#     if not session.get("username"):
#         return redirect("/login")
#     if request.method == "POST":
#         pass # TODO: What should we do here?
#     else:
#         mycursor.execute('SELECT * FROM appointments WHERE username=%s', (session['username'],))
#         appointments = mycursor.fetchall()
#         return render_template("see-appointments.html", appointments=appointments)
#
#
@app.route("/book-appointment", methods=["POST", "GET"])
def book_appointment():
    msg=''
    appts = []
    if not session.get("username"):
        return redirect("/login")
    if request.method == 'POST':
        username = request.form.get('username')
        appointment_id = request.form.get('appointment_id')
        mycursor.execute('UPDATE appointments SET pat_username=%s WHERE id=%s', (username, appointment_id,))
        con.commit()
        msg = "Appointment booked successfully!"
    if 'specialty' in request.args:
        specialty = request.args.get('specialty')
        mycursor.execute('SELECT * FROM appointments WHERE specialization=%s', (specialty,))
        records = mycursor.fetchall()
        if records:
            appts = [{'id': row[0], 'dr_fname': row[1], 'dr_lname': row[2], 'specialty': row[3], 'date': row[4],
                      'time': row[5], 'fee': row[6]}
                     for row in records]
    return render_template('book-appointment.html', appts=appts, msg=msg)


@app.route("/see-accounts", methods=['POST', 'GET'])
def see_accounts():
    msg = ''
    if session.get("role") != 0:
        return redirect("/login")
    if request.method == 'POST':
        search_text = request.form['search_text']
        mycursor.execute('SELECT * FROM users WHERE fname LIKE %s OR lname LIKE %s',
                         (f'%{search_text}%', f'%{search_text}%'))
        record = mycursor.fetchall()
        if record:
            users = [{'username': row[0], 'fname': row[3], 'lname': row[4], 'email': row[5], 'dob': row[6],
                      'phone': row[7], 'address': row[8], 'city': row[9], 'state': row[10], 'zip': row[11],
                      'insurance': row[12], 'history': row[13], 'billing': row[14], 'specialization': row[16]}
                     for row in record]
        else:
            users = []
            msg = "No users found"
    else:
        users = []
    return render_template("see-accounts.html", users=users, msg=msg)


def run_app(debug=True):
    app.run(debug=debug)

if __name__ == "__main__":
    run_app(True)


