from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm




class EmailEdit(forms.Form):
    email = forms.EmailField(required=False)
    

    class Meta:
        model = User
        fields = ('email')

class UsernameEdit(forms.Form):
	username = forms.CharField(required=True)

	class Meta:
		model = User
		fields = ('username')

class DescForm(forms.Form):
	desc = forms.CharField(required=True)

	class Meta:
		model = User
		fields = ('description')

class DescEdit(forms.Form):
    description = forms.CharField(required=False)
    

    class Meta:
        model = User
        fields = ('description')

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

class PhotoForm(forms.Form):
    photo = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )

    class Meta:
        model = User
        fields = ('photo')

class PhotoEdit(forms.Form):
    photo = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )

    class Meta:
        model = User
        fields = ('photo')