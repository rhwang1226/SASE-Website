from flask import Flask, render_template, request, g, jsonify, send_from_directory, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from sqlite3 import Error
from waitress import serve
import os
import bcrypt
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['DATABASE'] = 'database.db'  # SQLite database file

app.static_folder = 'static'

UPLOAD_FOLDER = 'static/resources'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    eboardRows = [{"name": row[0], "position": row[1], "greeting": row[2], "picture": row[3]} for row in rows]
    

    con.close()
    return render_template('eboard.html',eboardRows=eboardRows)

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')


@app.route('/admin')
def admin():
    if 'authenticated' in session:
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row
        
        cur = con.cursor()

        cur.execute("SELECT * FROM eboard")

        rows = cur.fetchall()
        eboardRows = [{"name": row[0], "position": row[1], "greeting": row[2], "picture": row[3]} for row in rows]
        
        con.close()
        # If the user is already authenticated, redirect to the admin page
        return render_template('admin.html', eboardRows=eboardRows)
    
    return redirect(url_for('login'))

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if 'authenticated' in session:
        # If the user is already authenticated, redirect to the admin page
        return redirect(url_for('admin'))
    
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        
        # Retrieve the user record from the database
        cur.execute("SELECT password, salt FROM login WHERE username=?", (username,))
        result = cur.fetchone()
        
        if result:
            hashed_password = result[0]
            salt = result[1]
            
            # Verify the password
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                session['authenticated'] = True
                return admin()
        
        error = 'Invalid credentials. Please try again.'

    return render_template('adminLogin.html', error=error)

@app.route('/logout')
def logout():
    # Clear the session and log out the user
    session.clear()
    return redirect(url_for('index'))

@app.route('/admin/add-eboard-member', methods=['GET','POST'])
def addEboard():
    if request.method == 'POST':
        name = request.form.get("name")
        position = request.form.get("position")
        greeting = request.form.get("greeting")

        con = sqlite3.connect("database.db")
        cur = con.cursor()
        
        file = request.files['resume']
    
        allowed_extensions = {'png', 'jpg', 'jpeg'}
        if file.filename.split('.')[-1].lower() in allowed_extensions:
            file = request.files['resume']
            if file:
                filename = secure_filename(file.filename)
                destination = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                # Check if a file with the same name already exists
                counter = 1
                while os.path.exists(destination):
                    # Generate a new filename by appending a counter to the original filename
                    filename = f"{os.path.splitext(filename)[0]}_{counter}{os.path.splitext(filename)[1]}"
                    destination = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    counter += 1
                
                file.save(destination)
                print(destination)
                try:
                    cur.execute("INSERT INTO eboard (name, position, greeting, picture) VALUES(?,?,?,?)", (name, position, greeting, filename))
                    con.commit()
                except sqlite3.Error as e:
                    print("An error occurred:", e)

        cur.close()
        con.close()

    return admin()

@app.route('/admin/delete-eboard-member', methods=['GET','DELETE'])
def deleteEboard():
    name = request.args.get("name")
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    cur.execute("SELECT picture FROM eboard WHERE name=?", (name,))
    result = cur.fetchone()
    
    if result:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], result[0])
        if os.path.exists(file_path):
            os.remove(file_path)
        
    try:
        cur.execute("DELETE FROM eboard WHERE name = ?", (name,))
        con.commit()
    except sqlite3.Error as e:
        print("An error occurred:", e)
        return jsonify(success=False, message="Error deleting language")

    return admin()

@app.route('/admin/reset-eboard', methods=['GET','DELETE'])
def resetEboard():
    con = sqlite3.connect("database.db")
    con.execute('DROP TABLE IF EXISTS eboard')
    con.execute('CREATE TABLE eboard (name TEXT NOT NULL, position TEXT NOT NULL, greeting TEXT NOT NULL, picture TEXT NOT NULL)')

    con.commit()
    con.close()

    return admin()

@app.route('/mwrc')
def mwrc():
    return render_template('mwrc.html')

# Error Handling
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

# Run the Flask application
if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000, url_scheme='https')