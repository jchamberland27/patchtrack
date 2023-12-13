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
    return "UI Pending", 200
    #return render_template('index.html')


@app.route('/ping')
def ping():
    """Ping the service."""
    return 'pong', 200


@app.route('/config/get')
def config_get():
    """Return the config."""
    return json.dumps(db.dgetall("config")), 200


@app.route('/config/init')
def config_init():
    """Initialize a blank config."""
    db.dcreate('config')
    db.dcreate('patch')
    db.dcreate('switch')
    db.dump()
    return "INIT OK", 200


@app.route('/config/patch_ports')
def config_patch_ports():
    """Set number of patch panel ports in config."""
    ports = int(request.args.get('ports'))
    db.dadd("config", ('PORT_COUNT_PATCH', ports))
    db.dump()
    return "PORT_COUNT_PATCH UPDATE OK", 200


@app.route('/config/switch_ports')
def config_switch_ports():
    """Set number of switch ports in config."""
    ports = int(request.args.get('ports'))
    db.dadd("config", ('PORT_COUNT_SWITCH', ports))
    db.dump()
    return "PORT_COUNT_SWITCH UPDATE OK", 200

@app.route('/patch/all_ports')
def patch_all_ports():
    """Get all patch ports"""
    return json.dumps(db.dgetall("patch")), 200

@app.route('/patch/<int:port>/clear')
def patch_port_clear(port):
    """Clear a patch port value"""
    if port > db.dget("config", "PORT_COUNT_PATCH") or port < 1:
        return "ERROR: PORT OUT OF RANGE", 401
    elif port not in db.dkeys("patch"):
        return "PATCH_PORT_OPEN", 201
    else:
        db.dpop("patch", port)
        db.dump()
        return "PATCH_PORT_CLEAR OK", 200


@app.route('/patch/<int:port>/get')
def patch_port_get(port):
    """Get a patch port value"""
    if port > db.dget("config", "PORT_COUNT_PATCH") or port < 1:
        return "ERROR: PORT OUT OF RANGE", 401
    elif port not in db.dkeys("patch"):
        return "PATCH_PORT_OPEN", 200
    else:
        return db.dget("patch", port), 200


@app.route('/patch/<int:port>/set')
def patch_port_set(port):
    """Set a patch port value"""
    value = request.args.get('value')
    if value > db.dget("config", "PORT_COUNT_PATCH") or value < 1:
        return "ERROR: PORT OUT OF RANGE", 401
    
    db.dadd("patch", (port, value))
    db.dump()
    
    return "PATCH_PORT_SET OK", 200


@app.route('/switch/all_ports')
def switch_all_ports():
    """Get all switch ports"""
    return json.dumps(db.dgetall("switch")), 200


@app.route('/switch/<int:port>/clear')
def switch_port_clear(port):
    """Clear a switch port value"""
    if port > db.dget("config", "PORT_COUNT_SWITCH") or port < 1:
        return "ERROR: PORT OUT OF RANGE", 401
    elif port not in db.dkeys("switch"):
        return "SWITCH_PORT_OPEN", 201
    else:
        db.dpop("switch", port)
        db.dump()
        return "SWITCH_PORT_CLEAR OK", 200


@app.route('/switch/<int:port>/get')
def switch_port_get(port):
    """Get a switch port value"""
    if port > db.dget("config", "PORT_COUNT_SWITCH") or port < 1:
        return "ERROR: PORT OUT OF RANGE", 401
    elif port not in db.dkeys("switch"):
        return "SWITCH_PORT_OPEN", 200
    else:
        return db.dget("switch", port), 200


@app.route('/switch/<int:port>/set')
def switch_port_set(port):
    """Set a switch port value"""
    value = request.args.get('value')
    if value > db.dget("config", "PORT_COUNT_SWITCH") or value < 1:
        return "ERROR: PORT OUT OF RANGE", 401
    
    db.dadd("switch", (port, value))
    db.dump()
    
    return "SWITCH_PORT_SET OK", 200


#Start app
if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')