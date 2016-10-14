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
    registerDetails = {}
    #registerDetails.update(csrf(request))
    # If request is not POST then send forms
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        registerDetails['form'] = form
        if form.is_valid(): 
            form.save()  # save user to database if form is valid

            # Gather cleaned form data
            username, userEmail, country, address, postcode = cleanFormData(form)

            # Create an activattion key
            activationKey = activationSalt(userEmail)

            # Set user as unconfimed           
            status = "unconfirmed"

            #Get user by username
            user = User.objects.get(username=username)

            # Save the new user profile
            saveNewUserProfile(user, activationKey, status, country, address, postcode)

            # authenticate and login the new user
            authenticateLogin(username, password=form.cleaned_data['password1'])

            # Create and send the activation email
            activationEmail(username, activationKey, userEmail)

            return HttpResponseRedirect('/reg/success')
    else:
        registerDetails['form'] = RegistrationForm()

    return render_to_response('reg/reg.html', registerDetails, context_instance=RequestContext(request))

def acivationEmail(username, activationKey, userEmail):
    # Create activation email subject and body
    emailSubject = 'The Adventurer account confirmation'
    emailBody = 'Hey %s,\n\n Thanks for signing up for The Adventurer. Please click the following link to activate your account: \n\n http://127.0.0.1:8000/reg/confirm/?username=%s&activation_key=%s \n\nThanks\n\nThe Adventurer Team' % (username, username, activationKey)

    # send the email using the above subject and body to the user supplied details
    send_mail(emailSubject, emailBody, 'no-reply@theadvr.com',
        [userEmail], fail_silently=False)

def activationSalt(userEmail):
    # Using the sha1 FIPS secure hash algorith on a randomly generated float thats been converted 
    # to a string. Digesting the hash in hexidecimal from index 0 to, but not including index 5
    activationSalt = hashlib.sha1(str(random.random())).hexdigest()[:5]  

    # Create an activation key using the above salt and the user email using 
    # the sha1 hash algortith digested in hexidecimal form          
    activationKey = hashlib.sha1(activationSalt+userEmail).hexdigest() 

    return activationKey

def saveNewUserProfile(user, activationKey, status, country, address, postcode):
    # Create and save new user profile                                                                                                                                  
    new_profile = UserProfile(user=user, activation_key=activationKey, status=status, country = country, address = address, postcode = postcode)
    new_profile.save()

def cleanFormData(form):
    # Clean user data and assign variables
    username = form.cleaned_data['username']
    userEmail = form.cleaned_data['email']
    country = form.cleaned_data['country']
    address = form.cleaned_data['address']
    postcode = form.cleaned_data['postcode']

    return (username, userEmail, country, address, postcode)


def authenticateLogin(username, password):
    # Authenticate and login the new user
    newUser = authenticate(username=username, password=form.cleaned_data['password1'])
    login(request, newUser)

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