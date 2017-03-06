import app, unittest, flask_testing, requests
import urllib2

from flask_testing import LiveServerTestCase

class ServerIntegrationTestCase(
    flask_testing.LiveServerTestCase
):
    def create_app(self):
        return app.app
        
    def test_page_response(self):
        response = urllib2.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)

    
if __name__ == '__main__':
    unittest.main()