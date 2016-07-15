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
    
class List(ndb.Model):
    list_name = ndb.StringProperty()
    list_username = ndb.StringProperty()

class Event(ndb.Model):
    event_name = ndb.StringProperty()
    associated_list = ndb.StringProperty()
        
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
            self.redirect('/')
            print 'f'
        #print muserKey[username]
        else:
            print 'p'
            self.redirect('/signup')
        
class Welcome(webapp2.RequestHandler):
    def get(self):
        
        lusr=self.request.get('username')
        template_values=dict()
        template_values['username']=lusr
        template = JINJA_ENVIRONMENT.get_template('Welcome.html')
        self.response.write(template.render(template_values))
        print lusr
        
class getusernametemp(webapp2.RequestHandler):
    def get(self):
        print "get-username"
        template_values=dict()
        template_values['username']="luser"
        template = JINJA_ENVIRONMENT.get_template('get-username.html')
        self.response.write(template.render(template_values))
        
class lout(webapp2.RequestHandler):
    def get(self):
        GlobalClass.user_login=''
        self.redirect('/')
        
class gotonext(webapp2.RequestHandler):
    def get(self):
        usr = self.request.get('username')
        template_values = dict()
        template_values['username'] = usr
        
        list_query = List.query()
        
        arr = []
        
        for entry in list_query:
            print entry.list_name
            if (usr == entry.list_username):
                arr.append(entry.list_name)
                template_values['list_names'] = arr
            
        template = JINJA_ENVIRONMENT.get_template('task_list.html')
        self.response.write(template.render(template_values))   
        
    def post(self):
        print 'gotonext Post'
        usr = self.request.get('username')
        listname=self.request.get('list_name')
        print usr
        print listname
        if listname == '':
            listname = "Default_List"
            
        list_element = List(list_name = listname, list_username = usr)
        list_element.put()
        print 'redirected'
        self.redirect('/gotonext?username='+usr)
        
class tasks(webapp2.RequestHandler):
    def get(self):
        event_name = self.request.get('event_name')
        template_values = dict()
        list_name = self.request.get('list_name')
        template_values['list_name'] = list_name
        
        event_query = Event.query()
        
        arr = []
        
        for entry in event_query:
            if list_name == entry.associated_list:
                print entry.event_name
                arr.append(entry.event_name)
                template_values['list_names'] = arr
   
        template = JINJA_ENVIRONMENT.get_template('event_list.html')
        self.response.write(template.render(template_values))   
        
    def post(self):
        print 'events Post'
        event_name = self.request.get('event_name')
        usr = self.request.get('username')
        print event_name
        associated_list = self.request.get('list_name')
            
        event_element = Event(event_name = event_name, associated_list = associated_list)
        event_element.put()
        self.redirect('/tasks?username='+usr+'&list_name='+associated_list)

app = webapp2.WSGIApplication([
    ('/', Login),
    ('/welcome',Welcome),
    ('/lout',lout),
    ('/signup',SignUp),
    ('/verifyLogin',Login),
    ('/getusernametemp',getusernametemp),
    ('/gotonext',gotonext),
    ('/tasks', tasks) 
], debug=True)
               
