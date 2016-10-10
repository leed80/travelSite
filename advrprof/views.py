from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404, HttpResponse, redirect
from django.template import RequestContext
from advrprof import forms
from django.views.decorators import csrf
from forms import *
from django import forms
from reg import models


# This is the view for displaying and editing user details in the profile area of the site.
@login_required
def profile(request):
  
  args = {}
  args['form'] = {'usernameedit': UsernameEdit(), 'email': EmailEdit(), 'first': FirstNameEdit(), 'last': LastNameEdit()}

  return render_to_response ('advrprof/profile.html', args, RequestContext(request))

# This is the view for editing the username
@login_required
def username_edit(request):
  usernameedit = {}
  usernameedit.update(csrf(request))
  if request.method == 'POST':
    form = UsernameEdit(request.POST)
    usernameedit['form'] = form
    if form.is_valid():
      username = form.cleaned_data['username']
      user = getUser()  
      user.username = username
      user.save()

      return redirect('advrprof.views.prof')



# This is the view for editing the email
@login_required
def email_edit(request):
  email = {}
  email.update(csrf(request))
  if request.method == 'POST':
        form = EmailEdit(request.POST)
        email['form'] = form
        if form.is_valid():
          emailedit = form.cleaned_data['email']
          user = getUser()    
          user.email = emailedit
          user.save()

          return redirect('advrprof.views.prof')

# This is the view for editing the first name         
@login_required
def first_name_edit(request):
  first = {}
  first.update(csrf(request))
  if request.method == 'POST':
        form = FirstNameEdit(request.POST)
        first['form'] = form
        if form.is_valid():
          first = form.cleaned_data['first_name']
          user = getUser()    
          user.first_name = first
          user.save()

          return redirect('advrprof.views.prof')

# This is the view for editing the last name
@login_required
def last_name_edit(request):
  last = {}
  last.update(csrf(request))
  if request.method == 'POST':
        form = LastNameEdit(request.POST)
        last['form'] = form
        if form.is_valid():
          last = form.cleaned_data['last_name']
          user = getUser()     
          user.last_name = last
          user.save()

          return redirect('advrprof.views.prof')

# This is the view for deleting the user
@login_required
def deleteProfile(request):
  user = getUser()  
  user.delete()
  deleted = 'deleted'
  args = {'deleted': deleted}

  return render_to_response('homepage/home.html', args, RequestContext(request))

  

# This is the function to get the current user
def getUser():
  current_user = request.user.id
  user = User.objects.get(id = current_user)
  return user










