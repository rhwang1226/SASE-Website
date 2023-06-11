from flask import Flask, render_template, request, g, jsonify, send_from_directory, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from sqlite3 import Error
from waitress import serve
import os

app = Flask(__name__)
app.config['DATABASE'] = 'database.db'  # SQLite database file

app.static_folder = 'static'

# Define routes and views
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/eboard')
def eboard():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    
    cur = con.cursor()

    cur.execute("SELECT * FROM eboard")

    rows = cur.fetchall()
    eboardRows = [{"name": row[0], "position": row[1], "greeting": row[2]} for row in rows]
    

    con.close()
    return render_template('eboard.html',eboardRows=eboardRows)


@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('admin'))
    return render_template('adminLogin.html', error=error)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)