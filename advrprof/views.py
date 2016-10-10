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
  
  userInformation = {}
  userInformation['form'] = {'usernameedit': UsernameEdit(), 'email': EmailEdit(), 'first': FirstNameEdit(), 'last': LastNameEdit()}

  return render_to_response ('advrprof/profile.html', userInformation, RequestContext(request))

# This is the view for editing the username
@login_required
def usernameEdit(request):
  usernameEdit = {}
  usernameEdit.update(csrf(request))
  if request.method == 'POST':
    form = UsernameEdit(request.POST)
    usernameEdit['form'] = form
    if form.is_valid():
      usernameEdit = form.cleaned_data['username']
      user = getUser()  
      user.username = usernameEdit
      user.save()

      return redirect('advrprof.views.prof')



# This is the view for editing the email
@login_required
def emailEdit(request):
  emailEdit = {}
  emailEdit.update(csrf(request))
  if request.method == 'POST':
        form = EmailEdit(request.POST)
        emailEdit['form'] = form
        if form.is_valid():
          emailEdit = form.cleaned_data['email']
          user = getUser()    
          user.email = emailEdit
          user.save()

          return redirect('advrprof.views.prof')

# This is the view for editing the first name         
@login_required
def firstNameEdit(request):
  firstName = {}
  firstName.update(csrf(request))
  if request.method == 'POST':
        form = FirstNameEdit(request.POST)
        firstName['form'] = form
        if form.is_valid():
          firstNameEdit = form.cleaned_data['first_name']
          user = getUser()    
          user.first_name = firstNameEdit
          user.save()

          return redirect('advrprof.views.prof')

# This is the view for editing the last name
@login_required
def lastNameEdit(request):
  lastName = {}
  lastName.update(csrf(request))
  if request.method == 'POST':
        form = LastNameEdit(request.POST)
        lastName['form'] = form
        if form.is_valid():
          lastNameEdit = form.cleaned_data['last_name']
          user = getUser()     
          user.last_name = lastNameEdit
          user.save()

          return redirect('advrprof.views.prof')

# This is the view for deleting the user
@login_required
def deleteProfile(request):
  user = getUser()  
  user.delete()
  userDeleted = 'User deleted'
  deleteMessage = {'deleted': userDeleted}

  return render_to_response('homepage/home.html', deleteMessage, RequestContext(request))

  

# This is the function to get the current user
def getUser():
  current_user = request.user.id
  user = User.objects.get(id = current_user)
  return user










