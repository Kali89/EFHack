"""
https://github.com/ozgur/python-linkedin
Using a linkedin api already written.  See above linkedin

install is via pip: sudo pip install python-linkedin

"""
import BaseHTTPServer
import cgi
import requests
import json


class LinkedInHandler():

    def __init__(self):
        self.KEY = '77o0i7g6tnd1eb'
        self.SECRET = 'zYgn5AyIo7EL1UOz'
        self.RETURN_URL = 'http://localhost:8000'

    def get_user(self):
        auth_code = self.request_authentication()
        if auth_code.code is None:
            return None
        access_token = self.request_access_token(auth_code)
        if access_token is None:
            return None
        return self.get_profile(access_token)


    def build_request_string(self):
        return "https://www.linkedin.com/uas/oauth2/authorization?response_type=code&client_id=" + self.KEY + "&scope=r_fullprofile&state=1UXrL4PbYPVtYyowFAez&redirect_uri="+self.RETURN_URL

    def request_authentication(self):
        print self.build_request_string()
        auth_code = Token()
        self._wait_for_user_to_enter_browser(auth_code)
        return auth_code


    def get_profile(self, access_token):
        url = "https://api.linkedin.com/v1/people/~:(first-name,last-name,location,interests,languages,skills,educations,three_current_positions,three_past_positions,recommendations-received)?format=json"
        #url = "https://api.linkedin.com/v1/people/~:(skills)"
        payload = {'oauth2_access_token':access_token}
        r = requests.get(url, params=payload)
        try:
            return json.loads(r.text.encode('utf-8'))
        except:
            return None

    def request_access_token(self, auth_code):
        url = "https://www.linkedin.com/uas/oauth2/accessToken?grant_type=authorization_code"
        payload = {'code':auth_code.code, 'redirect_uri':self.RETURN_URL, 'client_id':self.KEY, 'client_secret':self.SECRET}
        r = requests.post(url, params=payload)
        try:
            return json.loads(r.text)['access_token']
        except:
            return None

    def _wait_for_user_to_enter_browser(self, auth_code):
        class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
            def do_GET(self):
                p = self.path.split('?')
                if len(p) > 1:
                    params = cgi.parse_qs(p[1], True, True)
                    try:
                        auth_code.set_token(params['code'][0])
                    except:
                        print "User does not want"

        server_address = ('', 8000)
        httpd = BaseHTTPServer.HTTPServer(server_address, MyHandler)
        httpd.handle_request()

class Token():

    def __init__(self):
        self.code = None

    def set_token(self, token):
        self.code = token

    def __str__(self):
        return self.code


if __name__ == "__main__":
    li = LinkedInHandler()
    print li.get_user()
