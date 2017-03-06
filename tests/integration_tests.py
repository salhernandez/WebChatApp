import app, unittest, flask_testing, requests
import urllib2

from flask_testing import LiveServerTestCase

class ServerIntegrationTestCase(
    flask_testing.LiveServerTestCase
):
    def create_app(self):
        return app.app
    
    #checks that the page is live
    def test_page_response(self):
        response = urllib2.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)
    
    #checks that the page returns something
    #def test_server_sends_hello(self):
    #    r = requests.get(self.get_server_url())
    #    self.assertGreater(len(r.text), 0)
    
    #makes sure that it is an html page
    def test_getty_images(self):
        r = requests.get(self.get_server_url())
        self.assertIn(r.text[0], "<html>")
    
if __name__ == '__main__':
    unittest.main()