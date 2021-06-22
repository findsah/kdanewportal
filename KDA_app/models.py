from django.db import models
from django.contrib.auth.models import User
import os

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# from rest_framework.authtoken.models import Token

"""localhost:8015"""


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, username, first_name, last_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(username, first_name, last_name, password, **other_fields)

    def create_user(self, username, first_name, last_name, password, **other_fields):

        if not username:
            raise ValueError(_('You must provide a username'))

        # email = self.normalize_email(email)
        user = self.model(username=username, first_name=first_name, last_name=last_name,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user


class Role(models.Model):
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=300, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_user = models.CharField(max_length=300)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    modified_user = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name


Gender = [('Male', 'Male'), ('Female', 'Female')]


# USER_TYPE = [('Student', 'Student'), ('Individual', 'Individual'), ('Receptionist', 'Receptionist'),
#              ('Psychologist', 'Psychologist'), ('Secretary', 'Secretary')]


class Person(AbstractBaseUser, PermissionsMixin):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    gender = models.CharField(max_length=300, null=True, blank=True, choices=Gender)
    dob = models.DateField(null=True, blank=True)

    def get_upload_path_profile(instance, filename):
        return f'person/profile_pic/{instance.username}/{filename}'

    profile_pic = models.ImageField(upload_to=get_upload_path_profile, null=True, blank=True)
    username = models.CharField(max_length=300, unique=True)

    father_name = models.CharField(max_length=300, null=True, blank=True)
    mother_name = models.CharField(max_length=300, null=True, blank=True)

    country = models.CharField(max_length=300, null=True, blank=True)
    state = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=300, null=True, blank=True)
    street = models.CharField(max_length=300, null=True, blank=True)
    block = models.CharField(max_length=300, null=True, blank=True)
    postal_code = models.CharField(max_length=300, null=True, blank=True)

    qualification = models.CharField(max_length=300, null=True, blank=True)
    institute = models.CharField(max_length=300, null=True, blank=True)
    class_name = models.CharField(max_length=300, null=True, blank=True)

    mobile_number = models.IntegerField(null=True, blank=True)
    email = models.EmailField(unique=True)

    approved = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    # @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    # def create_auth_token(sender, instance=None, created=False, **kwargs):
    #     if created:
    #         Token.objects.create(user=instance)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Availability(models.Model):
    psychologist = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='avail')
    m_available_time_from = models.TimeField(null=True, blank=True)
    m_available_time_to = models.TimeField(null=True, blank=True)
    tu_available_time_from = models.TimeField(null=True, blank=True)
    tu_available_time_to = models.TimeField(null=True, blank=True)
    w_available_time_from = models.TimeField(null=True, blank=True)
    w_available_time_to = models.TimeField(null=True, blank=True)
    th_available_time_from = models.TimeField(null=True, blank=True)
    th_available_time_to = models.TimeField(null=True, blank=True)
    # f_available_time_from = models.TimeField(null=True, blank=True)
    # f_available_time_to = models.TimeField(null=True, blank=True)
    sa_available_time_from = models.TimeField(null=True, blank=True)
    sa_available_time_to = models.TimeField(null=True, blank=True)
    su_available_time_from = models.TimeField(null=True, blank=True)
    su_available_time_to = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.psychologist.first_name


class Slot(models.Model):
    psychologist = models.ForeignKey(Person, on_delete=models.CASCADE)
    day = models.DateField()
    s_time = models.TimeField()
    e_time = models.TimeField()
    available = models.BooleanField()

    def __str__(self):
        return str(self.day)


class Hosted_Centres(models.Model):
    centre_name = models.CharField(max_length=300)

    def get_upload_path_hc_logo(instance, filename):
        return f'hosted_centres/{instance.centre_email}_{instance.centre_name}/{filename}'

    hc_logo = models.ImageField(upload_to=get_upload_path_hc_logo)

    def get_upload_path_hc_document(instance, filename):
        return f'hosted_centres/{instance.centre_email}_{instance.centre_name}/document/{filename}'

    hc_document = models.FileField(upload_to=get_upload_path_hc_document, null=True, blank=True)

    qualification = models.CharField(max_length=300, null=True, blank=True)
    institute = models.CharField(max_length=300, null=True, blank=True)

    spoc_f_name = models.CharField(_("SPOC first name"), max_length=300)
    spoc_l_name = models.CharField(_("SPOC last name"), max_length=300)

    def get_upload_path_spoc_profile_pic(instance, filename):
        return f'hosted_centres/{instance.centre_email}_{instance.centre_name}/spoc/{filename}'

    spoc_profile_pic = models.ImageField(upload_to=get_upload_path_spoc_profile_pic, null=True, blank=True)

    country = models.CharField(max_length=300)
    state = models.CharField(max_length=300)
    city = models.CharField(max_length=300)
    street = models.CharField(max_length=300)
    block = models.CharField(max_length=300)
    postal_code = models.CharField(max_length=300, null=True, blank=True)

    spoc_email = models.EmailField()
    spoc_mobile_number = models.IntegerField()
    spoc_extension_number = models.IntegerField(null=True, blank=True)
    spoc_office_number = models.IntegerField(null=True, blank=True)

    centre_mobile_number_1 = models.IntegerField(null=True, blank=True)
    centre_mobile_number_2 = models.IntegerField(null=True, blank=True)
    centre_office_number = models.IntegerField(null=True, blank=True)
    centre_extension_number = models.IntegerField(null=True, blank=True)
    centre_email = models.EmailField(null=True, blank=True, unique=True)
    centre_web_address = models.CharField(max_length=300, null=True, blank=True)

    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.centre_name


class Appointment(models.Model):
    psychologist = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='appointment')
    child = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='appointmentt')
    appointment_date = models.DateField()
    appointment_s_time = models.TimeField()
    appointment_e_time = models.TimeField()
    status = models.BooleanField()

    def __str__(self):
        return self.child.first_name
