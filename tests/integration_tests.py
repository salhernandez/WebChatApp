import app, unittest, flask_testing, requests
import flask
import urllib2

class ServerIntegrationTestCase(
    flask_testing.LiveServerTestCase
):
    def create_app(self):
        app = flask.Flask(__name__)
        app.config['TESTING'] = True
        # Default port is 5000
        app.config['LIVESERVER_PORT'] = 8080
        # Default timeout is 5 seconds
        app.config['LIVESERVER_TIMEOUT'] = 10
        return app

    def test_server_is_up_and_running(self):
        response = urllib2.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)

    
if __name__ == '__main__':
    unittest.main()