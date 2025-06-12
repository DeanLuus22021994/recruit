"""Forms for the candidates application."""

from django import forms


class UserApplyStep1Form(forms.Form):
    """Form for the first step of user application."""

    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    citizenship = forms.CharField(max_length=50)
    skype_id = forms.CharField(max_length=50, required=False)
    timezone = forms.CharField(max_length=50)


class UserApplyStep2Form(forms.Form):
    """Form for the second step of user application."""

    birth_year = forms.CharField(max_length=4)
    gender = forms.ChoiceField(choices=[("male", "Male"), ("female", "Female")])
    education = forms.CharField(max_length=25)
    education_major = forms.CharField(max_length=250, required=False)
    image = forms.ImageField()
    resume = forms.FileField()
