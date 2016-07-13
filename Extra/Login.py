import jinja2
import webapp2
import os
from google.appengine.ext import ndb
from webapp2_extras import sessions,auth
import webapp2_extras.appengine.auth.models
from __builtin__ import None

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# class User(webapp2_extras.appengine.auth.models.User):
#     username=ndb.StringProperty()

config = {
  'webapp2_extras.auth': {
    'User': 'models.User',
    'user_attributes': ['user_name']
  },
  'webapp2_extras.sessions': {
    'secret_key': 'YOUR_SECRET_KEY'
  }
}

# class User(webapp2_extras.appengine.auth.models.User):
#     def set_password(self, raw_password):
#         self.password = security.generate_password_hash(raw_password, length=12)
#     @classmethod
#     def get_by_auth_token(cls, user_id, token, subject='auth'):
#         token_key = cls.token_model.get_key(user_id, subject, token)
#         user_key = ndb.Key(cls, user_id)
#     # Use get_multi() to save a RPC call.
#         valid_token, user = ndb.get_multi([token_key, user_key])
#         if valid_token and user:
#             timestamp = int(time.mktime(valid_token.created.timetuple()))
#             return user, timestamp
#  
#     return None, None  
    

class BaseHandler(webapp2.RequestHandler):
    pass
#     @webapp2.cached_property
#     def auth(self):
#         """Shortcut to access the auth instance as a property."""
#         return auth.get_auth()
#     
#     @webapp2.cached_property
#     def user_info(self):
#         return self.auth.get_user_by_session()
#     @webapp2.cached_property
#     def user(self):
#         u = self.user_info
#         return self.user_model.get_by_id(u['user_id']) if u else None
#    
#     @webapp2.cached_property
#     def user_model(self):
#        return self.auth.store.user_model
#     
#     @webapp2.cached_property
#     def session(self):
#         """Shortcut to access the current session."""
#         return self.session_store.get_session(backend="datastore")
#     
#     def render_template(self, view_filename, params={}):
#         user = self.user_info
#         params['user'] = user
#         path = os.path.join(os.path.dirname(__file__), 'views', view_filename)
#         self.response.out.write(template.render(path, params))
#  
#   def display_message(self, message):
#     """Utility function to display a template with a simple message."""
#     params = {
#       'message': message
#     }
#     self.render_template('message.html', params)
#  
#   # this is needed for webapp2 sessions to work
#   def dispatch(self):
#       # Get a session store for this request.
#       self.session_store = sessions.get_store(request=self.request)
#  
#       try:
#           # Dispatch the request.
#           webapp2.RequestHandler.dispatch(self)
#       finally:
#           # Save all sessions.
#           self.session_store.save_sessions(self.response)
#     @webapp2.cached_property
#     def session_store(self):
#         return sessions.get_store(request=self.request)
#     @webapp2.cached_property
#     def session(self):
#         return self.session_store.get_session(backend="datastore")
#     
#     def dispatch(self):        
#         try:
#             super(BaseHandler, self).dispatch()
#         finally:
#             # Save the session after each request        
#             self.session_store.save_sessions(self.response)
# 
#     @webapp2.cached_property
#     def auth(self):
#         return auth.get_auth(request=self.request)
#     
#     @webapp2.cached_property
#     def user(self):
#         user = self.auth.get_user_by_session()
#         return user
    
#     @webapp2.cached_property
#     def user_model(self):
#         user_model, timestamp = 
#             self.auth.store.user_model.get_by_auth_token(
#                 self.user['username'], 
#                 self.user['token']) if self.user else (None, None)
#         return user_model
class SignUp(BaseHandler):
    def get(self):
        template_values=dict()
        template = JINJA_ENVIRONMENT.get_template('signup.html')
        self.response.write(template.render(template_values))
    
    def post(self):
        user_name=self.request.get('username')
        password=self.request.get('password')
        
        unique_property=['username']
        user_data=self.user_model.create_user(user_name,unique_property,username=user_name,password_raw=password,verified=False)
        if not user_data[0]:
            print "Unable to create user"
        
        

class LoginPage(webapp2.RequestHandler):
    def get(self):
        template_values=dict()
        template = JINJA_ENVIRONMENT.get_template('login.html')
        self.response.write(template.render(template_values))
        

#app = webapp2.WSGIApplication([('/', LoginPage),], debug=True)
