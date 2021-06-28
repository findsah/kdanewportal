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


class Child_Case_Data(models.Model):
    child = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="child_form")

    # Child Details
    civil_number = models.IntegerField(null=True, blank=True)
    school_name = models.CharField(max_length=200)
    dob = models.DateField()
    place_of_birth = models.CharField(max_length=200)
    nationality = models.CharField(max_length=200)
    grade = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)

    # Father Details
    f_name = models.CharField(max_length=200)
    f_age = models.IntegerField(null=True, blank=True)
    f_nationality = models.CharField(max_length=200, null=True, blank=True, default='')
    f_phone = models.IntegerField()
    f_education_level = models.CharField(max_length=200, null=True, blank=True, default='')
    f_occupation = models.CharField(max_length=200, null=True, blank=True, default='')
    f_address = models.CharField(max_length=300)
    f_email = models.EmailField()

    # Mother Details
    m_name = models.CharField(max_length=200, null=True, blank=True, default='')
    m_age = models.IntegerField(null=True, blank=True)
    m_nationality = models.CharField(max_length=200, null=True, blank=True, default='')
    m_phone = models.IntegerField(null=True, blank=True)
    m_education_level = models.CharField(max_length=200, null=True, blank=True, default='')
    m_occupation = models.CharField(max_length=200, null=True, blank=True, default='')
    m_address = models.CharField(max_length=300, null=True, blank=True, default='')
    m_email = models.EmailField(null=True, blank=True)

    # Guardian Details
    g_name = models.CharField(max_length=200, null=True, blank=True, default='')
    g_education_level = models.CharField(max_length=200, null=True, blank=True, default='')
    g_relation_child = models.CharField(max_length=200, null=True, blank=True, default='')
    g_phone = models.IntegerField(null=True, blank=True)
    g_occupation = models.CharField(max_length=200, null=True, blank=True, default='')
    g_address = models.CharField(max_length=300, null=True, blank=True, default='')
    g_email = models.EmailField(null=True, blank=True)

    # family
    relation_btw_parents = models.CharField(max_length=200, null=True, blank=True, default='')
    martial_status = models.CharField(max_length=200, null=True, blank=True, default='')
    passed_away = models.CharField(max_length=200, null=True, blank=True, default='')
    living_in_case = models.CharField(max_length=200, null=True, blank=True, default='')
    father_married = models.CharField(max_length=200, null=True, blank=True, default='')
    mother_married = models.CharField(max_length=200, null=True, blank=True, default='')
    married_when = models.CharField(max_length=200, null=True, blank=True, default='')
    second_marriage = models.CharField(max_length=200, null=True, blank=True, default='')
    nationality_sec_m = models.CharField(max_length=200, null=True, blank=True, default='')
    number_of_fam = models.IntegerField(null=True, blank=True)
    number_of_bros = models.IntegerField(null=True, blank=True)
    number_of_sis = models.IntegerField(null=True, blank=True)
    number_of_bros_f = models.IntegerField(null=True, blank=True)
    number_of_sis_f = models.IntegerField(null=True, blank=True)
    number_of_bros_m = models.IntegerField(null=True, blank=True)
    number_of_sis_m = models.IntegerField(null=True, blank=True)
    order_sib = models.IntegerField(null=True, blank=True)
    other_people_house = models.CharField(max_length=200, null=True, blank=True, default='')
    lives_current = models.CharField(max_length=200, null=True, blank=True, default='')

    # Child History
    # During Pregnancy
    state_of_m = models.CharField(max_length=200, null=True, blank=True, default='')
    p_m_age = models.CharField(max_length=200, null=True, blank=True, default='')
    m_health = models.CharField(max_length=200, null=True, blank=True, default='')
    p_bleeding = models.CharField(max_length=200, null=True, blank=True, default='')
    p_poisoning = models.CharField(max_length=200, null=True, blank=True, default='')
    p_infection = models.CharField(max_length=200, null=True, blank=True, default='')
    p_accident = models.CharField(max_length=200, null=True, blank=True, default='')
    p_accident_detail = models.CharField(max_length=200, null=True, blank=True, default='')
    p_medicines = models.CharField(max_length=200, null=True, blank=True, default='')
    p_problems = models.CharField(max_length=200, null=True, blank=True, default='')
    p_duration = models.CharField(max_length=200, null=True, blank=True, default='')
    p_month = models.CharField(max_length=200, null=True, blank=True, default='')

    # Birth
    type_birth = models.CharField(max_length=200, null=True, blank=True, default='')
    umbilical_cord = models.CharField(max_length=200, null=True, blank=True, default='')
    skin_yellow = models.CharField(max_length=200, null=True, blank=True, default='')
    skin_blue = models.CharField(max_length=200, null=True, blank=True, default='')
    twin_trip = models.CharField(max_length=200, null=True, blank=True, default='')
    needed_oxy = models.CharField(max_length=200, null=True, blank=True, default='')
    colic_cramps = models.CharField(max_length=200, null=True, blank=True, default='')
    dropsy = models.CharField(max_length=200, null=True, blank=True, default='')
    baby_weight = models.IntegerField(null=True, blank=True)
    b_problems = models.CharField(max_length=200, null=True, blank=True, default='')
    b_complications = models.CharField(max_length=200, null=True, blank=True, default='')

    # Post Birth
    health_m_pb = models.CharField(max_length=200, null=True, blank=True, default='')
    incubator = models.CharField(max_length=200, null=True, blank=True, default='')
    incubator_period = models.CharField(max_length=200, null=True, blank=True, default='')
    b_surgery = models.CharField(max_length=200, null=True, blank=True, default='')

    extremely_high_temp_age = models.IntegerField(null=True, blank=True)
    extremely_high_temp_dur = models.CharField(max_length=200, null=True, blank=True, default='')
    ear_problems_age = models.IntegerField(null=True, blank=True)
    ear_problems_dur = models.CharField(max_length=200, null=True, blank=True, default='')
    vision_problems_age = models.IntegerField(null=True, blank=True)
    vision_problems_dur = models.CharField(max_length=200, null=True, blank=True, default='')
    juandice_age = models.IntegerField(null=True, blank=True)
    juandice_dur = models.CharField(max_length=200, null=True, blank=True, default='')
    asthma_age = models.IntegerField(null=True, blank=True)
    asthma_dur = models.CharField(max_length=200, null=True, blank=True, default='')
    allergy_age = models.IntegerField(null=True, blank=True)
    allergy_dur = models.CharField(max_length=200, null=True, blank=True, default='')
    poisoning_age = models.IntegerField(null=True, blank=True)
    poisoning_dur = models.CharField(max_length=200, null=True, blank=True, default='')
    surgical_age = models.IntegerField(null=True, blank=True)
    surgical_dur = models.CharField(max_length=200, null=True, blank=True, default='')
    surgery = models.CharField(max_length=200, null=True, blank=True, default='')
    accident_age = models.IntegerField(null=True, blank=True)
    accident_dur = models.CharField(max_length=200, null=True, blank=True, default='')
    accident = models.CharField(max_length=200, null=True, blank=True, default='')
    not_mentioned_disease = models.CharField(max_length=200, null=True, blank=True, default='')

    # Stages of Growth
    breastfeeding = models.CharField(max_length=200, null=True, blank=True, default='')
    age_weaning = models.IntegerField(null=True, blank=True)
    age_teething = models.IntegerField(null=True, blank=True)
    age_commune = models.IntegerField(null=True, blank=True)
    age_pronouncing = models.IntegerField(null=True, blank=True)
    age_speech = models.IntegerField(null=True, blank=True)
    age_full_sentence = models.IntegerField(null=True, blank=True)
    age_bottle_milk = models.IntegerField(null=True, blank=True)
    age_love = models.IntegerField(null=True, blank=True)
    age_sat_self = models.IntegerField(null=True, blank=True)
    age_stop_self = models.IntegerField(null=True, blank=True)
    age_walking = models.IntegerField(null=True, blank=True)
    age_wearing_help = models.IntegerField(null=True, blank=True)
    age_wearing_self = models.IntegerField(null=True, blank=True)
    age_shoes = models.IntegerField(null=True, blank=True)
    age_feeding = models.IntegerField(null=True, blank=True)
    age_urination = models.IntegerField(null=True, blank=True)
    age_bathroom = models.IntegerField(null=True, blank=True)

    visual_prob = models.CharField(max_length=200, null=True, blank=True, default='')
    use_glasses = models.CharField(max_length=200, null=True, blank=True, default='')
    age_glasses = models.IntegerField(null=True, blank=True)
    hearing_prob = models.CharField(max_length=200, null=True, blank=True, default='')
    use_hearing_aid = models.CharField(max_length=200, null=True, blank=True, default='')
    age_hearing_aid = models.IntegerField(null=True, blank=True)
    diff_speaking = models.CharField(max_length=200, null=True, blank=True, default='')
    treated_speech = models.CharField(max_length=200, null=True, blank=True, default='')
    age_treated_speech = models.IntegerField(null=True, blank=True)
    hand_writing = models.CharField(max_length=200, null=True, blank=True, default='')
    leg_kicking = models.CharField(max_length=200, null=True, blank=True, default='')
    both_hands = models.CharField(max_length=200, null=True, blank=True, default='')
    stop_left_hand = models.CharField(max_length=200, null=True, blank=True, default='')
    age_stop_left_hand = models.IntegerField(null=True, blank=True)
    involuntary_urination = models.CharField(max_length=200, null=True, blank=True, default='')
    cause_involuntary_urination = models.CharField(max_length=200, null=True, blank=True, default='')
    age_involuntary_urination = models.IntegerField(null=True, blank=True)
    medicines_bool = models.CharField(max_length=200, null=True, blank=True, default='')
    medicines_name = models.CharField(max_length=200, null=True, blank=True, default='')
    medicine_reason = models.CharField(max_length=200, null=True, blank=True, default='')
    eating_habits = models.CharField(max_length=200, null=True, blank=True, default='')
    fav_food = models.CharField(max_length=200, null=True, blank=True, default='')

    # Family History
    hyperinactivity = models.TextField(null=True, blank=True)
    reading_diff = models.TextField(null=True, blank=True)
    writing_dictating_diff = models.TextField(null=True, blank=True)
    calculating_diff = models.TextField(null=True, blank=True)
    concentration_diff = models.TextField(null=True, blank=True)
    pronouncing_diff = models.TextField(null=True, blank=True)
    impaired_hearing = models.TextField(null=True, blank=True)
    visual_impairment = models.TextField(null=True, blank=True)
    impaired_mobility = models.TextField(null=True, blank=True)
    intellectual_disability = models.TextField(null=True, blank=True)
    down_syn = models.TextField(null=True, blank=True)
    autism = models.TextField(null=True, blank=True)
    other_prob = models.TextField(null=True, blank=True)
    child_hereditary = models.CharField(max_length=200, null=True, blank=True, default='')
    age_problem = models.IntegerField(null=True, blank=True)
    prob_effect = models.CharField(max_length=200, null=True, blank=True, default='')

    # Social Development
    friends = models.CharField(max_length=200, null=True, blank=True, default='')
    siblings = models.CharField(max_length=200, null=True, blank=True, default='')
    parents = models.CharField(max_length=200, null=True, blank=True, default='')
    adults = models.CharField(max_length=200, null=True, blank=True, default='')
    maid = models.CharField(max_length=200, null=True, blank=True, default='')
    age_maid = models.IntegerField(null=True, blank=True)
    fam_auth = models.CharField(max_length=200, null=True, blank=True, default='')
    fam_close = models.CharField(max_length=200, null=True, blank=True, default='')
    punishment_sys = models.CharField(max_length=200, null=True, blank=True, default='')
    punisher = models.CharField(max_length=200, null=True, blank=True, default='')
    punishment = models.CharField(max_length=200, null=True, blank=True, default='')
    spent_time_in = models.CharField(max_length=200, null=True, blank=True, default='')
    fav_hobby = models.CharField(max_length=200, null=True, blank=True, default='')
    main_lang = models.CharField(max_length=200, null=True, blank=True, default='')
    other_lang = models.CharField(max_length=200, null=True, blank=True, default='')
    dilects = models.CharField(max_length=200, null=True, blank=True, default='')

    # Child Behaviour
    mental_illness_bool = models.CharField(max_length=200, null=True, blank=True, default='')
    mental_illness = models.CharField(max_length=200, null=True, blank=True, default='')

    # Not true, sometimes, true
    spends_time_alone = models.CharField(max_length=200, null=True, blank=True, default='')
    no_friend = models.CharField(max_length=200, null=True, blank=True, default='')
    diff_friend = models.CharField(max_length=200, null=True, blank=True, default='')
    quarrels_friend = models.CharField(max_length=200, null=True, blank=True, default='')
    like_to_play = models.CharField(max_length=200, null=True, blank=True, default='')
    avoid_to_play = models.CharField(max_length=200, null=True, blank=True, default='')
    older_friend = models.CharField(max_length=200, null=True, blank=True, default='')
    younger_friend = models.CharField(max_length=200, null=True, blank=True, default='')
    seeker_attention = models.CharField(max_length=200, null=True, blank=True, default='')
    confidence_ability = models.CharField(max_length=200, null=True, blank=True, default='')
    quite = models.CharField(max_length=200, null=True, blank=True, default='')
    impulsive = models.CharField(max_length=200, null=True, blank=True, default='')
    normal_activity = models.CharField(max_length=200, null=True, blank=True, default='')
    cooperative = models.CharField(max_length=200, null=True, blank=True, default='')
    lies = models.CharField(max_length=200, null=True, blank=True, default='')
    moody = models.CharField(max_length=200, null=True, blank=True, default='')
    gets_bored = models.CharField(max_length=200, null=True, blank=True, default='')
    completes_tasks = models.CharField(max_length=200, null=True, blank=True, default='')
    sad = models.CharField(max_length=200, null=True, blank=True, default='')
    cheerful = models.CharField(max_length=200, null=True, blank=True, default='')
    aggressive = models.CharField(max_length=200, null=True, blank=True, default='')
    avoid_competition = models.CharField(max_length=200, null=True, blank=True, default='')
    compete_others = models.CharField(max_length=200, null=True, blank=True, default='')
    lazy = models.CharField(max_length=200, null=True, blank=True, default='')
    leadership = models.CharField(max_length=200, null=True, blank=True, default='')
    self_reliance = models.CharField(max_length=200, null=True, blank=True, default='')
    long_time_tasks = models.CharField(max_length=200, null=True, blank=True, default='')
    anxious = models.CharField(max_length=200, null=True, blank=True, default='')
    afraid = models.CharField(max_length=200, null=True, blank=True, default='')

    # School History
    school_name_1 = models.CharField(max_length=200, null=True, blank=True, default='')
    enroll_date_1 = models.DateField(null=True, blank=True, default=timezone.now().date())
    attitude_school_1 = models.CharField(max_length=200, null=True, blank=True, default='')
    school_name_2 = models.CharField(max_length=200, null=True, blank=True, default='')
    enroll_date_2 = models.DateField(null=True, blank=True, default=timezone.now().date())
    attitude_school_2 = models.CharField(max_length=200, null=True, blank=True, default='')
    school_name_3 = models.CharField(max_length=200, null=True, blank=True, default='')
    enroll_date_3 = models.DateField(null=True, blank=True, default=timezone.now().date())
    attitude_school_3 = models.CharField(max_length=200, null=True, blank=True, default='')
    first_stage = models.CharField(max_length=200, null=True, blank=True, default='')
    failed = models.CharField(max_length=200, null=True, blank=True, default='')
    failed_class = models.CharField(max_length=200, null=True, blank=True, default='')
    failed_subjs = models.CharField(max_length=200, null=True, blank=True, default='')
    private_tutors = models.CharField(max_length=200, null=True, blank=True, default='')
    take_advantage = models.CharField(max_length=200, null=True, blank=True, default='')
    difficult_teaching = models.CharField(max_length=200, null=True, blank=True, default='')
    teachers_note = models.CharField(max_length=200, null=True, blank=True, default='')
    supervision = models.CharField(max_length=200, null=True, blank=True, default='')
    academic_achievement = models.CharField(max_length=200, null=True, blank=True, default='')
    motivation = models.CharField(max_length=200, null=True, blank=True, default='')
    enthusiasm = models.CharField(max_length=200, null=True, blank=True, default='')
    time_punctual = models.CharField(max_length=200, null=True, blank=True, default='')
    fav_articles = models.CharField(max_length=200, null=True, blank=True, default='')
    least_fav_material = models.CharField(max_length=200, null=True, blank=True, default='')
    rel_teachers = models.CharField(max_length=200, null=True, blank=True, default='')
    desire_school = models.CharField(max_length=200, null=True, blank=True, default='')
    reason_absent = models.CharField(max_length=200, null=True, blank=True, default='')

    # Difficulties
    reading = models.CharField(max_length=200, null=True, blank=True, default='')
    dictating = models.CharField(max_length=200, null=True, blank=True, default='')
    writing = models.CharField(max_length=200, null=True, blank=True, default='')
    remembering_nearby = models.CharField(max_length=200, null=True, blank=True, default='')
    recog_time = models.CharField(max_length=200, null=True, blank=True, default='')
    recog_days = models.CharField(max_length=200, null=True, blank=True, default='')
    recog_directions = models.CharField(max_length=200, null=True, blank=True, default='')
    completing_work = models.CharField(max_length=200, null=True, blank=True, default='')
    focus_attention = models.CharField(max_length=200, null=True, blank=True, default='')
    understanding = models.CharField(max_length=200, null=True, blank=True, default='')
    remembering_remote = models.CharField(max_length=200, null=True, blank=True, default='')
    relationships = models.CharField(max_length=200, null=True, blank=True, default='')
    expressing_ideas = models.CharField(max_length=200, null=True, blank=True, default='')
    remembering_skills = models.CharField(max_length=200, null=True, blank=True, default='')
    moving_blackboard = models.CharField(max_length=200, null=True, blank=True, default='')
    copying_printed = models.CharField(max_length=200, null=True, blank=True, default='')
    flip_words = models.CharField(max_length=200, null=True, blank=True, default='')
    confuses_numbers = models.CharField(max_length=200, null=True, blank=True, default='')
    understanding_verbal = models.CharField(max_length=200, null=True, blank=True, default='')
    learning_listening = models.CharField(max_length=200, null=True, blank=True, default='')
    repeat_instruction = models.CharField(max_length=200, null=True, blank=True, default='')
    distinguish_numbers = models.CharField(max_length=200, null=True, blank=True, default='')
    memorizing_multiplication = models.CharField(max_length=200, null=True, blank=True, default='')
    memorizing_phone = models.CharField(max_length=200, null=True, blank=True, default='')
    counting_up = models.CharField(max_length=200, null=True, blank=True, default='')
    performing_add_subt = models.CharField(max_length=200, null=True, blank=True, default='')
    understanding_mathematical = models.CharField(max_length=200, null=True, blank=True, default='')
    distinguish_size = models.CharField(max_length=200, null=True, blank=True, default='')

    # Other Info
    parents_cooperation = models.TextField(null=True, blank=True)
    reason_1 = models.TextField(null=True, blank=True)
    reason_2 = models.TextField(null=True, blank=True)
    reason_3 = models.TextField(null=True, blank=True)
    reason_4 = models.TextField(null=True, blank=True)
    reason_5 = models.TextField(null=True, blank=True)
    prev_iq = models.CharField(max_length=200, null=True, blank=True, default='')
    date_last_assessment = models.DateField(null=True, blank=True, default=timezone.now().date())
    place_last_assessment = models.CharField(max_length=200, null=True, blank=True, default='')
    other_info = models.TextField(null=True, blank=True)
