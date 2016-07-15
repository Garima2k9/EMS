import jinja2,os,webapp2,urllib
from google.appengine.ext import ndb


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class mUser(ndb.Model):
    un = ndb.StringProperty(Indexed = False)
 
class gotonext(webapp2.RequestHandler):
    def get(self):
        
        un=self.request.get('username')
        template_values=dict()
        template_values['username']=un
        print un
        template = JINJA_ENVIRONMENT.get_template('task_list.html')
        self.response.write(template.render(template_values))
        
app = webapp2.WSGIApplication([
    ('/gotonext', gotonext)
], debug=True)