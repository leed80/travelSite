import hashlib
import random

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail


def get_form_data(request):
    username = request.POST['username']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    password = request.POST['password']
    email = request.POST['email']
    country = request.POST['country']

    reg_args = [username, first_name, last_name, password, email, country]

    return reg_args


def getUser(request):
  current_user = request.user.id
  user = User.objects.get(id = current_user)
  return user


def activationEmail(username, activationKey, userEmail):
    # Create activation email subject and body
    emailSubject = 'The Adventurer account confirmation'
    emailBody = 'Hey %s,\n\n Thanks for signing up for The Adventurer. Please click the following link to activate your account: \n\n http://127.0.0.1:8000/user_profile/confirm/?activation_key=%s \n\nThanks\n\n' % (username, activationKey)

    # send the email using the above subject and body to the user supplied details
    send_mail(emailSubject, emailBody, 'no-reply@theadvr.com',
        [userEmail], fail_silently=False)


def activation_salt(userEmail):
    # Using the sha1 FIPS secure hash algorith on a randomly generated float thats been converted
    # to a string. Digesting the hash in hexidecimal from index 0 to, but not including index 5
    activationSalt = hashlib.sha1(str(random.random())).hexdigest()[:5]

    # Create an activation key using the above salt and the user email using
    # the sha1 hash algortith digested in hexidecimal form
    activationKey = hashlib.sha1(activationSalt+userEmail).hexdigest()

    return activationKey


def authenticate_user(request):
    # Get username and password and authenticate user
    username = request.POST['username']
    password = request.POST['password']

    # Use the django authenticate function with the username and password given
    user = authenticate(username=username, password=password)
    return user


def authenticateLogin(username, password, request):
    # Authenticate and login the new user
    newUser = authenticate(username=username, password=password)
    login(request, newUser)