import unittest
import app


class ChatBotResponseTest(unittest.TestCase):
    def test_command_about(self):
        response = app.getBotResponse('!! about')
        self.assertEquals(response, 'This web app is an open chatroom')
    
    def test_command_potato(self):
        response = app.getBotResponse('!! potato')
        self.assertEquals(response, 'potatos are delicious')
    
    def test_command_help(self):
        msg = "type '!! about' '!! help', '!! say <something>', '!! bot <chat with the bot>', '!! potato', '!! weather <city or address>' "
        response = app.getBotResponse('!! help')
        self.assertEquals(response, msg)
    
    def test_command_say(self):
        response = app.getBotResponse('!! say hellooo')
        msg = "someone told me to say hellooo"
        self.assertEquals(response, msg)
        
    def test_command_say_2(self):
        response = app.getBotResponse('!! say potato')
        msg = "someone told me to say potato"
        self.assertEquals(response, msg)
    
    def test_command_invalid(self):
        response = app.getBotResponse('!! hello')
        msg = "can't recognize that command fam"
        self.assertEquals(response, msg)
    
    def test_command_invalid_2(self):
        response = app.getBotResponse('!! a potato is delicious')
        msg = "can't recognize that command fam"
        self.assertEquals(response, msg)
    
    def test_command_invalid_3(self):
        response = app.getBotResponse('!! reply potato')
        msg = "can't recognize that command fam"
        self.assertEquals(response, msg)
    
    def test_command_invalid_4(self):
        response = app.getBotResponse('!! not say potato')
        msg = "can't recognize that command fam"
        self.assertEquals(response, msg)
    
    def test_invalid_5(self):
        response = app.getBotResponse('!! echo potato')
        self.assertEquals(response, "can't recognize that command fam")

if __name__ == '__main__':
    unittest.main()