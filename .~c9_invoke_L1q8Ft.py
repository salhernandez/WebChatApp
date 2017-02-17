import os
import flask
import flask_socketio
from flask import request
import flask_sqlalchemy
#import models

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)


# URI scheme: postgresql://<username>:<password>@<hostname>:<port>/<database-name>
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://potato:potatosareawesome@localhost/postgres'
#db = flask_sqlalchemy.SQLAlchemy(app)



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
all_sources = []
all_userPictures = []

#gets a new message from the client and broadcasts it
@socketio.on('send:message:server')
def on_server_message(data):
    socketio.emit('send:message:client', data, broadcast=True)

#gets the user that just joined and sends them to the client
@socketio.on('server:user:join')
def server_user_join(data):
    print "a new person has joined ", data
    socketio.emit('user:join', data, broadcast=True)

socketio.emit('init', {
        'users' : all_users,
        'name': data['user'],
    })

    
"""    
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
    #all_messages.append(data['message'])
    
    
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
    all_sources.append(data['source'])
    all_userPictures.append(data['userPicture'])
    
    print request.sid #gets sid
    
    #emit new message
    socketio.emit('all users', {
        'users': all_users,
        'sources' : all_sources,
        'userPictures' : all_userPictures
    })
    
    socketio.emit('init', {
        'users' : all_users,
        'name': data['user'],
    })
"""

socketio.run(
    app,
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 8080)),
    debug=True
)

