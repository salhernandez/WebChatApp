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

#api_key = '6c48b0b26ed6bc18d09c8d6e62e10b27'

app = flask.Flask(__name__)

# for database
import models

socketio = flask_socketio.SocketIO(app)


# URI scheme: postgresql://<username>:<password>@<hostname>:<port>/<database-name>
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://potato:potatosareawesome@localhost/postgres'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

db = flask_sqlalchemy.SQLAlchemy(app)

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

@app.route('/')
def hello():
    #var_1 = flask.request.args.get('user', "not set")
    #var_2 = flask.request.args.get('var_2', "not set")
    
    
    #querying database for messages
    ########################################################################################################
    recent = models.db.session.query(models.MessageTable).order_by(models.MessageTable.id.desc()).limit(100)
    for row in recent.from_self().order_by(models.MessageTable.id):
        #print "FROM MESSAGE TABLE "+str(row.message)
        pass
    #all_messages.append({'message':row.message,'name':row.name,'picture':row.picture})
    
    #querying for users
    recent = models.db.session.query(models.UserTable).order_by(models.UserTable.id.desc()).limit(100)
    for row in recent.from_self().order_by(models.UserTable.id):
        #print "FROM USER TABLE "+str(row.user) +" "+str(row.src)
        pass
    #all_messages.append({'message':row.message,'name':row.name,'picture':row.picture})
    
    
    #print var_1
    return flask.render_template('index.html')

##SOCKETS
#############################################################################
@socketio.on('connect')
def on_connect():
    print request.sid #gets sid
    print 'Someone connected!'
    
    """
    socketio.emit('init', {
            'users' : all_users,
            'name': "muahahah",
        })
        """

@socketio.on('disconnect')
def on_disconnect():
    print 'Someone disconnected!'
    
    socketio.emit('user:left', {
            'name': "a user",
        }, broadcast=True)
    

#gets a new message from the client and broadcasts it
@socketio.on('send:message:server')
def on_server_message(data):
    
    
    #socketio.emit('send:message:client', data, broadcast=True, include_self=True)
    
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
        print "bot triggered"
        aUser = "RONBOT"
        
        if '!! about' in data['text']:
            msg = "This webapp is a chatroom"
        
        elif '!! help' in data['text']:
            msg = "type '!! about' '!! help', '!! say <something>', '!! bot <chat with the bot>', '!! potato' "
            
        elif '!! say' in data['text']:
            theText = str(data['text'])
            msg = "someone told me to say "+str(theText[len('!! say '):len(theText)])
    
        #chat with the bot
        elif '!! bot' in data['text']:
            theText = str(data['text'])
            msg = bot.get_response((theText[len('!! bot '):len(theText)]))
            print str("__"+(theText[len('!! bot '):len(theText)])+"__")
            
        elif '!! potato' in data['text']:
            # Get a response for some unexpected input
            msg = "potatos are delicious"
            
        elif '!! weather' in data['text']:
            theText = data['text']
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
                
                #print "CURRENT FORECAST"
                
                weather = str(forecast.currently())
                msg = address+": "+weather[len('ForecastioDataPoint instance: '):len(weather)]+" UTC"
        else:
            msg = "can't recognize that command fam"
    
    
    
    """
    recent = models.db.session.query(models.MessageTable).order_by(models.MessageTable.id.desc()).limit(100)
    for row in recent.from_self().order_by(models.MessageTable.id):
        print "FROM MESSAGE TABLE "+str(row.message)+str(row.user)+str(row.src)
    """
    
    isItRonbot = False
    
    if "RONBOT" in str(aUser):
        isItRonbot = True
        
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
        #print "FROM MESSAGE TABLE "+str(row.message)+str(row.user)+str(row.src)
        pass
        messagesFromDB.append({
            'user': str(row.user),
            'text': str(row.message),
            'src' : str(row.src)
        })
    
    
    socketio.emit('init', {
        'name': data['user'],
        'users' : all_users,
        'src': data['src'],
        "messagesFromDB": messagesFromDB
    }, 
    broadcast=False)
    #socketio.emit('user:join', data, broadcast=True, include_self=False)

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


#@socketio.on('chatbot:message')
def on_chatbot(data):
    msg = "huh?"
    

    if '!!' not in data:
        msg = "can't recognize that command fam"
        """
        socketio.emit('send:message:client', {
            'user': "RONBOT",
            'text': msg,
            'src' : ""
        }, broadcast = False)
        """
        newMsg = {}
        newMsg =  {
                'user': "RONBOT",
                'text': msg,
                'src' : ""
            }
        return newMsg
    if '!! about' in data:
        msg = "This webapp is a chatroom"
        """
        socketio.emit('send:message:client', {
            'user': "RONBOT",
            'text': botmsg,
            'src' : ""
        }, broadcast = True)
        """
        
    elif '!! help' in data:
        msg = "type '!! about' '!! help', '!! say <something>', '!! bot <chat with the bot>', '!! potato' "
        """
        socketio.emit('send:message:client', {
            'user': "RONBOT",
            'text': botmsg,
            'src' : ""
        }, broadcast = True)
        """
    
    elif '!! say' in data:
        msg = "someone told me to say "+(data[len('!! say '):len(data)])
        """
        socketio.emit('send:message:client', {
            'user': "RONBOT",
            'text': botmsg,
            'src' : ""
        }, broadcast = True)
        """
    
    #chat with the bot
    elif '!! bot' in data:
        # Get a response for some unexpected input
        response = bot.get_response((data[len('!! bot '):len(data)]))
        print str("__"+(data[len('!! bot '):len(data)])+"__")
        
        msg = response
        #print(response)
        """
        socketio.emit('send:message:client', {
            'user': "RONBOT",
            'text': str(response),
            'src' : ""
        }, broadcast = False)
        """
    
    elif '!! potato' in data:
        # Get a response for some unexpected input
        msg = "potatos are delicious"
        #print(response)
        """
        socketio.emit('send:message:client', {
            'user': "RONBOT",
            'text': msg,
            'src' : ""
        }, broadcast = True)
        """
    
    elif '!! weather' in data:
        
        address = (data[len('!! weather'):len(data)])
        
        #checks that there is an address, if not let the user know
        if len(address) == 0:
            msg = "need to provide city or address"
            """
            socketio.emit('send:message:client', {
            'user': "RONBOT",
            'text': msg,
            'src' : ""
        }, broadcast = False)
        """
            newMsg = {}
            newMsg =  {
                    'user': "RONBOT",
                    'text': msg,
                    'src' : ""
                }
            return newMsg
        
        #gets lat and long based on address
        location = geolocator.geocode(address)
        
        lat = location.latitude
        lng = location.longitude
        
        #gets forecast based on latitude and longitude
        forecast = forecastio.load_forecast(api_key, lat, lng)
        
        #print "CURRENT FORECAST"
        
        weather = str(forecast.currently())
        msg = address+": "+weather[len('ForecastioDataPoint instance: '):len(weather)]+" UTC"
        #print (msg)
            
        """   
        socketio.emit('send:message:client', {
            'user': "RONBOT",
            'text': msg,
            'src' : ""
        }, broadcast = True)
        """
    newMsg = {}
    newMsg =  {
            'user': "RONBOT",
            'text': msg,
            'src' : ""
        }
    return newMsg
        
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

if __name__ == '__main__': # __name__!
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )

