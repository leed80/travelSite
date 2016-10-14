from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django_countries.fields import LazyTypedChoiceField
from django_countries import countries

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'E-mail address'}))
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    country = LazyTypedChoiceField(choices=countries)
    address = forms.CharField(required=True)
    postcode = forms.CharField(required=True)



    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'country', 'address', 'postcode')
        
#clean email field
def clean_email(self):
    email = self.cleaned_data["email"]
    try:
        User._default_manager.get(email=email)
    except User.DoesNotExist:
        return email
    raise forms.ValidationError('duplicate email')

