import jinja2
import webapp2
import os
from google.appengine.ext import ndb
from webapp2_extras import sessions,auth
import webapp2_extras.appengine.auth.models 


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# class User(webapp2_extras.appengine.auth.models.User):
#     username=ndb.StringProperty()

config = {
  'webapp2_extras.auth': {
    'user_model': 'User',
    'user_attributes': ['user_name']
  },
  'webapp2_extras.sessions': {
    'secret_key': 'YOUR_SECRET_KEY'
  }
}

class mUser(webapp2_extras.appengine.auth.models.User):
    pass 
    

class BaseHandler(webapp2.RequestHandler):
    user=None
#     def session_store(self):
#         return sessions.get_store(request=self.request)
    
    def session(self):
        return self.session_store.get_session(backend='datastore')
    
    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)
        try:
            super(BaseHandler,self).dispatch()
        finally:
            self.session_store.save_sessions(self.response)
    
    def auth(self):
        self.auth=auth.get_auth(request=self.request)
        return self.auth
        
    def user(self):
        user=self.auth.get_user_by_session()
        return user
    
    def user_model(self):
        user_model, timestamp =self.auth.store.user_model.get_by_auth_token(self.user['user_id'],self.user['token']) if self.user else (None, None) 
        return user_model
    
class SignUp(BaseHandler):
    def get(self):
        print 'Hello'
        template_values=dict()
        template = JINJA_ENVIRONMENT.get_template('signup.html')
        self.response.write(template.render(template_values))
    
    def post(self):
        user_name=self.request.get('username')
        password=self.request.get('password')
        print user_name,password,self.auth
        success, info = self.auth.store.user_model.create_user(
                "auth:" + user_name,
                unique_properties=['user_name'],
                user_name=user_name,
                password_raw= password)
#         unique_property=['username']
#         if success:
#                 self.auth.get_user_by_password("auth:"+user_name,password)
#                 return self.redirect_to("home")
#         else:
#                 error = "That username is already in use." if 'user_name' in self.user else "Something has gone horrible wrong."
#          
        

# class LoginPage(webapp2.RequestHandler):
#     def get(self):
#         template_values=dict()
#         template = JINJA_ENVIRONMENT.get_template('login.html')
#         self.response.write(template.render(template_values))
        

app = webapp2.WSGIApplication([('/', SignUp),], debug=True,config=config)
