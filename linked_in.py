"""
https://github.com/ozgur/python-linkedin
Using a linkedin api already written.  See above linkedin

install is via pip: sudo pip install python-linkedin

"""
from linkedin import linkedin

class LinkedInHandler:

    def __init__(self):
        self.CONSUMER_KEY = '77o0i7g6tnd1eb'
        self.CONSUMER_SECRET = 'zYgn5AyIo7EL1UOz'
        self.USER_TOKEN = 'a18ee3a3-4363-4c77-9d68-ba9161a0e197'
        self.USER_SECRET = '46a8553c-c694-4943-809e-e22f75fbb189'
        self.RETURN_URL = 'http://localhost:8000'

    def request_authentication(self):
        authentication = linkedin.LinkedInDeveloperAuthentication(self.CONSUMER_KEY, self.CONSUMER_SECRET, self.USER_TOKEN, self.USER_SECRET, self.RETURN_URL, ['r_fullprofile'])
        application = linkedin.LinkedInApplication(authentication)
        return application

    def get_information(self, user):
        interesting_fields = ['first-name', 'last-name', 'location', 'interests', 'languages', 'skills', 'educations','three_current_positions', 'three_past_positions', 'recommendations-received']
        return user.get_profile(selectors=interesting_fields)

if __name__ == "__main__":
    li = LinkedInHandler()
    user_profile = li.request_authentication()
    info_dict = li.get_information(user_profile).items()
    print info_dict
