from django import forms

class CountrySelect(forms.Form):
    country = forms.ChoiceField(required=True)