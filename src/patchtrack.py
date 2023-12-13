#!/usr/bin/python3

from flask import Flask, request, render_template
from flask_socketio import SocketIO
import json
import os
import pickledb

app = Flask(__name__)
socketio = SocketIO(app)

db = pickledb.load('db/db.db', False)
if db is None:
    print("Failed to load DB, exiting")
    exit(1)


@app.route('/')
def display_ui():
    """Display the UI for the dash."""
    return "UI Pending"
    #return render_template('index.html')


@app.route('/ping')
def ping():
    """Ping the service."""
    return 'pong'


#Start app
if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')