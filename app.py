import requests
from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(
    database="service_db",
    user="",
    password="",
    host="127.0.0.1",
    port="5432"
    )

cursor = conn.cursor()

@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')

@app.route('/login/', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == '' and password == '':
        # Redirect to the same login page if creds are empty
        return render_template('login.html', is_empty_creds = True)
    cursor.execute(f'''
    SELECT * FROM service.users 
    WHERE login='{str(username)}' AND password='{str(password)}'
    ''')
    records = list(cursor.fetchall())
    if records == []:
        # Redirect to the same login page if no such a user is in DB
        return render_template('login.html', no_user = username)
    return render_template(
        'account.html', 
        full_name=records[0][1], 
        username=username,
        password=password,
        )