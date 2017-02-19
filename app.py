import os
import flask
import flask_socketio
from flask import request
from chatterbot import ChatBot

from geopy.geocoders import Nominatim
import forecastio


geolocator = Nominatim()

#darksky
api_key = "6c48b0b26ed6bc18d09c8d6e62e10b27"

#import flask_sqlalchemy
#import models

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)


# URI scheme: postgresql://<username>:<password>@<hostname>:<port>/<database-name>
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://potato:potatosareawesome@localhost/postgres'
#db = flask_sqlalchemy.SQLAlchemy(app)


# Create a new instance of a ChatBot
bot = ChatBot(
    'Default Response Example Bot',
    storage_adapter='chatterbot.storage.JsonFileStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.65,
            'default_response': 'I am sorry, but I do not understand.'
        }
    ],
    trainer='chatterbot.trainers.ListTrainer'
)

# Train the chat bot with a few responses
bot.train([
    'Im off hours',
    'What are we going to do',
    'Youre drunk',
    'lets get drunk',
    'lets go to alvarado street brewery',
    'Im hungry',
    'whats wrong',
    'whats wroooong',
    'speaking of drinking, whens everyone free next week',
    'this is so janky',
    'hello beautiful',
    'watup cuz',
    'Im so beautiful',
    'Im so smart',
    'Im so humble'
])

@app.route('/')
def hello():
    #var_1 = flask.request.args.get('user', "not set")
    #var_2 = flask.request.args.get('var_2', "not set")
    
    #print var_1
    return flask.render_template('index.html')

@socketio.on('connect')
def on_connect():
    print request.sid #gets sid
    print 'Someone connected!'
    
    
    socketio.emit('init', {
            'users' : all_users,
            'name': "muahahah",
        })
    
    

@socketio.on('disconnect')
def on_disconnect():
    print 'Someone disconnected!'
    
    socketio.emit('user:left', {
            'name': "a user",
        }, broadcast=True)
    
    
    
all_numbers = []
all_users = []
all_messages = []
all_sources = []
all_userPictures = []

#gets a new message from the client and broadcasts it
@socketio.on('send:message:server')
def on_server_message(data):
    socketio.emit('send:message:client', data, broadcast=True, include_self=False)
    
    #train chatbot
    bot.train(data['text'])

@socketio.on('send:message:self')
def on_self_message(data):
    socketio.emit('send:message:client', data, broadcast=False, include_self=True)

#gets the user that just joined and sends them to the client
@socketio.on('server:user:join')
def server_user_join(data):
    print "a new person has joined ", data
    socketio.emit('user:join', data, broadcast=True)

#gets the user that just joined and sends them to the client
@socketio.on('user:disconnect')
def user_disconnect():
    print "a client left"
    

@socketio.on('chatbot:message')
def on_chatbot(data):
    if '!! about' in data:
        botmsg = "This webapp is a chatroom"
        socketio.emit('send:message:client', {
            'user': "RONBOT",
            'text': botmsg,
            'src' : ""
        }, broadcast = True)
        
    elif '!! help' in data:
        botmsg = "type '!! about' '!! help', '!! say <something>', '!! bot <chat with the bot>', '!! potato' "
        socketio.emit('send:message:client', {
            'user': "RONBOT",
            'text': botmsg,
            'src' : ""
        }, broadcast = True)
    
    elif '!! say' in data:
        botmsg = "someone told me to say "+(data[len('!! say '):len(data)])
        socketio.emit('send:message:client', {
            'user': "RONBOT",
            'text': botmsg,
            'src' : ""
        }, broadcast = True)
    
    #chat with the bot
    elif '!! bot' in data:
        # Get a response for some unexpected input
        response = bot.get_response((data[len('!! bot '):len(data)]))
        print str("__"+(data[len('!! bot '):len(data)])+"__")
        #print(response)
        socketio.emit('send:message:client', {
            'user': "RONBOT",
            'text': str(response),
            'src' : ""
        }, broadcast = False)
    
    elif '!! potato' in data:
        # Get a response for some unexpected input
        msg = "potatos are delicious"
        #print(response)
        socketio.emit('send:message:client', {
            'user': "RONBOT",
            'text': msg,
            'src' : ""
        }, broadcast = True)
    
    elif '!! weather' in data:
        
        address = (data[len('!! weather'):len(data)])
        
        #checks that there is an address, if not let the user know
        if len(address) == 0:
            msg = "need to provide city or address"
            socketio.emit('send:message:client', {
            'user': "RONBOT",
            'text': msg,
            'src' : ""
        }, broadcast = False)
            return
        
        location = geolocator.geocode(address)
        #"175 5th Avenue NYC"
        #print(location.address)
        #Flatiron Building, 175, 5th Avenue, Flatiron, New York, NYC, New York, ...
        #print((location.latitude, location.longitude))
        
        lat = location.latitude
        lng = location.longitude
        
        forecast = forecastio.load_forecast(api_key, lat, lng)
        
        #print "CURRENT FORECAST"
        
        weather = str(forecast.currently())
        msg = address+": "+weather[len('ForecastioDataPoint instance: '):len(weather)]+" UTC"
        #print (msg)
                
        #print(response)
        socketio.emit('send:message:client', {
            'user': "RONBOT",
            'text': msg,
            'src' : ""
        }, broadcast = True)
    
    else:
        msg = "can't recognize that command fam"
        socketio.emit('send:message:client', {
            'user': "RONBOT",
            'text': msg,
            'src' : ""
        }, broadcast = False)
        
    # Get a response for some unexpected input
    #response = bot.get_response("are you ok")
    #print(response)
    
    
    
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

