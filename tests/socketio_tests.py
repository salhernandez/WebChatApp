# socketio_tests.py
import app, unittest
class SocketIOTestCase(unittest.TestCase):
    def test_server_acks_connect(self):
        client = app.socketio.test_client(app.app)
        r = client.get_received()
        # print r
        self.assertEquals(len(r), 1)
        from_server = r[0]
        self.assertEquals(
        from_server['name'],
        'hello to client'
        )
        data = from_server['args'][0]
        self.assertEquals(data['message'], 'I acknowledge you!')
        
    
    def test_server_acks_disconnect(self):
        client = app.socketio.test_client(app.app)
        client.emit('disconnect')
        r = client.get_received()
        # print r
        self.assertEquals(len(r), 3)
        from_server = r[1]
        self.assertEquals(
            from_server['name'],
            'test disconnect'
        )
        data = from_server['args'][0]
        self.assertEquals(
            data['name'],
            u'potato'
    )
    
    def test_message_self(self):
        client = app.socketio.test_client(app.app)
        message_info = {
            'user': 'potato',
            'text': 'some text',
            'src' : 'potato.png'
        }
        
        client.emit('send:message:self', message_info)
        result = client.get_received()
        
        response = result[1]
        
        #get socket listen
        self.assertEquals(response['name'],'send:message:client')
        
        #get package data
        data = response['args'][0]
        self.assertEquals(data['user'],u'potato')
        self.assertEquals(data['text'],u'some text')
        self.assertEquals(data['src'],u'potato.png')
    
    #test message when it was not sent by the bot
    def test_send_message_server(self):
        client = app.socketio.test_client(app.app)
        message_info = {
            'user': 'potato',
            'text': 'some text',
            'src' : 'potato.png'
        }
        
        client.emit('send:message:server', message_info)
        result = client.get_received()
        
        response = result[1]
        
        #get socket listen
        self.assertEquals(response['name'],'send:message:client')
        
        #get package data
        data = response['args'][0]
        self.assertEquals(data['user'],u'potato')
        self.assertEquals(data['text'],u'some text')
        self.assertEquals(data['src'],u'potato.png')
        
if __name__ == '__main__':
 unittest.main()