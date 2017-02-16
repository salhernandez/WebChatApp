import os
import flask
import flask_socketio
from flask import request

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)

@app.route('/')
def hello():
    var_1 = flask.request.args.get('user', "not set")
    #var_2 = flask.request.args.get('var_2', "not set")
    
    print var_1
    return flask.render_template('index.html')

@socketio.on('connect')
def on_connect():
    print request.sid #gets sid
    print 'Someone connected!'

@socketio.on('disconnect')
def on_disconnect():
    print request.sid #gets sid
    print 'Someone disconnected!'
    
all_numbers = []
all_users = []
all_messages = []

@socketio.on('new number')
def on_new_number(data):
    print "Got an event for new number with data:", data
    # TODO: Fill me out!
    all_numbers.append(data['number'])
    
    print request.sid #gets sid
    socketio.emit('all numbers', {
        'numbers': all_numbers
    })
    
@socketio.on('new message')
def on_new_message(data):
    print "Got an event for new message with data:", data
    # TODO: Fill me out!
    all_messages.append(data['message'])
    
    
    print request.sid #gets sid
    #emit new message
    socketio.emit('all messages', {
        'messages': all_messages
    })

@socketio.on('new user')
def on_new_user(data):
    print "Got an event for new user with data:", data
    # TODO: Fill me out!
    all_users.append(data['user'])
    
    
    print request.sid #gets sid
    
    #emit new message
    socketio.emit('all users', {
        'users': all_users
    })


socketio.run(
    app,
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 8080)),
    debug=True
)

