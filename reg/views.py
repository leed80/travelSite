from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.views.decorators import csrf
from forms import *
from models import *
from django.template import RequestContext
from django.core.mail import send_mail
import hashlib, datetime, random
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render
import urllib2, urllib


def register_user(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        args['form'] = form
        if form.is_valid(): 
            form.save()  # save user to database if form is valid

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]            
            activation_key = hashlib.sha1(salt+email).hexdigest()            
            status = "unconfirmed"
            country = form.cleaned_data['country']
            address = form.cleaned_data['address']
            postcode = form.cleaned_data['postcode']


            #Get user by username
            user=User.objects.get(username=username)

            # Create and save user profile                                                                                                                                  
            new_profile = UserProfile(user=user, activation_key=activation_key, status=status, country = country, address = address, postcode = postcode)
            new_profile.save()

            new_user = authenticate(username=username, password=form.cleaned_data['password1'])
            login(request, new_user)

            # Send email with activation key
            email_subject = 'The Adventurer account confirmation'
            email_body = 'Hey %s,\n\n Thanks for signing up for The Adventurer. Please click the following link to activate your account: \n\n http://127.0.0.1:8000/reg/confirm/?username=%s&activation_key=%s \n\nThanks\n\nThe Adventurer Team' % (username, username, activation_key)

            send_mail(email_subject, email_body, 'no-reply@theadvr.com',
                [email], fail_silently=False)

            

            return HttpResponseRedirect('/reg/success')
    else:
        args['form'] = RegistrationForm()

    return render_to_response('reg/reg.html', args, context_instance=RequestContext(request))


def confirm(request):
    activation_key = request.GET['activation_key']

    print 'activation_key is %s' % (activation_key)

    profile = UserProfile.objects.get(activation_key=activation_key)
    profile.status = 'confirmed'

    profile.save()

    return render_to_response("reg/confirm.html", context_instance=RequestContext(request))



  
def success(request):
    return render_to_response('reg/register_success.html')
  
def user_login(request):

    if request.user.is_authenticated():
        return render_to_response('advrprof/profile.html', RequestContext(request))
    else:
        # Like before, obtain the context for the user's request.
        context = RequestContext(request)

        # If the request is a HTTP POST, try to pull out the relevant information.
        if request.method == 'POST':
            # Gather the username and password provided by the user.
            # This information is obtained from the login form.
            username = request.POST['username']
            password = request.POST['password']

            # Use Django's machinery to attempt to see if the username/password
            # combination is valid - a User object is returned if it is.
            user = authenticate(username=username, password=password)

            # If we have a User object, the details are correct.
            # If None (Python's way of representing the absence of a value), no user
            # with matching credentials was found.
            if user:
                # Is the account active? It could have been disabled.
                if user.is_active:
                    # If the account is valid and active, we can log the user in.
                    # We'll send the user back to the homepage.
                    login(request, user)
                    return HttpResponseRedirect('/profile/')
                else:
                    # An inactive account was used - no logging in!
                    return HttpResponse("Your account is disabled.")
            else:
                # Bad login details were provided. So we can't log the user in.
                print "Invalid login details: {0}, {1}".format(username, password)
                invalid = 'yes'
                args = {'invalid': invalid}
                return render_to_response('reg/login.html', args, RequestContext(request))

        # The request is not a HTTP POST, so display the login form.
        # This scenario would most likely be a HTTP GET.
        else:
            # No context variables to pass to the template system, hence the
            # blank dictionary object...
            return render_to_response('reg/login.html', {}, context)
          
# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return render_to_response('homepage/home.html')