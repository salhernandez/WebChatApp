import flask_sqlalchemy, app

#for heroku
#app.app.config['SQLALCHEMY_DATABASE_URI'] = app.os.getenv('DATABASE_URL')
app.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://potato:potatosareawesome@localhost/postgres'
db = flask_sqlalchemy.SQLAlchemy(app.app)

class MessageTable(db.Model):
    id = db.Column(db.Integer, primary_key=True) # key
    user = db.Column(db.String(120))
    src = db.Column(db.String(200))
    message = db.Column(db.String(120))
    
    def __init__(self, t, u, v):
        self.user = t
        self.src = u
        self.message = v
        
    def __repr__(self): # what's __repr__?
        return '<MessageTable text: %s %s %s>' % self.user % self.src % self.message

class UserTable(db.Model):
    id = db.Column(db.Integer, primary_key=True) # key
    user = db.Column(db.String(120))
    src = db.Column(db.String(200))
    loginSource = db.Column(db.String(20))
    
    def __init__(self, t, u, v):
        self.user = t
        self.src = u
        self.loginSource = v
        
    def __repr__(self): # what's __repr__?
        return '<UserTable text: %s %s %s>' % self.user % self.src % self.loginSource