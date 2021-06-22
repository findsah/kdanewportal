from django import forms
from .models import Person
from django.core.exceptions import ValidationError


ROLES = [('Admin', 'Admin'), ('Trainer', 'Trainer'), ('Centre', 'Centre'), ('Individual', 'Individual'),
         ('Secretary', 'Secretary'),
         ('Physiologist', 'Physiologist'), ('Student', 'Student'), ('Receptionist', 'Receptionist')]
Gender = [('Male', 'Male'), ('Female', 'Female')]


# class login_form(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())
#     # rolee = forms.ChoiceField(choices=ROLES, widget=forms.Select, initial='')
#
#     class Meta:
#         model = Person
#         fields = ['username', 'password']


class login_form(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())


class register_form(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    username = forms.CharField(required=True)
    gender = forms.ChoiceField(choices=Gender, required=True)
    dob = forms.DateField(widget=forms.DateInput, required=True)
    profile_picture = forms.ImageField(required=True)
    street = forms.CharField(required=True)
    block = forms.CharField(required=True)
    city = forms.CharField(required=True)
    state = forms.CharField(required=True)
    country = forms.CharField(required=True)
    postalcode = forms.CharField(required=True)
    qualification = forms.CharField(required=True)
    institution = forms.CharField(required=True)
    mobile = forms.IntegerField(min_value=0, required=True)
    email = forms.EmailField(required=True)
    
    def clean_username(self):
        username = self.cleaned_data['username']
        a = Person.objects.filter(username=username)
        if a:
            raise ValidationError("username is taken")
        return username


class register_centre_form(forms.Form):
    centre_name = forms.CharField(required=True)
    hc_logo = forms.ImageField(required=True)
    hc_document = forms.FileField(required=False)

    qualification = forms.CharField(required=False)
    institution = forms.CharField(required=False)

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    profile_picture = forms.ImageField(required=False)

    street = forms.CharField(required=True)
    block = forms.CharField(required=True)
    city = forms.CharField(required=True)
    state = forms.CharField(required=True)
    country = forms.CharField(required=True)
    postalcode = forms.CharField(required=False)

    spoc_mobile_number = forms.IntegerField(min_value=0, required=True)
    spoc_email = forms.EmailField(required=True)
    spoc_extension = forms.IntegerField(min_value=0, required=False)
    spoc_office_number = forms.IntegerField(min_value=0, required=False)

    centre_mobile_number_1 = forms.IntegerField(min_value=0, required=True)
    centre_mobile_number_2 = forms.IntegerField(min_value=0, required=False)
    centre_office_number = forms.IntegerField(min_value=0, required=False)
    centre_extension_number = forms.IntegerField(min_value=0, required=False)
    centre_email = forms.EmailField(required=True)
    centre_web_address = forms.CharField(required=False)


class add_appointment_form(forms.Form):
    appointment_date = forms.CharField(required=True)
