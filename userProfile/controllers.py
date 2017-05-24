from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from userProfile.views import user_registered_view, registration_page_view

from userProfile.functions import get_form_data, getUser, activationEmail, activation_salt
from userProfile.models import User_Profile


def registration_page_controller(request):
    view = registration_page_view(request)
    return view.load()


@login_required
def profile(request):
    return render_to_response('advrprof/profile.html', userInformation, RequestContext(request))


class User_Profile_Create_Edit(object):
    def __init__(self):
        self.username = None
        self.email = None
        self.first_name = None
        self.last_name = None
        self.country = None
        self.phone = None
        self.password = None
        self.password2 = None
        self.activation_key = None
        self.status = None
        self.user = None

    def new_user_profile(self, request):
        form_data = get_form_data(request)
        self.username = form_data[0]
        self.first_name = form_data[1]
        self.last_name = form_data[2]
        self.password = form_data[3]
        self.email = form_data[4]
        self.activation_key = activation_salt(self.email)
        self.status = "unconfirmed"
        self.country = form_data[5]

        # We use django user model to store basic user information
        create_django_user = User(username=self.username, first_name=self.first_name, last_name=self.last_name,
                                  email=self.email, is_staff=False)
        create_django_user.set_password(self.password)  # This will encrypt the password
        create_django_user.save()

        # get user ID
        self.user = User.objects.get(username=self.username)

        # We use the User profile model to create the table for non standard user information with the user foreign key
        create_user_profile = User_Profile(user=self.user, activation_key=self.activation_key, status=self.status, country=self.country)
        create_user_profile.save()

    def login(self, request):
        if request.user.is_authenticated():
            return 0
        elif self.user:
            login(request, self.user)
            return 1
        else:
            user = authenticate_user(request)
            login(request, user)
            return 1

    def activation_email(self, request=None):
        if self.username is None:
            self.username = request.user.username
            self.email = request.user.email
            self.activation_key = activation_salt(self.email)
            activationEmail(self.username, self.activation_key, self.email)

        else:
            activationEmail(self.username, self.activation_key, self.email)

    def activate_account(self):
        return "I am an incomplete Method :("

    def get_user_profile(self):
        return "I am an incomplete Method :("

    def update_user_profile(self):
        return "I am an incomplete Method :("

    def delete_user_profile(self):
        return "I am an incomplete Method :("


@login_required
def deleteProfile(request):
    user = getUser(request)
    user.delete()
    userDeleted = 'User deleted'
    deleteMessage = {'deleted': userDeleted}

    return render_to_response('homepage/home.html', deleteMessage, RequestContext(request))


def register_user_controller(request):
    if request.method == 'POST':
        # Register the user
        create_user = User_Profile_Create_Edit()
        create_user.new_user_profile(request)
        #activate email closed off whilst in developent
        #create_user.activation_email()

        # log the user in
        create_user.login(request)

        # Load the view
        view = user_registered_view(request, create_user)
        return view.load()
    view = registration_page_view(request)
    return view.load()


def saveNewUserProfile(user, activationKey, status, country, address, postcode):
    # Create and save new user profile
    new_profile = User_Profile_Create_Edit(user=user, activation_key=activationKey, status=status, country=country, address=address,
                                           postcode=postcode)
    new_profile.save()


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


def success(request):
    # This is the view for returning the page for successful registration
    return render_to_response('reg/register_success.html')


def user_login(request):
    # The view for logging the user in

    user = User_Profile_Create_Edit()
    user.login()

    # # Check the sent details are correct. If the user is already authenticated then send them to their profile page
    # if
    #     return render_to_response('advrprof/profile.html', RequestContext(request))
    # else:
    #     # Get the context data for the users request
    #     context = RequestContext(request)
    #
    #     # Check for POST method
    #     if request.method == 'POST':
    #
    #         user = authenticate_user(request)
    #
    #         # If user is correct then login and send to profile page
    #         if user:
    #             login(request, user)
    #             return HttpResponseRedirect('userProfile/profile/')
    #         else:
    #             # The wrong login details were provided
    #             invalid = 'yes'
    #             args = {'invalid': invalid}
    #             return render_to_response('reg/login.html', args, RequestContext(request))
    #     else:
    #         # POST was not used to return to login form
    #         return render_to_response('reg/login.html', {}, context)
    #


def authenticate_user(request):
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
