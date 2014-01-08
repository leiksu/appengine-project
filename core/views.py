from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import Context, RequestContext
from django.template.loader import get_template

from models import Blog
from forms import  BlogForm

from google.appengine.ext import ndb

from django.shortcuts import get_object_or_404, render_to_response, render, redirect
from django.http import HttpResponseRedirect

from django.core.cache import cache
from django.core.urlresolvers import reverse

from google.appengine.api import users

# function that creates/edit blog    
def create_blog(request, id=False):
    if request.method == 'POST': # If the form has been submitted...
        form = BlogForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
           
            blog_id = int(request.POST['blog_id'])
            blog_name = form.cleaned_data['blog_name']
            blog_content = form.cleaned_data['blog_content']
            
            if blog_id == False:
                # Create blog entity
                blog_item = Blog(
                                 blog_name=blog_name,
                                 blog_content=blog_content)
            else:
                # retrieve existing blog entity
                blog_item = ndb.Key(Blog, blog_id).get()
          
                # update existing blog entity
                blog_item.blog_name = blog_name
                blog_item.blog_content = blog_content 
                
            # save request changes
            blog_item_key = blog_item.put()

            # redirect
            return HttpResponseRedirect('/blog') # Redirect after POST
    else:
        if id == False:
            # initialize form that creates form 
            form = BlogForm() # An unbound form
        else:
            # fetch the blog item based on the given id
            key = ndb.Key(Blog, int(id))
            selected_blog = key.get()
            
            # initialize form that edits form
            form = BlogForm(initial={
                                     'blog_name': selected_blog.blog_name,
                                     'blog_content': selected_blog.blog_content
                                      })

    # produce var for template
    variables = RequestContext(request, {
                                         'form' : form,
                                         'blog_id': int(id)                                                                                
                                         })
    
    return render_to_response( 'create_blog.html', variables )

# function that views blogs 
def view_blog(request, id=0):
    template = get_template("view_blog.html")
    posts = Blog.query()
    
    user = users.get_current_user()
    if user:
        variables = Context(
                           {'system_name' : id,
                            'posts': posts,
                            'nickname': user.nickname(),
                            'logout_url': users.create_logout_url('/blog')
                           })
    else:  
        variables = Context(
                            {'posts': posts,
                             'login_url': users.create_login_url('/blog')
                            })
        
        
    output = template.render(variables)
    return HttpResponse(output)

# function that deletes blog 
def delete_blog(request, id):
    key = ndb.Key(Blog, int(id))
    
    key.delete()
    return HttpResponseRedirect('/blog')

# original hello world part
class HelloWorld(TemplateView):
    template_name = "hello-world.html"

    def get_context_data(self, **kwargs):
        context = super(HelloWorld, self).get_context_data(**kwargs)
        self.request.session['test'] = 'val'
        context['session_test'] = self.request.session['test']
        return context

hello_world = HelloWorld.as_view()