import jinja2,os,webapp2,urllib
from google.appengine.ext import ndb
import datetime

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class mUser(ndb.Model):
    username=ndb.StringProperty()
    password=ndb.StringProperty()

class DailyEntry(ndb.Model):
    username=ndb.StringProperty()
    TTime=ndb.DateTimeProperty(auto_now_add=True)
    type=ndb.StringProperty()
    d=ndb.StringProperty()
    m=ndb.StringProperty()
    y=ndb.StringProperty()
    ms=ndb.StringProperty()


class GlobalClass(webapp2.RequestHandler):
    user_login=''
    
class List(ndb.Model):
    list_name = ndb.StringProperty()
    list_username = ndb.StringProperty()

class Event(ndb.Model):
    event_name = ndb.StringProperty()
    associated_list = ndb.StringProperty()
    start_time = ndb.DateTimeProperty()
    end_time = ndb.DateTimeProperty()
        
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
                
class lout(webapp2.RequestHandler):
    def get(self):
        GlobalClass.user_login=''
        self.redirect('/')
        
class Attendance(webapp2.RequestHandler):
    def get(self):
        lusr=self.request.get('username')       
        print lusr
        template_values=dict()
        template_values['username']=lusr
        template = JINJA_ENVIRONMENT.get_template('Attendance.html')
        self.response.write(template.render(template_values))
    def post(self):
        typ=self.request.get('identifier')
        usr=self.request.get('username')
        print typ,usr
        if typ=='view':
            template_values=dict()
            template_values['username']=usr
            
            print usr
            iqresult=DailyEntry.query(DailyEntry.username==usr,DailyEntry.type=='In').order(-DailyEntry.ms)
#             template_values['iresult']=iqresult
            for i in iqresult:
                print i
            oqresult=DailyEntry.query(DailyEntry.username==usr,DailyEntry.type=='Out').order(-DailyEntry.ms)
            result = map(None,iqresult, oqresult)
            template_values['result']=result
            for i in oqresult:
                print i
            for i,j in result:
                print type(j.TTime-i.TTime)
            template = JINJA_ENVIRONMENT.get_template('ViewAttendance.html')
            self.response.write(template.render(template_values))
        elif typ=='entry':
            template_values=dict()
            template_values['username']=usr
            print usr
            template = JINJA_ENVIRONMENT.get_template('Enter.html')
            self.response.write(template.render(template_values))

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
#         event_name = self.request.get('event_name')
        template_values = dict()
        list_name = self.request.get('list_name')
        template_values['list_name'] = list_name
        
        event_query = Event.query()
        
        events = []
        
        for entry in event_query:
            if list_name == entry.associated_list:
                print entry.event_name
                print entry.start_time
                print entry.end_time
                events.append(entry)
                template_values['event_names'] = events
   
        template = JINJA_ENVIRONMENT.get_template('event_list.html')
        self.response.write(template.render(template_values))   
        
    def post(self):
        print 'events Post'
        event_name = self.request.get('event_name')
        usr = self.request.get('username')
        print event_name
        associated_list = self.request.get('list_name')
        st_date = self.request.get('start_date').split('-')
        st_date = map(int, st_date)
        
        st_time = self.request.get('start_time').split(':')
        st_time = map(int, st_time)
        st_date_part = datetime.datetime(st_date[0],st_date[1],st_date[2], st_time[0], st_time[1],0,0)
    
        starttime = st_date_part
        
        end_date = self.request.get('end_date').split('-')
        end_date = map(int, end_date)
        end_time = self.request.get('end_time').split(':')
        end_time = map(int, end_time)
        end_date_part = datetime.datetime(end_date[0], end_date[1],end_date[2], end_time[0], end_time[1], 0, 0)
        
        endtime = end_date_part
        
        event_element = Event(event_name = event_name, associated_list = associated_list, start_time = starttime, end_time = endtime)
        event_element.put()
        self.redirect('/tasks?username='+usr+'&list_name='+associated_list)

class InOut(webapp2.RequestHandler):
    def get(self):
        typ=self.request.get('type')
        lusr=self.request.get('username') 
        print typ,lusr
        if typ=='In':
            template_values=dict()
            template_values['username']=lusr
            template = JINJA_ENVIRONMENT.get_template('In.html')
            self.response.write(template.render(template_values))
        elif typ=='Out':
            template_values=dict()
            template_values['username']=lusr
            template = JINJA_ENVIRONMENT.get_template('Out.html')
            self.response.write(template.render(template_values))
    def post(self):
        typ=self.request.get('type')
        lusr=self.request.get('username')
        d=self.request.get('date')
        m=self.request.get('month')
        y= self.request.get('year')
        ms=self.request.get('time')
        print typ,lusr
        if typ=='In':
            de=DailyEntry(username=lusr,type=typ,d=d,m=m,y=y,ms=ms)
            de.put()
            query_params = {'username': lusr}
            self.redirect('/EnterData?'+ urllib.urlencode(query_params))
        elif typ=='Out':
            de=DailyEntry(username=lusr,type=typ,d=d,m=m,y=y,ms=ms)
            de.put()
            query_params = {'username': lusr}
            self.redirect('/EnterData?'+ urllib.urlencode(query_params))
            
app = webapp2.WSGIApplication([
    ('/', Login),
    ('/welcome',Welcome),
    ('/lout',lout),
    ('/signup',SignUp),
    ('/verifyLogin',Login),
    ('/attendance',Attendance),
    ('/Display',Attendance),
    ('/EnterData',Attendance),
    ('/In',InOut),
    ('/Out',InOut),
    ('/submitEntry',InOut),
    ('/gotonext',gotonext),
    ('/tasks', tasks) 
], debug=True)
               
