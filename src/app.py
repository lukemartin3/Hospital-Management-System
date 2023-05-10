from flask import Flask, render_template, request, session, url_for, redirect
import mysql.connector
# Always use Flask.session instead of the Session object for direct access.
from flask_session import Session
from flask import Flask
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

__HOST = 'localhost'
__USERNAME = 'root'
__PASSWORD = 'alphonse'
__DATABASE = 'test'

app.config['SECRET_KEY'] = "debug key" 
app.config['SESSION_TYPE'] = 'filesystem' 
app.config['SESSION_PERMANENT']= False
Session(app)

app2 = Flask(__name__)
mail= Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'swe.team09@gmail.com'
app.config['MAIL_PASSWORD'] = 'vmxcgujzgzexmsfb'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

INSURANCE = ['Blue Cross Blue Shield','United', 'Anthem']

con = mysql.connector.connect(host=__HOST, user=__USERNAME, password=__PASSWORD, database=__DATABASE)
mycursor = con.cursor(buffered=True)


@app.route("/")
def home():
    if not session.get("username"):
        return redirect("/login")
    return render_template('all/home.html')


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
        mycursor.execute('SELECT * FROM users WHERE username=%s', (username,))
        record = mycursor.fetchone()
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
    return render_template('admin/assign-role.html', msg=msg)


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
    return render_template('all/login.html', msg=msg)

def do_register(cursor, data: dict):
    username = data.get('username')
    password = data.get('password')
    confirm_pass = data.get('password_confirm')
    unique_pin = data.get('four_pin')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    dob = data.get('dob')
    phone = data.get('phone')
    address = data.get('address')
    city = data.get('city')
    state = data.get('state')
    zip = data.get('zip')
    insurance = data.get('insurance')
    med_history = data.get('med_history')

    if unique_pin and len(unique_pin) > 4:
        msg = "Pin can not exceed 4 characters."
    elif password != confirm_pass:
        msg = "Passwords do not match"
    else:
        hashed_password = generate_password_hash(password)
        cursor.execute('SELECT * FROM users WHERE email=%s OR username=%s',
                          (email, username))
        record = cursor.fetchone()
        if record:
            if record[5] == email:
                msg = 'Email already exists'
            else:
                msg = "Username already exists"
        else:
            cursor.execute('INSERT INTO users (username, email, password, pin, '
                             'fname, lname, dob, phone, address, city, states, zip, '
                             'insurance, history) VALUES (%s, %s, %s, %s, %s, %s, %s, '
                             '%s, %s, %s, %s, %s, %s, %s)', (username, email,
                                                             hashed_password, unique_pin,
                                                             first_name, last_name, dob,
                                                             phone, address, city, state,
                                                             zip, insurance, med_history))

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
    return render_template('all/registration.html', msg=msg)


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
        mycursor.execute('SELECT pin FROM users WHERE username=%s AND email=%s', (username, email))
        send_pin = mycursor.fetchone()
        mycursor.execute('SELECT email FROM users WHERE username=%s AND email=%s', (username, email))
        send_email = mycursor.fetchone()
        if record:
            session['loggedin'] = True
            session['username'] = username
            print("this is current session username", session['username'])
            return redirect(url_for('reset'))
        else:
            msg="Incorrect username, email, or pin. Check your email for the correct pin."
            mycursor.execute('SELECT pin FROM users WHERE username=%s AND email=%s', (username, email))
            send_pin = mycursor.fetchone()
            mycursor.execute('SELECT email FROM users WHERE username=%s AND email=%s', (username, email))
            send_email = mycursor.fetchone()

            if send_pin == None or send_email == None:
                msg = "Incorrect username or pin."
            else: 
                msg2 = Message("Hello " + username,
                            sender = "swe.team09@gmail.com", 
                            recipients = ["swe.team09@gmail.com", send_email[0]])
                msg2.body = "here is your 4 digit pin: " + str(send_pin[0])
                mail.send(msg2)

        return render_template('all/forgot-password.html', msg=msg)
    return render_template("all/forgot-password.html", msg=msg)


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
            hashedPassword = generate_password_hash(password)
            mycursor.execute('UPDATE users SET password = %s WHERE username = %s',
                                (hashedPassword, username))
            con.commit()
            session['loggedin'] = True
            session['username'] = username  #record[0]
            print("this is current session username", session['username'])
            return redirect(url_for('login'))
    return render_template('all/reset-password.html', msg=msg)
    

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
    return render_template("admin/scheduling.html", msg=msg)


@app.route("/see-appointments", methods=['POST', 'GET'])
def see_appointments():
    msg=''
    appts=[]
    if not session.get("username"):
        return redirect("/login")
    if request.method == "POST":
        username = 'NULL'
        appointment_id = request.form.get('appointment_id')
        mycursor.execute('UPDATE appointments SET pat_username=%s WHERE appt_id=%s', (username, appointment_id,))
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
    return render_template("patient/see-appointments.html", appts=appts, msg=msg)


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
    return render_template('patient/book-appointment.html', appts=appts, msg=msg)


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
    return render_template("admin/see-accounts.html", users=users, msg=msg)


@app.route("/manage-beds", methods=['POST', 'GET'])
def manage_beds():
    msg = ''
    beds=[]
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
    else:
        mycursor.execute('SELECT * FROM beds')
        records = mycursor.fetchall()
        if records:
            beds = [{'bed_id': row[0], 'available': row[1], 'pat_username': row[2]}
                    for row in records]
        else:
            msg = "No beds found"
    return render_template("admin/manage-beds.html", beds=beds, msg=msg)


@app.route("/assign-bed", methods=['POST', 'GET'])
def assign_bed():
    msg=''
    beds=[]
    if session.get("role") != 3:
        return redirect("/login")
    if request.method == 'POST':
        bed_id = request.form.get('bed_id')
        username = request.form.get('username')
        mycursor.execute('UPDATE beds SET pat_username=%s, available=0 WHERE bed_id=%s',
                         (username, bed_id,))
        con.commit()
        msg = "Bed assigned successfully!"
    else:
        mycursor.execute('SELECT * FROM beds WHERE available=%s', (1,))
        records = mycursor.fetchall()
        if records:
            beds = [{'bed_id': row[0]}
                    for row in records]
        else:
            msg = "No users found"
    return render_template("physician/assign-bed.html", beds=beds, msg=msg)


@app.route('/billing-rates', methods=['GET', 'POST'])
def billing_rates():
    msg = ''
    # Check if user is logged in and is an admin
    if session.get("role") == 1:
        return redirect("/")
    # Fetch current billing rates
    if request.method == 'POST':
        if 'new_procedure' in request.form and 'new_rate' in request.form:
            procedure = request.form['new_procedure']
            rate = request.form['new_rate']
            # Check if procedure exists

            mycursor.execute('SELECT * FROM billing_rates WHERE procedures = %s', (procedure,))
            existing_procedure = mycursor.fetchone()
            if existing_procedure:
                mycursor.execute("UPDATE billing_rates SET rate = %s WHERE procedures = %s", (rate, procedure))
                msg = 'New Rate Applied'
            else:
                mycursor.execute('INSERT INTO billing_rates (procedures, rate) VALUES (%s, %s)', (procedure, rate))
                msg = 'Procedure has been added'
            con.commit()
    mycursor.execute('SELECT * FROM billing_rates')
    billing_rates = mycursor.fetchall()
    return render_template('nurse/billing-rates.html', billing_rates=billing_rates, msg=msg)


@app.route('/invoice_patient', methods=['GET', 'POST'])
def invoice_patient():
    msg = ''
    users = []
    discount_rate = 0.0
    mycursor.execute('SELECT username, procedure_name, SUM(price) as price, email FROM invoice WHERE username=%s '
                     'GROUP BY username, procedure_name, email', (session['username'],))
    record = mycursor.fetchall()
    if record:
        for row in record:
            username, procedure_name, total_price, email = row
            mycursor.execute('SELECT rate FROM billing_rates WHERE procedures=%s', (procedure_name,))
            billing_record = mycursor.fetchone()
            if billing_record:
                original_price = billing_record[0]
                discount_rate = original_price - total_price
                users.append({'username': username, 'procedure_name': procedure_name, 'original_price': original_price, 'total_price': total_price, 'email': email, 'discount_rate': discount_rate})
    else:
        msg = "No invoices found for username"
    return render_template('patient/invoice-patient.html', users=users, msg=msg)


@app.route('/assign-procedure', methods=['GET', 'POST'])    
def assign_procedure():
    msg = ''
    discount_rate = 0.0
    if request.method == "POST":
        username = request.form.get('username')
        proced = request.form.get('procedure')
        email = request.form.get('email')
        mycursor.execute('SELECT insurance FROM users WHERE username=%s', (username,))
        insurance = mycursor.fetchone()
        mycursor.execute('SELECT rate FROM billing_rates WHERE procedures=%s', (proced,))
        price = mycursor.fetchall()
        print(price)
        if price:
            #Has insurance, discount the price
            if insurance and insurance[0] in INSURANCE:
                discount_rate = 0.8 #20% discount from insurance
                old_price = price[0][0]
                new_price = old_price * discount_rate
                price[0] = new_price
                mycursor.execute('INSERT INTO invoice (username, procedure_name, price, email) VALUES (%s, %s, %s, %s)',
                             (username, proced, price[0], email))
                con.commit()
                msg = 'Successfully added procedure for user with insurance'
            #No insurance, do as normal
            else:
                mycursor.execute('INSERT INTO invoice (username, procedure_name, price, email) VALUES (%s, %s, %s, %s)',
                             (username, proced, price[0][0], email))
                con.commit()
                msg = "Successfully added procedure for user."
        else:
            msg = "Incorrect username, procedure, or email. Please verify the information entered is correct."
    mycursor.execute('SELECT * FROM billing_rates')
    billing_rates = mycursor.fetchall()
    return render_template('admin/assign-procedure.html', msg=msg, billing_rates=billing_rates)


@app.route('/make-payment', methods=['GET', 'POST'])
def make_payment():
    msg=''
    billing=0.00
    if session.get("role") != 1:
        return redirect("/login")
    if request.method == 'POST':
        mycursor.execute('UPDATE invoice SET price=0.00 WHERE username=%s', (session['username'],))
        con.commit()
        mycursor.execute('DELETE FROM invoice WHERE username=%s', (session['username'],))
        con.commit()
        msg = "Payment Success!"
    else:
        mycursor.execute('SELECT SUM(price) FROM invoice WHERE username=%s', (session['username'],))
        record = mycursor.fetchone()[0]
        if record:
            billing = "{:.2f}".format(record)
    return render_template("patient/make-payment.html", billing=billing, msg=msg)


@app.route('/notification', methods=['GET', 'POST'])
def notification():
    msg=''
    if session.get("role") == 1:
        return redirect("/login")
    if request.method == 'POST':
        pat_username = request.form.get('pat_username')
        message = request.form.get('message')
        role = request.form.get('role')
        lname = request.form.get('lname')
        sender = role + ' ' + lname
        mycursor.execute('SELECT * FROM users WHERE username=%s',
                        (pat_username,))
        record = mycursor.fetchone()
        if record:

            try:
                mycursor.execute('INSERT INTO notification (pat_username, message, sender) VALUES (%s, %s, %s)',
                                 (pat_username, message, sender))
                con.commit()
                msg = "Notification message successfully sent to Patient"
            except:
                msg = 'Your message is too long'
        else:
            msg = 'Invalid patient'
    return render_template("all/notification.html", msg=msg)


@app.route('/inbox', methods=['GET', 'POST'])
def inbox():
    msg=''
    messages=[]
    if session.get("role") != 1:
        return redirect("/login")
    if request.method == 'POST':
        notif_id = request.form.get('notif_id')
        mycursor.execute('DELETE FROM notification WHERE notif_id=%s', (notif_id,))
        con.commit()
        msg = "Message Deleted"
    else:
        mycursor.execute('SELECT * FROM notification WHERE pat_username=%s', (session['username'],))
        record = mycursor.fetchall()
        if record:
            messages = [{'notif_id': row[0], 'message': row[2], 'sender': row[3]}
                        for row in record]
    return render_template("patient/inbox.html", messages=messages, msg=msg)


@app.route("/discharge-patient", methods=['POST', 'GET'])
def discharge_patient():
    msg=''
    beds=[]
    if session.get("role") != 2:
        return redirect("/login")
    if request.method == 'POST':
        bed_id = request.form.get('bed_id')
        mycursor.execute('SELECT * FROM beds WHERE bed_id=%s', (bed_id,))
        record = mycursor.fetchone()
        if record:
            mycursor.execute('UPDATE beds SET available=1, pat_username=NULL WHERE bed_id=%s', (bed_id,))
            con.commit()
            msg = 'Patient successfully discharged'
        else:
            msg = 'Bed number is not found'
    else:
        mycursor.execute('SELECT * FROM beds WHERE available=0')
        records = mycursor.fetchall()
        if records:
            beds = [{'bed_id': row[0], 'pat_username': row[2]}
                    for row in records]
        else:
            msg = 'No occupied beds'
    return render_template("nurse/discharge-patient.html", beds=beds, msg=msg)

def run_app(debug=True):
    app.run(debug=debug)


app.run(port=8000, debug=True)
if __name__ == "__main__":
    app.run(port=8000, debug=True)


