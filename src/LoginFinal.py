import jinja2,os,webapp2,urllib
from google.appengine.ext import ndb


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class mUser(ndb.Model):
    username=ndb.StringProperty()
    password=ndb.StringProperty()

class GlobalClass(webapp2.RequestHandler):
    user_login=''
       

class Login(webapp2.RequestHandler):
    def get(self):
        #import pdb;pdb.set_trace()
        print 'LoginGet'
        #status,lu=self.check_User()
        print GlobalClass.user_login
        if GlobalClass.user_login=='':
            
            template_values=dict()
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
        else:
            print 'Login Get Else'
            query_params = {'username': GlobalClass.user_login}
            self.redirect('/welcome?'+ urllib.urlencode(query_params))
            
    def post(self):
        print 'Login Post'
        usrname=self.request.get('username')
        paswrd=self.request.get('password')
        qresult=mUser.query(mUser.username==usrname,mUser.password==paswrd)
        print qresult.count()
        
        for i in qresult:
            print i
        if qresult.count()!=0:
            print qresult
            GlobalClass.user_login=usrname
            print 'in if', GlobalClass.user_login
        else:
            print 'Error'
        self.redirect('/')    
        
class SignUp(webapp2.RequestHandler):
    def get(self):
        template_values=dict()
        template = JINJA_ENVIRONMENT.get_template('signup.html')
        self.response.write(template.render(template_values))
        
    def post(self):
        print 'Login Post'
        usrname=self.request.get('username')
        paswrd=self.request.get('password')
        qresult=mUser.query(mUser.username==usrname)
        if qresult.count()==0:
            GlobalClass.user_login=usrname
            muserKey=mUser(username=usrname,password=paswrd)
            muserKey.put()
        #print muserKey[username]
        self.redirect('/signup')
        
class Welcome(webapp2.RequestHandler):
    def get(self):
        
        lusr=self.request.get('username')
        template_values=dict()
        template_values['username']=lusr
        template = JINJA_ENVIRONMENT.get_template('Welcome.html')
        self.response.write(template.render(template_values))
        print lusr

class lout(webapp2.RequestHandler):
    def get(self):
        GlobalClass.user_login=''
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', Login),
    ('/welcome.*',Welcome),
    ('/lout',lout),
    ('/signup',SignUp),
    ('/verifyLogin',Login)
], debug=True)
               
