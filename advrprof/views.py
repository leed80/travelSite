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


#send new creation and editing to front end
@login_required
def prof(request):
  
  args = {}
  args['form'] = {'usernameedit': UsernameEdit(), 'email': EmailEdit(), 'first': FirstNameEdit(), 'last': LastNameEdit()}

  return render_to_response ('advrprof/profile.html', args, RequestContext(request))

@login_required
def username_edit(request):
  usernameedit = {}
  usernameedit.update(csrf(request))
  if request.method == 'POST':
    form = UsernameEdit(request.POST)
    usernameedit['form'] = form
    if form.is_valid():

      username = form.cleaned_data['username']

      current_user = request.user.id

      user = User.objects.get(id = current_user)
            
      user.username = username

      user.save()

      return redirect('advrprof.views.prof')



      
@login_required
def email_edit(request):
  email = {}
  email.update(csrf(request))
  if request.method == 'POST':
        form = EmailEdit(request.POST)
        email['form'] = form
        if form.is_valid():

          emailedit = form.cleaned_data['email']

          current_user = request.user.id

          user = User.objects.get(id = current_user)
            
          user.email = emailedit

          user.save()

          return redirect('advrprof.views.prof')
@login_required
def desc_edit(request):
  descedit = {}
  descedit.update(csrf(request))
  if request.method == 'POST':
        form = DescEdit(request.POST)
        descedit['form'] = form
        if form.is_valid():
          descedit = form.cleaned_data['description']

          current_user = request.user.id

          user = User.objects.get(id = current_user)
            
          user.desc = descedit

          user.save()

          return redirect('advrprof.views.prof')
          
@login_required
def first_name_edit(request):
  first = {}
  first.update(csrf(request))
  if request.method == 'POST':
        form = FirstNameEdit(request.POST)
        first['form'] = form
        if form.is_valid():

          first = form.cleaned_data['first_name']

          current_user = request.user.id

          user = User.objects.get(id = current_user)
            
          user.first_name = first

          user.save()

          return redirect('advrprof.views.prof')

@login_required
def last_name_edit(request):
  last = {}
  last.update(csrf(request))
  if request.method == 'POST':
        form = LastNameEdit(request.POST)
        last['form'] = form
        if form.is_valid():
          last = form.cleaned_data['last_name']

          current_user = request.user.id

          user = User.objects.get(id = current_user)
            
          user.last_name = last

          user.save()

          return redirect('advrprof.views.prof')

@login_required
def deleteProfile(request):
  current_user = request.user.id

  user = User.objects.get(id = current_user)

  user.delete()

  deleted = 'deleted'

  args = {'deleted': deleted}

  return render_to_response('homepage/home.html', args, RequestContext(request))

  












