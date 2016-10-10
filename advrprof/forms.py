from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# This is the form for editing user details in profile area

class EmailEdit(forms.Form):
    emailEdit = forms.EmailField(required=False)
    
    class Meta:
        model = User
        fields = ('EmailEdit')

class UsernameEdit(forms.Form):
	username = forms.CharField(required=True)

	class Meta:
		model = User
		fields = ('username')

class FirstNameEdit(forms.Form):
    first_name = forms.CharField(required=False)
    
    class Meta:
        model = User
        fields = ('first_name')

class LastNameEdit(forms.Form):
    last_name = forms.CharField(required=False)
    
    class Meta:
        model = User
        fields = ('last_name')
