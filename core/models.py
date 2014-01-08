from google.appengine.ext import ndb

class Blog(ndb.Model):
    blog_name = ndb.StringProperty()
    blog_content = ndb.StringProperty()
