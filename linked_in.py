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

    def build_request_string(self):
        """
        Didn't think this could be done with the requests api.  As it involves user input in the browser.
        """
        return "https://www.linkedin.com/uas/oauth2/authorization?response_type=code&client_id=" + self.KEY + "&scope=r_fullprofile&state=1UXrL4PbYPVtYyowFAez&redirect_uri="+self.RETURN_URL

    def request_authentication(self):
        return self.build_request_string()

    def wait_for_auth(self):
        auth_code = Token()
        self._wait_for_user_to_enter_browser(auth_code)
        return auth_code


    def get_profile(self, access_token):
        """
        Wasn't sure how to pass the selectors with request so they are hard
        coded in.  These can change.
        """
        url = "https://api.linkedin.com/v1/people/~:(first-name,last-name,location,interests,languages,skills,educations,three_current_positions,three_past_positions,recommendations-received)?format=json"
        #url = "https://api.linkedin.com/v1/people/~:(skills)"
        payload = {'oauth2_access_token':access_token}
        r = requests.get(url, params=payload)
        try:
            return json.loads(r.text)
        except:
            return None

    def request_access_token(self, auth_code):
        """
        The access token is what lets us do stuff.  It expires after 60 days.
        For our purposes this isn't a problem.
        """
        url = "https://www.linkedin.com/uas/oauth2/accessToken?grant_type=authorization_code"
        payload = {'code':auth_code.code, 'redirect_uri':self.RETURN_URL, 'client_id':self.KEY, 'client_secret':self.SECRET}
        r = requests.post(url, params=payload)
        try:
            return json.loads(r.text)['access_token']
        except:
            return None

    def _wait_for_user_to_enter_browser(self, auth_code):
        """
        This is dirty, fire up a web server to listen for linkedin response.
        Can this be replaced with whatever is running on mikey's laptop
        """
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
    """
    This is a bullshit class to allow the authorisation code to be passed out of the server
    """
    def __init__(self):
        self.code = None

    def set_token(self, token):
        self.code = token

    def __str__(self):
        return self.code

class User():

    def __init__(self, profile_dict):
        self.profile_string = ""
        self.parse(profile_dict)

    def parse(self, profile):
        """
        LinkedIn API returns some arbitrarily nested dictionaries with lists
        or whatever in them.  This method recurses through that deciding what
        to do.  The base case of a 'primitive' is where we add it the out put
        string.  Using an instance variable to make coming up recursion much
        easier.
        """
        if type(profile) == list:
            for item in profile:
                self.parse(item)
        elif type(profile) == dict:
            for key, value in profile.items():
                self.parse(profile[key])
        elif type(profile) == tuple:
            for item in profile:
                self.parse(item)
        else:
            try:
                self.profile_string += profile.encode('utf-8', 'ignore') + "\n"
            except:
                pass

    def __str__(self):
        return self.profile_string

if __name__ == "__main__":
    li = LinkedInHandler()
    print li.request_authentication()
    auth_code = li.wait_for_auth()
    if auth_code.code is not None:
        access_token = li.request_access_token(auth_code)
        if access_token is not None:
            print li.get_profile(access_token)
