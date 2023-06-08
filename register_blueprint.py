from configparser import ConfigParser

import psycopg2
from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from flask_bcrypt import Bcrypt



register_bp = Blueprint('register', __name__)
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


@register_bp.route('/', methods=['GET', 'POST'])
def register():
    if 'user' in session:
        flash('You are already logged in', 'danger')
        return redirect(url_for('user', username=session['user']))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']

        if username == '' or password == '':
            flash('Please fill out all fields', 'danger')
            return redirect(url_for('.register'))

        if username.isnumeric():
            flash('Username cannot be a number', 'danger')
            return redirect(url_for('.register'))

        if password != password2:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('.register'))

        print(username)

        password = bcrypt.generate_password_hash(password, 10)
        try:
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cur.fetchone()
        except Exception as e:
            flash('Error: ' + str(e), 'danger')
            conn.rollback()
            return redirect(url_for('.register'))

        if user:
            flash('Username already exists', 'danger')
            return redirect(url_for('.register'))
        try:
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            session['user'] = username
            flash('You are now registered and can login', 'success')
            return redirect(url_for('.login'))
        except Exception as e:
            flash('Error registering: ' + str(e), 'danger')
            conn.rollback()
            return redirect(url_for('.register'))

    return render_template('register.html')
