from flask import Flask, render_template, request, g, jsonify, send_from_directory
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

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)