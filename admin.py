#coding:utf-8
import wsgiref.handlers 
import os
from functools import wraps
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
import methods,logging
import imahecompare

class AdminControl(webapp.RequestHandler):
    def render(self,template_file,template_value):
        path=os.path.join(os.path.dirname(__file__),template_file)
        self.response.out.write(template.render(path, template_value))
    def returnjson(self,dit):
        self.response.headers['Content-Type'] = "application/json"
        self.response.out.write(simplejson.dumps(dit))

class Admin_Upload(AdminControl):
    def get(self):
        self.render('views/upload.html', {})
    
    def post(self):
        bf=self.request.get("file")
        if not bf:
            return self.redirect('/admin/upload/')
        name=self.request.body_file.vars['file'].filename
        mime = self.request.body_file.vars['file'].headers['content-type']
        if mime.find('image')==-1:
             return self.redirect('/admin/upload/')
        description=self.request.get("description")
        image=methods.addImage( mime, description, bf, name)
        
        self.redirect('/show/%s/' %image.id)

    
class Find(AdminControl):
    def get(self):
        self.render('views/find.html', {})
        
    def post(self):
        PixelCompare(im1, im2, mode = "pct", alpha = .01):
        bf=self.request.get("file")
        if not bf:
            return self.redirect('/admin/find/')
        name=self.request.body_file.vars['file'].filename
        mime = self.request.body_file.vars['file'].headers['content-type']
        if mime.find('image')==-1:
             return self.redirect('/admin/find/')
        description=self.request.get("description")
        image=methods.addImage( mime, description, bf, name)
        
        self.redirect('/gshow/%s/' %image.id)
            
class Delete_Image(AdminControl):

    def get(self,key):
        methods.delImage(key)
        self.redirect('/')
    

    
application = webapp.WSGIApplication(
                                       [(r'/admin/upload/', Admin_Upload),
                                        (r'/admin/find/', Find),
                                        (r'/admin/del/(?P<key>[a-z,A-Z,0-9]+)', Delete_Image),
                                       ], debug=True)
wsgiref.handlers.CGIHandler().run(application)

