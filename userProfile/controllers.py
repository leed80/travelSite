from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from userProfile.User_Profile_Class import User_Profile_Create_Edit
from userProfile.views import user_registered_view, registration_page_view, email_activation_view, profile_page_view, \
    profile_deleted_view, user_profile_updated_view, logout_view


"""

This page contains all the controllers for the registration, profile and user authentication. Each controller
function is mapped to a url from urls.py in the userProfile application. All controller functions use the
User_Profile_Create_Edit class defined in User_Profile_Class.py and load views from views.py. Service functions are
called by the User_Profile_Create_Edit class from the functions.py file and models from the models.py file.

"""

def registration_page_controller(request):
    view = registration_page_view(request)
    return view.load()


@login_required
def profile(request):
    user_profile = User_Profile_Create_Edit()
    user_profile.get_user_profile(request)

    view = profile_page_view(user_profile.country, user_profile.status, request)
    return view.load()


@login_required
def edit_user_profile_controller(request):
    user_profile = User_Profile_Create_Edit()
    user_profile.update_user_profile(request)
    country = user_profile.country

    view = user_profile_updated_view(request, country)
    return view.load()


@login_required
def deleteProfile(request):
    user = User_Profile_Create_Edit()
    user.delete_user_profile(request)

    view = profile_deleted_view()
    return view.load()


@login_required
def activate_account(request):
    user_profile = User_Profile_Create_Edit(request)
    activation_message = user_profile.activate_account()

    view = email_activation_view(activation_message, request)
    return view.load()


def register_user_controller(request):
    if request.method == 'POST':
        # Register the user
        create_user = User_Profile_Create_Edit()
        create_user.new_user_profile(request)
        # activate email closed off whilst in developent
        # create_user.activation_email()

        # log the user in
        create_user.login(request)

        # Load the view
        view = user_registered_view(request, create_user)
        return view.load()
    view = registration_page_view(request)
    return view.load()


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



@login_required
def user_logout_controller(request):
    # Use the djngo logout function to log the current user out and return to homepage
    user_profile = User_Profile_Create_Edit()
    user_profile.logout(request)
    view = logout_view(request)
    return view.load()
