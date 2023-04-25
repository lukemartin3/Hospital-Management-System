from flask import Flask, render_template, request, session, url_for, redirect
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
    msg=''
    if session.get('role') != 0:
        return redirect('/')
    if request.method == 'POST':
        username = request.form.get('username')
        role = request.form.get('role')
        if role == "3":
            specialty = request.form.get('specialty')
        else:
            None
        record = mycursor.execute('SELECT * FROM users WHERE username=%s', (username,))
        if record:
            mycursor.execute('UPDATE users SET roles=%s, specialization=%s WHERE username=%s', (role, specialty,
                                                                                                username))
            con.commit()
            if role == "2":
                msg = 'Successfully created Nurse!'
            else:
                msg = 'Successfully created Physician!'
        else:
            msg = 'Username not found'
    return render_template('assign.html', msg=msg)


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
def register():
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
                session['loggedin'] = True
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
    return render_template("forgot-password.html", msg=msg)


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
    session.pop('role', None)
    return redirect("/")


@app.route("/schedule-appointment", methods=["POST", "GET"])
def schedule():
    msg=''
    if session.get("role") != 0:
        return redirect("/login")
    if request.method == "POST":
        username = request.form.get('username')
        date = request.form.get('date')
        time = request.form.get('time')
        mycursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        record = mycursor.fetchone()
        if record:
            first_name = record[3]
            last_name = record[4]
            specialty = record[16]
            mycursor.execute('INSERT INTO appointments (dr_fname, dr_lname, specialization, date, time) '
                             'VALUES (%s, %s, %s, %s, %s)',
                             (first_name, last_name, specialty, date, time))
            con.commit()
            msg = 'Successfully scheduled physician'
        else:
            msg = 'Invalid username'
    return render_template("scheduling.html", msg=msg)


@app.route("/see-appointments", methods=['POST', 'GET'])
def see_appointments():
    msg=''
    appts=[]
    if not session.get("username"):
        return redirect("/login")
    if request.method == "POST":
        user = 'NULL'
        appointment_id = request.form.get('appointment_id')
        mycursor.execute('UPDATE appointments SET pat_username=%s WHERE appt_id=%s', (user, appointment_id,))
        con.commit()
        msg = 'Successfully deleted appointment'
    else:
        mycursor.execute('SELECT * FROM appointments WHERE pat_username=%s', (session['username'],))
        records = mycursor.fetchall()
        if records:
            appts = [{'id': row[0], 'dr_fname': row[1], 'dr_lname': row[2], 'specialty': row[3], 'date': row[4],
                      'time': row[5]}
                     for row in records]
        else:
            msg = 'No appointments found'
    return render_template("see-appointments.html", appts=appts, msg=msg)


@app.route("/book-appointment", methods=["POST", "GET"])
def book_appointment():
    msg=''
    appts=[]
    if not session.get("username"):
        return redirect("/login")
    if request.method == 'POST':
        appointment_id = request.form.get('appointment_id')
        mycursor.execute('UPDATE appointments SET pat_username=%s WHERE appt_id=%s', (session['username'], appointment_id,))
        con.commit()
        msg = "Appointment booked successfully!"
    if 'specialty' in request.args:
        specialty = request.args.get('specialty')
        mycursor.execute('SELECT * FROM appointments WHERE specialization=%s AND pat_username IS NULL', (specialty,))
        records = mycursor.fetchall()
        if records:
            appts = [{'id': row[0], 'dr_fname': row[1], 'dr_lname': row[2], 'specialty': row[3], 'date': row[4],
                      'time': row[5]}
                     for row in records]
        else:
            msg = "No appointments found"
    return render_template('book-appointment.html', appts=appts, msg=msg)


@app.route("/see-accounts", methods=['POST', 'GET'])
def see_accounts():
    msg=''
    users=[]
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
            msg = "No users found"
    return render_template("see-accounts.html", users=users, msg=msg)

@app.route("/manage-beds", methods=['POST', 'GET'])
def manage_beds():
    msg = ''
    if session.get("role") != 0:
        return redirect("/login")
    if request.method == 'POST':
        bed_id = request.form.get('bed_id')
        delete = request.form.get('delete')
        mycursor.execute('SELECT * FROM beds WHERE bed_id=%s', (bed_id,))
        record = mycursor.fetchone()
        if delete != 'delete':
            if not record:
                mycursor.execute('INSERT INTO beds (bed_id, available) VALUES(%s, 1)', (bed_id,))
                con.commit()
                msg = 'Created new Bed'
            else:
                msg = 'Bed number is already registered'
        else:
            if record:
                mycursor.execute('DELETE FROM beds WHERE bed_id=%s', (bed_id,))
                con.commit()
                msg = 'Deleted bed number'
            else:
                msg = 'Bed number is not found'
    return render_template("manage_beds.html", msg=msg)


# @app.route("/view-beds", methods=['POST', 'GET'])
# def view_beds():
#     beds=[]
#     if session.get("role") != 3:
#         return redirect("/login")
#     if request.method == 'POST':
#         mycursor.execute('SELECT * FROM beds WHERE availability=%s', (1,))
#         record = mycursor.fetchall()
#         if record:
#             beds = [{'bed_id': row[0]}
#                      for row in record]
#         else:
#             msg = "No users found"
#     return render_template("see-accounts.html", beds=beds, msg=msg)


def run_app(debug=True):
    app.run(debug=debug)


if __name__ == "__main__":
    app.run(port=8000, debug=True)


