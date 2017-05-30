from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from userProfile.functions import get_form_data, activation_salt, activationEmail, authenticate_user
from userProfile.models import User_Profile


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
        self.return_key = None

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
        create_user_profile = User_Profile(user=self.user, activation_key=self.activation_key, status=self.status,
                                           country=self.country)
        create_user_profile.save()


    def logout(self, request):
        logout(request)

    def activation_email(self, request=None):
        if self.username is None:
            self.username = request.user.username
            self.email = request.user.email
            self.activation_key = activation_salt(self.email)
            activationEmail(self.username, self.activation_key, self.email)

        else:
            activationEmail(self.username, self.activation_key, self.email)

    def activate_account(self, request):
        self.return_key = request.GET["activation_key"]
        self.user = request.user
        self.activation_key = self.user.activation_key
        if self.return_key == self.activation_key:
            update_user_status = User_Profile.objects.get(user=self.user)
            update_user_status.status = "confirmed"
            update_user_status.save()

            return 1
        else:
            return 0

    def get_user_profile(self, request):

        self.user = request.user

        current_user = User_Profile.objects.get(user=self.user)
        self.country = current_user.country
        self.status = current_user.status

    def update_user_profile(self, request):
        self.username = request.user.username
        self.user = User.objects.get(username=self.username)
        self.user.email = request.POST['email']
        self.user.first_name = request.POST['first_name']
        self.user.last_name = request.POST['last_name']
        self.user.save()

        user_profile = User_Profile.objects.get(user=self.user)
        user_profile.country = request.POST['country']
        user_profile.save()

    def update_password(self, request):

        return "I am an incomplete Method :("

    def delete_user_profile(self, request):
        self.username = request.user.username
        self.user = request.user

        django_user = User.objects.get(username=self.username)
        django_user.is_active = False
        django_user.save()
        user_profile = User_Profile.objects.get(user=self.user)
        user_profile.status = "inactive"
        user_profile.save()