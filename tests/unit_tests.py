import unittest
import app


class ChatBotResponseTest(unittest.TestCase):
    def test_command(self):
        response = app.getBotResponse('!! potato')
        self.assertEquals(response, 'potatos are delicious')

if __name__ == '__main__':
    unittest.main()