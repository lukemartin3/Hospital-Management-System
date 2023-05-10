from flask import Flask, render_template, request, session, url_for, redirect
import mysql.connector
# Always use Flask.session instead of the Session object for direct access.
from flask_session import Session
from flask import Flask
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash

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
