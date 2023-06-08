from configparser import ConfigParser

import psycopg2
from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from flask_bcrypt import Bcrypt

login_bp = Blueprint('login', __name__)
bcrypt = Bcrypt()

config = ConfigParser()
config.read('config.ini')

db_host = config.get('database', 'host')
db_port = config.get('database', 'port')
db_name = config.get('database', 'database')
db_user = config.get('database', 'user')
db_password = config.get('database', 'password')

conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    database=db_name,
    user=db_user,
    password=db_password
)

cur = conn.cursor()


@login_bp.route('/', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        flash('You are already logged in', 'danger')
        return redirect(url_for('user', username=session['user']))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == '' or password == '':
            flash('Please fill out all fields', 'danger')
            return redirect(url_for('.login'))

        print(username)
        try:
            cur.execute("SELECT * FROM users WHERE username = %s ", (username,))
            passwords = cur.fetchone()
        except Exception as e:
            flash('Error: ' + str(e), 'danger')
            conn.rollback()
            return redirect(url_for('.login'))
        if passwords is None:
            flash('Invalid username', 'danger')
            return render_template('login.html')
        db_password1 = passwords[1]

        if not bcrypt.check_password_hash(bytes(db_password1), password):
            flash('Invalid username', 'danger')
            return redirect(url_for('.login'))

        else:
            print(username + " logged in")
            # Set session variable
            session['user'] = username
            flash('You are now logged in', 'success')

            return redirect(url_for('user', username=session['user']))

    return render_template('login.html')
