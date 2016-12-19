from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404, HttpResponse, redirect, HttpResponseRedirect
from django.template import RequestContext
from userProfile import forms
from django.views.decorators import csrf
from forms import *
from django import forms
from models import *
import hashlib
import random
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail



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

      return redirect('userProfile.views.prof')



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

          return redirect('userProfile.views.prof')

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

          return redirect('userProfile.views.prof')

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

          return redirect('userProfile.views.prof')

# This is the view for deleting the user
@login_required
def deleteProfile(request):
  user = getUser(request)  
  user.delete()
  userDeleted = 'User deleted'
  deleteMessage = {'deleted': userDeleted}

  return render_to_response('homepage/home.html', deleteMessage, RequestContext(request))

  

# This is the function to get the current user
def getUser(request):
  current_user = request.user.id
  user = User.objects.get(id = current_user)
  return user


#------------------- reg ----------------------------------------------


def register_user(request):
    registerDetails = {}
    if request.method == 'POST':
        # Register the user
        registrationProcess(request)
    else:
        # Send to the registration page with the registration form
        registerDetails['form'] = RegistrationForm()

    return render_to_response('reg/reg.html', registerDetails, context_instance=RequestContext(request))

def registrationProcess(request):
    # This is the main user registration process
    completeRegistrationForm = RegistrationForm(request.POST)
    if completeRegistrationForm.is_valid(): 
        completeRegistrationForm.save()  # save user to the main django User database table if form is valid

        # Start the process of adding the user to the user profile database table

        # Gather cleaned form data
        username, userEmail, country, address, postcode, password = cleanFormData(completeRegistrationForm)

        # Create an activation key
        activationKey = activationSalt(userEmail)

        # Set user as unconfimed           
        status = "unconfirmed"

        # Get user by username
        user = User.objects.get(username=username)

        # Save the new user profile
        saveNewUserProfile(user, activationKey, status, country, address, postcode)

        # authenticate and login the new user
        authenticateLogin(username, password, request)

        # Create and send the activation email
        activationEmail(username, activationKey, userEmail)

        # Return the user to the registration success page
        return HttpResponseRedirect('/userProfile/success')
    else:
        print 'This is not valid'

def activationEmail(username, activationKey, userEmail):
    # Create activation email subject and body
    emailSubject = 'The Adventurer account confirmation'
    emailBody = 'Hey %s,\n\n Thanks for signing up for The Adventurer. Please click the following link to activate your account: \n\n http://127.0.0.1:8000/reg/confirm/?username=%s&activation_key=%s \n\nThanks\n\n' % (username, username, activationKey)

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
    password=form.cleaned_data['password1']

    return (username, userEmail, country, address, postcode, password)


def authenticateLogin(username, password, request):
    # Authenticate and login the new user
    newUser = authenticate(username=username, password=password)
    login(request, newUser)

@login_required
def confirm(request):
    # This is the view for confirming the users activation key and changing their profile status to 'confirmed'

    # Get the activation key
    sentActivationKey = request.GET['activation_key']

    # Get the stored activation key
    storedActivationKey = storedActivationKey(request)

    if storedActivationKey == sentActivationKey:
        # If the two keys are the same then change profile status to confirmed, save and send to the confirmed account page
        profile.status = 'confirmed'
        profile.save()

        return render_to_response("reg/confirm.html", context_instance=RequestContext(request))
    else:
        # Send the error message that the sent key is wrong
        return HttpResponse('The activation key is wrong. Please try again or contact support')

def storedActivationKey(request):
    # Function for retricing the activation key stored on user proile

    # Get the current user
    current_user = request.user
    username = current_user.username

    # Get the user profile
    profile = UserProfile.objects.get(username=username)
    # Get the stored activation key
    storedActivationKey = profile.activation_key

    return storedActivationKey

  
def success(request):
    # This is the view for returning the page for successful registration
    return render_to_response('reg/register_success.html')
  
def user_login(request):
    # The view for logging the user in

    # Check the sent details are correct. If the user is already authenticated then send them to their profile page
    if request.user.is_authenticated():
        return render_to_response('advrprof/profile.html', RequestContext(request))
    else:
        # Get the context data for the users request
        context = RequestContext(request)

        # Check for POST method
        if request.method == 'POST':

            user = authenticateUser(request)

            # If user is correct then login and send to profile page
            if user:
                login(request, user)
                return HttpResponseRedirect('userProfile/profile/')
            else:
                # The wrong login details were provided
                invalid = 'yes'
                args = {'invalid': invalid}
                return render_to_response('reg/login.html', args, RequestContext(request))
        else:
            # POST was not used to return to login form
            return render_to_response('reg/login.html', {}, context)

def authenticateUser(request):
    # Get username and password and authenticate user
    username = request.POST['username']
    password = request.POST['password']

    # Use the django authenticate function with the username and password given
    user = authenticate(username=username, password=password)
    return user

          
@login_required
def user_logout(request):
    # Use the djngo logout function to log the current user out and return to homepage
    logout(request)

    return render_to_response('homepage/home.html')






