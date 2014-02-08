"""
https://github.com/ozgur/python-linkedin
Using a linkedin api already written.  See above linkedin

install is via pip: sudo pip install python-linkedin

"""
from linkedin import linkedin, server
import BaseHTTPServer
import cgi


class LinkedInHandler:

    def __init__(self):
        self.API_KEY = '77o0i7g6tnd1eb'
        self.API_SECRET = 'zYgn5AyIo7EL1UOz'
        self.RETURN_URL = 'http://localhost:8000'

    def request_authentication(self):
        authentication = linkedin.LinkedInAuthentication(self.API_KEY, self.API_SECRET, self.RETURN_URL, ['r_fullprofile'])
        print authentication.authorization_url  # open this url on your browser
        application = linkedin.LinkedInApplication(authentication)
        self._wait_for_user_to_enter_browser(application)
        print application
        print application.get_profile()

    def _wait_for_user_to_enter_browser(self, app):
        """
        This seems like a super hacky way of doing stuff.
        Probably going to have to stay as we're not going to be running on a
        web server.
        """
        class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
            def do_GET(self):
                p = self.path.split('?')
                if len(p) > 1:
                    params = cgi.parse_qs(p[1], True, True)
                    app.authentication.authorization_code = params['code'][0]
                    print app.authentication.authorization_code
                    app.authentication.get_access_token()
                    print app.authentication.get_access_token()

        server_address = ('', 8000)
        httpd = BaseHTTPServer.HTTPServer(server_address, MyHandler)
        httpd.handle_request()


if __name__ == "__main__":
    li = LinkedInHandler()
    li.request_authentication()

