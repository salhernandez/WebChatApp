import os
import flask
import flask_socketio
from flask import request
from chatterbot import ChatBot
from geopy.geocoders import Nominatim
import forecastio
import flask_sqlalchemy

#to get lat and long
geolocator = Nominatim()

#darksky
api_key = os.getenv('DARK_SKY')

app = flask.Flask(__name__)

# for database
import models

socketio = flask_socketio.SocketIO(app)


# URI scheme: postgresql://<username>:<password>@<hostname>:<port>/<database-name>
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://potato:potatosareawesome@localhost/postgres'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

db = flask_sqlalchemy.SQLAlchemy(app)

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
            'default_response': 'Say what?'
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

    
#these lists will contain all the messages and people that are connected
all_users = []
all_messages = []

def getBotResponse(someString):
    if '!! about' in someString:
        msg = "This web app is an open chatroom"
        
    
    #chat with the bot
    elif '!! bot' in someString:
        theText = str(someString)
        msg = bot.get_response((theText[len('!! bot '):len(theText)]))
        print str("__"+(theText[len('!! bot '):len(theText)])+"__")
            
    elif '!! help' in someString:
        msg = "type '!! about' '!! help', '!! say <x>', '!! bot <chat>', '!! potato', '!! weather <place>'"
        
    elif '!! say' in someString:
        theText = str(someString)
        msg = "someone told me to say "+str(theText[len('!! say '):len(theText)])
        
    elif '!! potato' in someString:
        # Get a response for some unexpected input
        msg = "potatos are delicious"
        
    elif '!! weather' in someString:
        theText = someString
        address = (theText[len('!! weather'):len(theText)])
        
        #checks that there is an address, if not let the user know
        if len(address) == 0:
            msg = "need to provide city or address"
            
        else:
            #gets lat and long based on address
            location = geolocator.geocode(address)
            
            lat = location.latitude
            lng = location.longitude
            
            #gets forecast based on latitude and longitude
            forecast = forecastio.load_forecast(api_key, lat, lng)
            
            weather = str(forecast.currently())
            msg = address+": "+weather[len('ForecastioDataPoint instance: '):len(weather)]+" UTC"
    else:
        msg = "can't recognize that command fam"
    
    return msg

@app.route('/')
def hello():
    return flask.render_template('index.html')

##SOCKETS
#############################################################################
@socketio.on('connect')
def on_connect():
    print request.sid #gets sid
    print 'Someone connected!'
    
    socketio.emit('hello to client', {
        'message': 'I acknowledge you!'
    })

@socketio.on('disconnect')
def on_disconnect():
    print 'Someone disconnected!'
    
    #used for the socket io tests
    socketio.emit('test disconnect', {
            'name': "potato",
        }, broadcast=True)
    
    socketio.emit('user:left', {
            'name': "a user",
        }, broadcast=True)

#gets a new message from the client and broadcasts it
@socketio.on('send:message:server')
def on_server_message(data):
    
    botTrigger = "!!"
    
    aUser = data['user']
    msg = data['text']
    aSrc = data['src']
    
    ##create new message
    message = models.MessageTable(str(aUser), str(aSrc), str(msg))
    models.db.session.add(message)
    models.db.session.commit()
    
    ##trigger bot
    if botTrigger in data['text']:
        aUser = "RONBOT"
        msg = getBotResponse(str(data['text']))
    
    if "RONBOT" in str(aUser):
        socketio.emit('send:message:client', {
        'user': str(data['user']),
        'text': str(data['text']),
        'src' : str(data['src'])
    }, broadcast = True, include_self=True)
        
        ## add response to db
        message = models.MessageTable(str(aUser), str(aSrc), str(msg))
        models.db.session.add(message)
        models.db.session.commit()
    
    else:
        #train chatbot
        bot.train(data['text'])
    
    socketio.emit('send:message:client', {
        'user': str(aUser),
        'text': str(msg),
        'src' : str(aSrc)
    }, broadcast = True, include_self=True)
        
    

#gets the user that just joined and sends them to the client
@socketio.on('local:user:login')
def local_user_login(data):
    print "local user login ", data
    print data['user']
    print data['src']
    
    all_users.append(data['user'])
    
    messagesFromDB = []
    recent = models.db.session.query(models.MessageTable).order_by(models.MessageTable.id.desc())
    for row in recent.from_self().order_by(models.MessageTable.id):
        messagesFromDB.append({
            'user': str(row.user),
            'text': str(row.message),
            'src' : str(row.src)
        })
    
    #on login, inits the info on the client side
    socketio.emit('init', {
        'name': data['user'],
        'users' : all_users,
        'src': data['src'],
        "messagesFromDB": messagesFromDB
    }, 
    broadcast=False)
    
    #send users data to the client
    socketio.emit('user:join', {
            'users' : all_users,
            'name': data['user'],
        })


@socketio.on('send:message:self')
def on_self_message(data):
    socketio.emit('send:message:client', data, broadcast=False, include_self=True)

#gets the user that just joined and sends them to the client
@socketio.on('server:user:join')
def server_user_join(data):
    print "a new person has joined ", data
    
    all_users.append(data['user'])
    print str(data['src'])
    
    socketio.emit('user:join', data, broadcast=True)

#gets the user that just joined and sends them to the client
@socketio.on('user:disconnect')
def user_disconnect():
    print "a client left"

if __name__ == '__main__': # __name__!
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )

