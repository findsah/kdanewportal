from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Person, Role, Hosted_Centres, Appointment, Availability, Slot, Child_Case_Data
from django.contrib import messages
from .forms import login_form, register_form, register_centre_form, add_appointment_form, child_case_form
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.utils import timezone
import datetime

# Create your views here.

current_time = timezone.now() + timezone.timedelta(hours=5)


# def home(request):
#     super = Person.objects.get(is_superuser=True)
#     if request.user.email != super.email:
#         return render(request, 'static_files/login.html')
#     else:
#         return render(request, 'static_files/index.html')
#
#
# def login(request):
#     email = request.POST.get('email')
#     password = request.POST.get('password')
#     super = Person.objects.get(is_superuser=True)
#     if email and password:
#         x = Person.objects.filter(email=email)
#         y = False
#         if x:
#             x = Person.objects.get(email=email)
#             y = x.check_password(password)
#         if y:
#             if x.email == super.email:
#                 return render(request, 'static_files/index.html')
#             else:
#                 messages.warning(request, 'Enter Correct Credentials')
#                 return redirect(login)
#         else:
#             messages.warning(request, 'Enter Correct Credentials')
#             return redirect(login)
#     return render(request, 'static_files/login.html')


def login(request):
    if request.method == "POST":
        lf = login_form(request.POST)
        if lf.is_valid():
            username = lf.cleaned_data["username"]
            password = lf.cleaned_data["password"]
            print(username, password)
            user = authenticate(username=username, password=password)
            print(user)
            if user:
                if user.role:
                    if user.role.name == "Receptionist":
                        return redirect(receptionist_dashboard)
                else:
                    return redirect(index)
            elif Person.objects.filter(username=username).count() == 0:
                messages.warning(request, message="Wrong Credentials, Check again")
                return redirect(login)
            elif not Person.objects.get(username=username).check_password(password):
                messages.warning(request, message="Wrong Credentials, Check again")
                return redirect(login)
            else:
                messages.warning(request, message="Wrong Credentials, Check again")
                return redirect(login)
    else:
        lf = login_form()
    return render(request, 'static_files/login.html', {'form': lf})


def index(request):
    return render(request, 'static_files/index.html')


def register(request):
    if request.method == "POST":
        rf = register_form(request.POST, request.FILES)
        if rf.is_valid():
            first_name = rf.cleaned_data['first_name']
            last_name = rf.cleaned_data['last_name']
            username = rf.cleaned_data['username']
            gender = rf.cleaned_data['gender']
            dob = rf.cleaned_data['dob']
            profile_picture = rf.cleaned_data['profile_picture']
            # profile_picture = request.FILES['profile_picture']
            street = rf.cleaned_data['street']
            block = rf.cleaned_data['block']
            city = rf.cleaned_data['city']
            state = rf.cleaned_data['state']
            country = rf.cleaned_data['country']
            postal_code = rf.cleaned_data['postalcode']
            qualification = rf.cleaned_data['qualification']
            institution = rf.cleaned_data['institution']
            mobile = rf.cleaned_data['mobile']
            email = rf.cleaned_data['email']

            Person.objects.create(first_name=first_name, last_name=last_name, gender=gender, dob=dob,
                                  profile_pic=profile_picture, username=username, country=country, state=state,
                                  city=city,
                                  street=street, block=block, postal_code=postal_code, qualification=qualification,
                                  institute=institution, mobile_number=mobile, email=email)
            messages.success(request, message="Individual Registered, Waiting for Approval From Admin")
            return redirect(register)
        else:
            print(rf.errors)
            return HttpResponse(rf.errors)
    else:
        rf = register_form()
    return render(request, 'static_files/register.html', {'form': rf})


def register_centre(request):
    rf = ''
    if request.method == "POST":
        rf = register_centre_form(request.POST, request.FILES)
        if rf.is_valid():
            centre_name = rf.cleaned_data['centre_name']
            hc_logo = rf.cleaned_data['hc_logo']
            hc_document = rf.cleaned_data['hc_document']
            qualification = rf.cleaned_data['qualification']
            institution = rf.cleaned_data['institution']
            first_name = rf.cleaned_data['first_name']
            last_name = rf.cleaned_data['last_name']
            profile_picture = rf.cleaned_data['profile_picture']
            # profile_picture = request.FILES['profile_picture']
            street = rf.cleaned_data['street']
            block = rf.cleaned_data['block']
            city = rf.cleaned_data['city']
            state = rf.cleaned_data['state']
            country = rf.cleaned_data['country']
            postal_code = rf.cleaned_data['postalcode']
            spoc_mobile_number = rf.cleaned_data['spoc_mobile_number']
            spoc_email = rf.cleaned_data['spoc_email']
            spoc_extension = rf.cleaned_data['spoc_extension']
            spoc_office_number = rf.cleaned_data['spoc_office_number']
            centre_mobile_number_1 = rf.cleaned_data['centre_mobile_number_1']
            centre_mobile_number_2 = rf.cleaned_data['centre_mobile_number_2']
            centre_office_number = rf.cleaned_data['centre_office_number']
            centre_extension_number = rf.cleaned_data['centre_extension_number']
            centre_email = rf.cleaned_data['centre_email']
            centre_web_address = rf.cleaned_data['centre_web_address']

            Hosted_Centres.objects.create(centre_name=centre_name, hc_logo=hc_logo, hc_document=hc_document,
                                          qualification=qualification, institute=institution, spoc_f_name=first_name,
                                          spoc_l_name=last_name, spoc_profile_pic=profile_picture, country=country,
                                          state=state, city=city, street=street, block=block, postal_code=postal_code,
                                          spoc_email=spoc_email, spoc_mobile_number=spoc_mobile_number,
                                          spoc_extension_number=spoc_extension, spoc_office_number=spoc_office_number,
                                          centre_mobile_number_1=centre_mobile_number_1,
                                          centre_mobile_number_2=centre_mobile_number_2,
                                          centre_office_number=centre_office_number,
                                          centre_extension_number=centre_extension_number, centre_email=centre_email,
                                          centre_web_address=centre_web_address)
            messages.success(request, message="Centre Registered. Waiting For Approval From Admin!")
            return redirect(register_centre)
        else:
            print(rf.errors)
            return HttpResponse(rf.errors)
    else:
        rf = register_centre_form()
    return render(request, 'static_files/register_centre.html', {'form': rf})


def receptionist_dashboard(request):
    return render(request, 'static_files/dashboard_receptionist.html')


def appointment_list(request):
    appoin_list = Appointment.objects.all()
    delete_old_slots(current_time.date())
    if request.method == "POST":
        s_by_name = request.POST['s_by_name']
        p_by_name = request.POST['p_by_name']
        if s_by_name:
            stu = s_by_name.split(' ')
            for s_n in stu:
                appoin_list = appoin_list.filter(child__first_name__icontains=s_n)
                print(appoin_list)
                if not appoin_list:
                    appoin_list = Appointment.objects.filter(child__last_name__icontains=s_n)
                else:
                    pass
        if p_by_name:
            psy = p_by_name.split(' ')
            for p_n in psy:
                appoin_list = appoin_list.filter(psychologist__first_name__icontains=p_n)
                if not appoin_list:
                    appoin_list = Appointment.objects.filter(psychologist_last_name__icontains=p_n)
                else:
                    pass
    return render(request, 'static_files/appointment_list.html', {'objs': appoin_list})


weekdays = {'0': 'm', '1': 'tu', '2': 'w', '3': 'th', '4': 'f', '5': 'sa',
            '6': 'su'}


def add_appointment(request):
    if request.method == "POST":
        af = add_appointment_form(request.POST)
        if af.is_valid():
            appointment_date = af.cleaned_data['appointment_date']
            psychologist_name = request.POST['psy']
            child_name = request.POST['child']

            if not psychologist_name or not child_name:
                messages.warning(request, message="Fill All fields Please")
                return redirect(add_appointment)

            full_name_psy = psychologist_name.split(' ')
            psy = Person.objects.get(first_name=full_name_psy[0])
            full_name_child = child_name.split(' ')
            child = Person.objects.get(first_name=full_name_child[0])

            d = appointment_date.split('/')
            datee = datetime.datetime(int(d[2]), int(d[1]), int(d[0]))
            if datee.date() < datetime.datetime.now().date():
                messages.warning(request, message="Add date Ahead of today")
                return redirect(add_appointment)
            if datee.date().weekday() == 4:
                messages.warning(request, message="Friday is OFF")
                return redirect(add_appointment)
            return redirect(check_slots, psy.id, child.id, datee.date())
        else:
            messages.warning(request, message=af.errors)
            return redirect(add_appointment)
    af = add_appointment_form()
    p = Person.objects.filter(role__name="Physiologist")
    students = Person.objects.filter(role__name="Student")
    return render(request, 'static_files/add_appointment.html', {'form': af, 'psys': p, 'students': students})


def check_slots(request, id1, id2, date):
    da = date.split('-')
    daat = datetime.datetime(int(da[0]), int(da[1]), int(da[2])).date()
    delete_old_slots(current_time.date())
    psy = Person.objects.get(id=id1)
    child = Person.objects.get(id=id2)
    slotss = Slot.objects.filter(psychologist_id=id1, day=date)
    x = current_time + timezone.timedelta(hours=2)
    # print(x.time())
    two_hours = int(str(x.time()).split(':')[0])
    if slotss:
        slotss = Slot.objects.filter(psychologist_id=id1, day=date, available=True)
        if str(current_time.date()) == str(date):
            for slot in slotss:
                slot_time = int(str(slot.s_time).split(':')[0])
                print(slot_time, two_hours)
                if slot_time < two_hours or two_hours == 0 or two_hours == 1:
                    slotss = slotss.exclude(id=slot.id)
    else:
        d = date.split('-')
        datee = datetime.datetime(int(d[0]), int(d[1]), int(d[2]))
        weekday = datee.date().weekday()
        create_slots(id1, weekday=weekday, day=date)
        slotss = Slot.objects.filter(psychologist_id=id1, day=date, available=True)
        if current_time.date() == date:
            for slot in slotss:
                slot_time = int(str(slot.s_time).split(':')[0])
                if slot_time < two_hours:
                    slotss = slotss.exclude(id=slot.id)

    return render(request, 'static_files/check_slots.html', {'slots': slotss, 'psy': psy, 'date': daat, 'child': child,
                                                             'true_date': date})


def success(request):
    return render(request, 'static_files/success.html')


def search_psy(request):
    psys = ''
    if request.method == "POST":
        id = request.POST['search_by_id']
        name = request.POST['search_by_name']
        if id:
            psys = Person.objects.filter(role__name="Physiologist", id=id)
        elif name:
            name = name.split(" ")
            for n in name:
                psys = Person.objects.filter(role__name="Physiologist", first_name__icontains=n)
                if not psys:
                    psys = Person.objects.filter(role__name="Physiologist", last_name__icontains=n)
    else:
        psys = Person.objects.filter(role__name="Physiologist")
    return render(request, 'static_files/search_psy.html', {'psys': psys})


def availability(request, id):
    p = Person.objects.get(id=id, role__name="Physiologist")
    ava = Availability.objects.get(psychologist=p)
    return render(request, 'static_files/availability_psy.html', {'ava': ava, 'psy': p})


def availability_edit(request, id):
    dic = {}
    p = Person.objects.get(id=id, role__name="Physiologist")
    ava = Availability.objects.get(psychologist=p)
    dic['m_from'] = str(ava.m_available_time_from)
    dic['m_to'] = str(ava.m_available_time_to)
    dic['tu_from'] = str(ava.tu_available_time_from)
    dic['tu_to'] = str(ava.tu_available_time_to)
    dic['w_from'] = str(ava.w_available_time_from)
    dic['w_to'] = str(ava.w_available_time_to)
    dic['th_from'] = str(ava.th_available_time_from)
    dic['th_to'] = str(ava.th_available_time_to)
    # dic['f_from'] = str(ava.f_available_time_from)
    # dic['f_to'] = str(ava.f_available_time_to)
    dic['sa_from'] = str(ava.sa_available_time_from)
    dic['sa_to'] = str(ava.sa_available_time_to)
    dic['su_from'] = str(ava.su_available_time_from)
    dic['su_to'] = str(ava.su_available_time_to)

    if request.method == "POST":
        m_from = request.POST['1-stime']
        m_to = request.POST['1-ftime']
        tu_from = request.POST['2-stime']
        tu_to = request.POST['2-ftime']
        w_from = request.POST['3-stime']
        w_to = request.POST['3-ftime']
        th_from = request.POST['4-stime']
        th_to = request.POST['4-ftime']
        # f_from = request.POST['5-stime']
        # f_to = request.POST['5-ftime']
        sa_from = request.POST['6-stime']
        sa_to = request.POST['6-ftime']
        su_from = request.POST['7-stime']
        su_to = request.POST['7-ftime']

        if m_from: ava.m_available_time_from = m_from
        if m_to: ava.m_available_time_to = m_to
        if tu_from: ava.tu_available_time_from = tu_from
        if tu_to: ava.tu_available_time_to = tu_to
        if w_from: ava.w_available_time_from = w_from
        if w_to: ava.w_available_time_to = w_to
        if th_from: ava.th_available_time_from = th_from
        if th_to: ava.th_available_time_to = th_to
        # if f_from: ava.f_available_time_from = f_from
        # if f_to: ava.f_available_time_to = f_to
        if sa_from: ava.sa_available_time_from = sa_from
        if sa_to: ava.sa_available_time_to = sa_to
        if su_from: ava.su_available_time_from = su_from
        if su_to: ava.su_available_time_to = su_to
        ava.save()

        return redirect(availability, id)
    return render(request, 'static_files/availability_psy_edit.html', {'dic': dic, 'psy': p})


def create_slots(id, weekday, day):
    slots = []
    ava = Availability.objects.get(psychologist_id=id)
    f = f'{weekdays[str(weekday)]}_available_time_from'
    t = f'{weekdays[str(weekday)]}_available_time_to'
    from_time = getattr(ava, f)
    to_time = getattr(ava, t)
    r = to_time.hour - from_time.hour
    y = from_time.hour
    for x in range(int(r / 2)):
        if y < 10:
            if y + 2 < 10:
                slots.append(f'0{y}:00-0{y + 2}:00')
            else:
                slots.append(f'0{y}:00-{y + 2}:00')
        else:
            slots.append(f'{y}:00-{y + 2}:00')
        y += 2
    for slot in slots:
        Slot.objects.create(psychologist_id=id, day=day, s_time=slot.split('-')[0], e_time=slot.split('-')[1],
                            available=True)
    return


def delete_old_slots(date):
    slots = Slot.objects.filter(day__lt=date)
    for slot in slots:
        slot.delete()
    appoints = Appointment.objects.filter(appointment_date__lt=date)
    for appoint in appoints:
        appoint.delete()


def confirm_appointment(request, id1, id2, date, time_s, time_e):
    child = Person.objects.get(id=id2)
    children = Person.objects.filter(role__name="Student").exclude(id=id2)
    psy = Person.objects.get(id=id1)
    da = date.split('-')
    daat = datetime.datetime(int(da[0]), int(da[1]), int(da[2])).date()

    if request.method == "POST":
        count = Appointment.objects.filter(child_id=id2).count()
        if count == 0:
            Appointment.objects.create(psychologist_id=id1, child_id=id2, appointment_date=date,
                                       appointment_s_time=time_s,
                                       appointment_e_time=time_e, status=True)
            slot = Slot.objects.get(psychologist_id=id1, day=date, s_time=time_s, e_time=time_e)
            if slot.available == False:
                messages.warning(request, "Slot not available, Kindly select slot again")
                return redirect(check_slots, id1, id2, date)
            else:
                slot.available = False
                slot.save()
                messages.success(request, message="Appointment Added")
                return redirect(appointment_list)
        else:
            appoint = Appointment.objects.get(child_id=id2)
            slot = Slot.objects.get(psychologist_id=appoint.psychologist.id, day=appoint.appointment_date,
                                    s_time=appoint.appointment_s_time, e_time=appoint.appointment_e_time)
            slot.available = True
            slot.save()
            appoint.psychologist_id = id1
            appoint.child_id = id2
            appoint.appointment_date = date
            appoint.appointment_s_time = time_s
            appoint.appointment_e_time = time_e
            appoint.save()
            slot = Slot.objects.get(psychologist_id=id1, day=date, s_time=time_s, e_time=time_e)
            if slot.available == False:
                messages.warning(request, "Slot not available, Kindly select slot again")
                return redirect(check_slots, id1, id2, date)
            else:
                slot.available = False
                slot.save()
                messages.success(request, message="Appointment Added")
                return redirect(add_appointment)

    return render(request, 'static_files/confirm_appointment.html', {'child': child, 'children': children, 'psy': psy,
                                                                     'date': daat, 'time_s': time_s, 'time_e': time_e})


def delete_appointment(request, id):
    appoin = Appointment.objects.get(id=id)
    psy = Person.objects.get(id=appoin.psychologist_id)
    slot = Slot.objects.get(psychologist_id=psy.id, day=appoin.appointment_date, s_time=appoin.appointment_s_time,
                            e_time=appoin.appointment_e_time)
    slot.available = True
    slot.save()
    appoin.delete()
    return redirect(appointment_list)


def rescheudle(request, id):
    appoin = Appointment.objects.get(id=id)
    psy = Person.objects.filter(role__name="Physiologist").exclude(id=appoin.psychologist_id)
    if request.method == "POST":
        appointment_date = request.POST['appointment_date']
        psy_name = request.POST['psy']
        full_name_psy = psy_name.split(' ')
        psy = Person.objects.get(first_name=full_name_psy[0])

        if not appointment_date:
            messages.warning(request, message="Kindly Select the date")
            return redirect(rescheudle, id)

        d = appointment_date.split('/')
        datee = datetime.datetime(int(d[2]), int(d[1]), int(d[0]))
        if datee.date() < datetime.datetime.now().date():
            messages.warning(request, message="Add date Ahead of today")
            return redirect(rescheudle, id)
        if datee.date().weekday() == 4:
            messages.warning(request, message="Friday is OFF")
            return redirect(rescheudle, id)
        return redirect(check_slots, psy.id, appoin.child.id, datee.date())

    return render(request, 'static_files/reshedule.html', {'appointment': appoin, 'psy': psy})


def is_none(field):
    if field is None:
        return True
    else:
        return False


def format_date_model(date):
    splitted = date.split('/')
    return f'{splitted[2]}-{splitted[1]}-{splitted[0]}'


def format_date_html(date):
    splitted = str(date).split('-')
    return f'{splitted[2]}/{splitted[1]}/{splitted[0]}'


def child_case(request, child_name):
    appoin = Appointment.objects.get(child__username=child_name)
    cc = ''
    count = Child_Case_Data.objects.filter(child__username=child_name).count()
    if request.method == "POST":
        child_form = child_case_form(request.POST)
        if child_form.is_valid():
            # Get data
            civil_number = child_form.cleaned_data['civil_number']
            school_name = child_form.cleaned_data['school_name']
            dob = child_form.cleaned_data['dob']
            place_of_birth = child_form.cleaned_data['place_of_birth']
            nationality = child_form.cleaned_data['nationality']
            grade = child_form.cleaned_data['grade']
            gender = request.POST['gender']

            father_name = child_form.cleaned_data['father_name']
            age_f = child_form.cleaned_data['age_f']
            nationality_f = child_form.cleaned_data['nationality_f']
            education_level_f = child_form.cleaned_data['education_level_f']
            phone_f = child_form.cleaned_data['phone_f']
            current_occupation_f = child_form.cleaned_data['current_occupation_f']
            residence_address_f = child_form.cleaned_data['residence_address_f']
            email_f = child_form.cleaned_data['email_f']

            mother_name = child_form.cleaned_data['mother_name']
            age_m = child_form.cleaned_data['age_m']
            nationality_m = child_form.cleaned_data['nationality_m']
            phone_m = child_form.cleaned_data['phone_m']
            education_level_m = child_form.cleaned_data['education_level_m']
            current_occupation_m = child_form.cleaned_data['current_occupation_m']
            residence_address_m = child_form.cleaned_data['residence_address_m']
            email_m = child_form.cleaned_data['email_m']

            guardian_name = child_form.cleaned_data['guardian_name']
            education_level_g = child_form.cleaned_data['education_level_g']
            relation_to_child = child_form.cleaned_data['relation_to_child']
            phone_g = child_form.cleaned_data['phone_g']
            current_occupation_g = child_form.cleaned_data['current_occupation_g']
            residence_address_g = child_form.cleaned_data['residence_address_g']
            email_g = child_form.cleaned_data['email_g']

            relation_btw_parents = request.POST['relation_btw_parents']
            martial_status_parents = request.POST['martial_status_parents']
            parent_passed_away = request.POST['parent_passed_away']
            child_living_with = child_form.cleaned_data['child_living_with']
            father_married_before = request.POST['father_married_before']
            mother_married_before = request.POST['mother_married_before']
            when_was_married = request.POST['when_was_married']
            second_marriage = request.POST['second_marriage']
            nationality_second_marriage = child_form.cleaned_data['nationality_second_marriage']
            number_of_family_members = child_form.cleaned_data['number_of_family_members']
            number_of_brothers = child_form.cleaned_data['number_of_brothers']
            number_of_sisters = child_form.cleaned_data['number_of_sisters']
            number_of_brothers_from_father = child_form.cleaned_data['number_of_brothers_from_father']
            number_of_sisters_from_father = child_form.cleaned_data['number_of_sisters_from_father']
            number_of_brothers_from_mother = child_form.cleaned_data['number_of_brothers_from_mother']
            number_of_sisters_from_mother = child_form.cleaned_data['number_of_sisters_from_mother']
            order_sibling = child_form.cleaned_data['order_sibling']
            others_living_in_house = child_form.cleaned_data['others_living_in_house']
            lives_with = child_form.cleaned_data['lives_with']

            if count == 0:
                child = Person.objects.get(username=child_name)
                Child_Case_Data.objects.create(child=child, civil_number=civil_number, school_name=school_name,
                                               dob=format_date_model(dob), place_of_birth=place_of_birth,
                                               nationality=nationality, grade=grade, gender=gender, f_name=father_name,
                                               f_age=age_f, f_nationality=nationality_f, f_phone=phone_f,
                                               f_education_level=education_level_f, f_occupation=current_occupation_f,
                                               f_address=residence_address_f, f_email=email_f, m_name=mother_name,
                                               m_age=age_m, m_nationality=nationality_m, m_phone=phone_m,
                                               m_education_level=education_level_m, m_occupation=current_occupation_m,
                                               m_address=residence_address_m, m_email=email_m, g_name=guardian_name,
                                               g_education_level=education_level_g, g_relation_child=relation_to_child,
                                               g_phone=phone_g, g_occupation=current_occupation_g,
                                               g_address=residence_address_g, g_email=email_g,
                                               relation_btw_parents=relation_btw_parents,
                                               martial_status=martial_status_parents, passed_away=parent_passed_away,
                                               living_in_case=child_living_with, father_married=father_married_before,
                                               mother_married=mother_married_before, married_when=when_was_married,
                                               second_marriage=second_marriage,
                                               nationality_sec_m=nationality_second_marriage,
                                               number_of_fam=number_of_family_members,
                                               number_of_bros=number_of_brothers,
                                               number_of_sis=number_of_sisters,
                                               number_of_bros_f=number_of_brothers_from_father,
                                               number_of_sis_f=number_of_sisters_from_father,
                                               number_of_bros_m=number_of_brothers_from_mother,
                                               number_of_sis_m=number_of_sisters_from_mother,
                                               order_sib=order_sibling, other_people_house=others_living_in_house,
                                               lives_current=lives_with
                                               )
            else:
                cc = Child_Case_Data.objects.get(child__username=child_name)
                cc.civil_number = civil_number
                cc.school_name = school_name
                cc.dob = format_date_model(dob)
                cc.place_of_birth = place_of_birth
                cc.nationality = nationality
                cc.grade = grade
                cc.gender = gender
                cc.f_name = father_name
                cc.f_age = age_f
                cc.f_nationality = nationality_f
                cc.f_phone = phone_f
                cc.f_education_level = education_level_f
                cc.f_occupation = current_occupation_f
                cc.f_address = residence_address_f
                cc.f_email = email_f
                cc.m_name = mother_name
                cc.m_age = age_m
                cc.m_nationality = nationality_m
                cc.m_phone = phone_m
                cc.m_education_level = education_level_m
                cc.m_occupation = current_occupation_m
                cc.m_address = residence_address_m
                cc.m_email = email_f
                cc.g_name = guardian_name
                cc.g_education_level = education_level_g
                cc.g_relation_child = relation_to_child
                cc.g_phone = phone_g
                cc.g_occupation = current_occupation_g
                cc.g_address = residence_address_g
                cc.g_email = email_g
                cc.relation_btw_parents = relation_btw_parents
                cc.martial_status = martial_status_parents
                cc.passed_away = parent_passed_away
                cc.living_in_case = child_living_with
                cc.father_married = father_married_before
                cc.mother_married = mother_married_before
                cc.second_marriage = second_marriage
                cc.nationality_sec_m = nationality_second_marriage
                cc.number_of_fam = number_of_family_members
                cc.number_of_bros = number_of_brothers
                cc.number_of_sis = number_of_sisters
                cc.number_of_bros_f = number_of_brothers_from_father
                cc.number_of_sis_f = number_of_sisters_from_father
                cc.number_of_bros_m = number_of_brothers_from_mother
                cc.number_of_sis_m = number_of_sisters_from_mother
                cc.order_sib = order_sibling
                cc.other_people_house = others_living_in_house
                cc.lives_current = lives_with

                cc.save()

            if 'next' in request.POST:
                return redirect(cc_child_history, child_name)
            elif 'step2' in request.POST:
                return redirect(cc_child_history, child_name)
            elif 'step3' in request.POST:
                return redirect(cc_condition, child_name)
            elif 'step4' in request.POST:
                return redirect(cc_stages_of_growth, child_name)
            elif 'step5' in request.POST:
                return redirect(cc_family_history, child_name)
            elif 'step6' in request.POST:
                return redirect(cc_social_development, child_name)
            elif 'step7' in request.POST:
                return redirect(cc_child_beh, child_name)
            elif 'step8' in request.POST:
                return redirect(cc_school_history, child_name)
            elif 'step9' in request.POST:
                return redirect(cc_diff_info, child_name)
            elif 'step10' in request.POST:
                return redirect(cc_other_info, child_name)

        else:
            print(child_form.errors)
    else:
        child_form = child_case_form()
        if count != 0:
            cc = Child_Case_Data.objects.get(child__username=child_name)
            cc.dob = format_date_html(cc.dob)

    return render(request, 'static_files/child-case.html', {'obj': appoin, 'form': child_form, 'cc': cc})


def cc_child_history(request, child_name):
    appoin = Appointment.objects.get(child__username=child_name)
    cc = ''
    if request.method == "POST":
        child_form = child_case_form(request.POST)
        if child_form.is_valid():
            # Get data
            state_of_mind_preg = child_form.cleaned_data['state_of_mind_preg']
            age_during_preg = child_form.cleaned_data['age_during_preg']
            health_psy_preg = child_form.cleaned_data['health_psy_preg']
            preg_bleeding = request.POST['preg_bleeding']
            preg_poisoning = request.POST['preg_poisoning']
            preg_infection = request.POST['preg_infection']
            preg_accident = request.POST['preg_accident']
            kind_of_accident_preg = child_form.cleaned_data['kind_of_accident_preg']
            medicines_drugs_preg = child_form.cleaned_data['medicines_drugs_preg']
            prob_disease_preg = child_form.cleaned_data['prob_disease_preg']
            duration_preg = request.POST['duration_preg']
            preg_month = request.POST['preg_month']
            birth_type = request.POST['birth_type']
            umbilical_cord_neck = request.POST['umbilical_cord_neck']
            skin_yellow = request.POST['skin_yellow']
            skin_blue = request.POST['skin_blue']
            twin_triplet = request.POST['twin_triplet']
            oxygen_deficiency = request.POST['oxygen_deficiency']
            colic_cramps = request.POST['colic_cramps']
            dropsy_edema_hydrops = request.POST['dropsy_edema_hydrops']

            baby_weight_birth = child_form.cleaned_data['baby_weight_birth']
            prob_birth = child_form.cleaned_data['prob_birth']
            complications_birth = child_form.cleaned_data['complications_birth']

            health_psy_post_b = child_form.cleaned_data['health_psy_post_b']
            baby_incubator = request.POST['baby_incubator']
            period_incubator = child_form.cleaned_data['period_incubator']
            surgery_baby = child_form.cleaned_data['surgery_baby']

            cc = Child_Case_Data.objects.get(child__username=child_name)
            cc.state_of_m = state_of_mind_preg
            cc.p_m_age = age_during_preg
            cc.m_health = health_psy_preg
            cc.p_bleeding = preg_bleeding
            cc.p_poisoning = preg_poisoning
            cc.p_infection = preg_infection
            cc.p_accident = preg_accident
            cc.p_accident_detail = kind_of_accident_preg
            cc.p_medicines = medicines_drugs_preg
            cc.p_problems = prob_disease_preg
            cc.p_duration = duration_preg
            cc.p_month = preg_month
            cc.type_birth = birth_type
            cc.umbilical_cord = umbilical_cord_neck
            cc.skin_yellow = skin_yellow
            cc.skin_blue = skin_blue
            cc.twin_trip = twin_triplet
            cc.needed_oxy = oxygen_deficiency
            cc.colic_cramps = colic_cramps
            cc.dropsy = dropsy_edema_hydrops
            cc.baby_weight = baby_weight_birth
            cc.b_problems = prob_birth
            cc.b_complications = complications_birth
            cc.health_m_pb = health_psy_post_b
            cc.incubator = baby_incubator
            cc.incubator_period = period_incubator
            cc.b_surgery = surgery_baby

            cc.save()

            if 'prev' in request.POST:
                return redirect(child_case, child_name)
            elif 'next' in request.POST:
                return redirect(cc_condition, child_name)
            elif 'step1' in request.POST:
                return redirect(child_case, child_name)
            elif 'step3' in request.POST:
                return redirect(cc_condition, child_name)
            elif 'step4' in request.POST:
                return redirect(cc_stages_of_growth, child_name)
            elif 'step5' in request.POST:
                return redirect(cc_family_history, child_name)
            elif 'step6' in request.POST:
                return redirect(cc_social_development, child_name)
            elif 'step7' in request.POST:
                return redirect(cc_child_beh, child_name)
            elif 'step8' in request.POST:
                return redirect(cc_school_history, child_name)
            elif 'step9' in request.POST:
                return redirect(cc_diff_info, child_name)
            elif 'step10' in request.POST:
                return redirect(cc_other_info, child_name)
        else:
            print(child_form.errors)
    else:
        child_form = child_case_form()
        cc = Child_Case_Data.objects.get(child__username=child_name)
    return render(request, 'static_files/cc_development_of_child.html', {'obj': appoin, 'form': child_form, 'cc': cc})


def cc_condition(request, child_name):
    appoin = Appointment.objects.get(child__username=child_name)
    cc = ''
    if request.method == "POST":
        child_form = child_case_form(request.POST)
        if child_form.is_valid():
            # Get data
            extremely_high_temp_age = child_form.cleaned_data['extremely_high_temp_age']
            extremely_high_temp_dur = child_form.cleaned_data['extremely_high_temp_dur']
            ear_problems_age = child_form.cleaned_data['ear_problems_age']
            ear_problems_dur = child_form.cleaned_data['ear_problems_dur']
            vision_problems_age = child_form.cleaned_data['vision_problems_age']
            vision_problems_dur = child_form.cleaned_data['vision_problems_dur']
            juandice_age = child_form.cleaned_data['juandice_age']
            juandice_dur = child_form.cleaned_data['juandice_dur']
            asthma_age = child_form.cleaned_data['asthma_age']
            asthma_dur = child_form.cleaned_data['asthma_dur']
            allergy_age = child_form.cleaned_data['allergy_age']
            allergy_dur = child_form.cleaned_data['allergy_dur']
            poisoning_age = child_form.cleaned_data['poisoning_age']
            poisoning_dur = child_form.cleaned_data['poisoning_dur']
            surgical_age = child_form.cleaned_data['surgical_age']
            surgical_dur = child_form.cleaned_data['surgical_dur']
            surgery = child_form.cleaned_data['surgery']
            accident_age = child_form.cleaned_data['accident_age']
            accident_dur = child_form.cleaned_data['accident_dur']
            accident = child_form.cleaned_data['accident']
            not_mentioned_disease = child_form.cleaned_data['not_mentioned_disease']

            cc = Child_Case_Data.objects.get(child__username=child_name)
            cc.extremely_high_temp_age = extremely_high_temp_age
            cc.extremely_high_temp_dur = extremely_high_temp_dur
            cc.ear_problems_age = ear_problems_age
            cc.ear_problems_dur = ear_problems_dur
            cc.vision_problems_age = vision_problems_age
            cc.vision_problems_dur = vision_problems_dur
            cc.juandice_age = juandice_age
            cc.juandice_dur = juandice_dur
            cc.asthma_age = asthma_age
            cc.asthma_dur = asthma_dur
            cc.allergy_age = allergy_age
            cc.allergy_dur = allergy_dur
            cc.poisoning_age = poisoning_age
            cc.poisoning_dur = poisoning_dur
            cc.surgical_age = surgical_age
            cc.surgical_dur = surgical_dur
            cc.surgery = surgery
            cc.accident_age = accident_age
            cc.accident_dur = accident_dur
            cc.accident = accident
            cc.not_mentioned_disease = not_mentioned_disease

            cc.save()

            if 'prev' in request.POST:
                return redirect(cc_child_history, child_name)
            elif 'next' in request.POST:
                return redirect(cc_stages_of_growth, child_name)
            elif 'step1' in request.POST:
                return redirect(child_case, child_name)
            elif 'step2' in request.POST:
                return redirect(cc_child_history, child_name)
            elif 'step4' in request.POST:
                return redirect(cc_stages_of_growth, child_name)
            elif 'step5' in request.POST:
                return redirect(cc_family_history, child_name)
            elif 'step6' in request.POST:
                return redirect(cc_social_development, child_name)
            elif 'step7' in request.POST:
                return redirect(cc_child_beh, child_name)
            elif 'step8' in request.POST:
                return redirect(cc_school_history, child_name)
            elif 'step9' in request.POST:
                return redirect(cc_diff_info, child_name)
            elif 'step10' in request.POST:
                return redirect(cc_other_info, child_name)
        else:
            print(child_form.errors)
    else:
        child_form = child_case_form()
        cc = Child_Case_Data.objects.get(child__username=child_name)
    return render(request, 'static_files/cc_condition.html', {'obj': appoin, 'form': child_form, 'cc': cc})


def cc_stages_of_growth(request, child_name):
    appoin = Appointment.objects.get(child__username=child_name)
    cc = ''
    if request.method == "POST":
        child_form = child_case_form(request.POST)
        if child_form.is_valid():
            # Get data
            breastfeeding = request.POST['breastfeeding']
            weaning_age = child_form.cleaned_data['weaning_age']
            age_tooth_start = child_form.cleaned_data['age_tooth_start']
            age_commune = child_form.cleaned_data['age_commune']
            age_simple_words = child_form.cleaned_data['age_simple_words']
            age_speech = child_form.cleaned_data['age_speech']
            age_sentence = child_form.cleaned_data['age_sentence']
            age_bottle_carry = child_form.cleaned_data['age_bottle_carry']
            age_love = child_form.cleaned_data['age_love']
            age_sat = child_form.cleaned_data['age_sat']
            age_stop = child_form.cleaned_data['age_stop']
            age_walk = child_form.cleaned_data['age_walk']
            age_wore_help = child_form.cleaned_data['age_wore_help']
            age_wore_self = child_form.cleaned_data['age_wore_self']
            age_shoes = child_form.cleaned_data['age_shoes']
            age_feed = child_form.cleaned_data['age_feed']
            age_urination = child_form.cleaned_data['age_urination']
            age_bathroom_train = child_form.cleaned_data['age_bathroom_train']
            visual_probs = request.POST['visual_probs']
            use_glasses = request.POST['use_glasses']
            age_glasses = child_form.cleaned_data['age_glasses']
            hearing_probs = request.POST['hearing_probs']
            hearing_aid = request.POST['hearing_aid']
            age_hearing_aid = child_form.cleaned_data['age_hearing_aid']
            speaking_difficulty = request.POST['speaking_difficulty']
            treated_speech_centres = request.POST['treated_speech_centres']
            age_speech_centre = child_form.cleaned_data['age_speech_centre']
            hand = request.POST['hand']
            leg = request.POST['leg']
            both_hand = request.POST['both_hand']
            stop_left_hand = request.POST['stop_left_hand']
            age_stop_left_hand = child_form.cleaned_data['age_stop_left_hand']
            involuntary_urination = request.POST['involuntary_urination']
            cause_involuntary_urination = request.POST['cause_involuntary_urination']
            age_involutary_urination = child_form.cleaned_data['age_involutary_urination']
            medicines_bool = request.POST['medicines_bool']
            medicine_name = child_form.cleaned_data['medicine_name']
            medicine_reason = child_form.cleaned_data['medicine_reason']
            appetite = child_form.cleaned_data['appetite']
            fav_food = child_form.cleaned_data['fav_food']

            cc = Child_Case_Data.objects.get(child__username=child_name)
            cc.breastfeeding = breastfeeding
            cc.age_weaning = weaning_age
            cc.age_teething = age_tooth_start
            cc.age_commune = age_commune
            cc.age_pronouncing = age_simple_words
            cc.age_speech = age_speech
            cc.age_full_sentence = age_sentence
            cc.age_bottle_milk = age_bottle_carry
            cc.age_love = age_love
            cc.age_sat_self = age_sat
            cc.age_stop_self = age_stop
            cc.age_walking = age_walk
            cc.age_wearing_help = age_wore_help
            cc.age_wearing_self = age_wore_self
            cc.age_shoes = age_shoes
            cc.age_feeding = age_feed
            cc.age_urination = age_urination
            cc.age_bathroom = age_bathroom_train
            cc.visual_prob = visual_probs
            cc.use_glasses = use_glasses
            cc.age_glasses = age_glasses
            cc.hearing_prob = hearing_probs
            cc.use_hearing_aid = hearing_aid
            cc.age_hearing_aid = age_hearing_aid
            cc.diff_speaking = speaking_difficulty
            cc.treated_speech = treated_speech_centres
            cc.age_treated_speech = age_speech_centre
            cc.hand_writing = hand
            cc.leg_kicking = leg
            cc.both_hands = both_hand
            cc.stop_left_hand = stop_left_hand
            cc.age_stop_left_hand = age_stop_left_hand
            cc.involuntary_urination = involuntary_urination
            cc.cause_involuntary_urination = cause_involuntary_urination
            cc.age_involuntary_urination = age_involutary_urination
            cc.medicines_bool = medicines_bool
            cc.medicines_name = medicine_name
            cc.medicine_reason = medicine_reason
            cc.eating_habits = appetite
            cc.fav_food = fav_food

            cc.save()

            if 'prev' in request.POST:
                return redirect(cc_condition, child_name)
            elif 'next' in request.POST:
                return redirect(cc_family_history, child_name)
            elif 'step1' in request.POST:
                return redirect(child_case, child_name)
            elif 'step2' in request.POST:
                return redirect(cc_child_history, child_name)
            elif 'step3' in request.POST:
                return redirect(cc_condition, child_name)
            elif 'step5' in request.POST:
                return redirect(cc_family_history, child_name)
            elif 'step6' in request.POST:
                return redirect(cc_social_development, child_name)
            elif 'step7' in request.POST:
                return redirect(cc_child_beh, child_name)
            elif 'step8' in request.POST:
                return redirect(cc_school_history, child_name)
            elif 'step9' in request.POST:
                return redirect(cc_diff_info, child_name)
            elif 'step10' in request.POST:
                return redirect(cc_other_info, child_name)
        else:
            print(child_form.errors)
    else:
        child_form = child_case_form()
        cc = Child_Case_Data.objects.get(child__username=child_name)
    return render(request, 'static_files/cc_stages_of_growth.html', {'obj': appoin, 'form': child_form, 'cc': cc})


def cc_family_history(request, child_name):
    appoin = Appointment.objects.get(child__username=child_name)
    cc = ''
    if request.method == "POST":
        child_form = child_case_form(request.POST)
        if child_form.is_valid():
            # Get data
            hyperinactivity = child_form.cleaned_data['hyperinactivity']
            reading = child_form.cleaned_data['reading']
            writing_dictating = child_form.cleaned_data['writing_dictating']
            calculating = child_form.cleaned_data['calculating']
            concentration = child_form.cleaned_data['concentration']
            pronouncing = child_form.cleaned_data['pronouncing']
            hearing = child_form.cleaned_data['hearing']
            visual = child_form.cleaned_data['visual']
            mobility = child_form.cleaned_data['mobility']
            intellectual = child_form.cleaned_data['intellectual']
            down_syndrome = child_form.cleaned_data['down_syndrome']
            autism = child_form.cleaned_data['autism']
            other_problems = child_form.cleaned_data['other_problems']
            child_hereditary = request.POST['child_hereditary']
            age_discovered = child_form.cleaned_data['age_discovered']
            effecting_child = child_form.cleaned_data['effecting_child']

            cc = Child_Case_Data.objects.get(child__username=child_name)
            cc.hyperinactivity = hyperinactivity
            cc.reading_diff = reading
            cc.writing_dictating_diff = writing_dictating
            cc.calculating_diff = calculating
            cc.concentration_diff = concentration
            cc.pronouncing_diff = pronouncing
            cc.impaired_hearing = hearing
            cc.visual_impairment = visual
            cc.impaired_mobility = mobility
            cc.intellectual_disability = intellectual
            cc.down_syn = down_syndrome
            cc.autism = autism
            cc.other_prob = other_problems
            cc.child_hereditary = child_hereditary
            cc.age_problem = age_discovered
            cc.prob_effect = effecting_child

            cc.save()

            if 'prev' in request.POST:
                return redirect(cc_stages_of_growth, child_name)
            elif 'next' in request.POST:
                return redirect(cc_social_development, child_name)
            elif 'step1' in request.POST:
                return redirect(child_case, child_name)
            elif 'step2' in request.POST:
                return redirect(cc_child_history, child_name)
            elif 'step3' in request.POST:
                return redirect(cc_condition, child_name)
            elif 'step4' in request.POST:
                return redirect(cc_stages_of_growth, child_name)
            elif 'step6' in request.POST:
                return redirect(cc_social_development, child_name)
            elif 'step7' in request.POST:
                return redirect(cc_child_beh, child_name)
            elif 'step8' in request.POST:
                return redirect(cc_school_history, child_name)
            elif 'step9' in request.POST:
                return redirect(cc_diff_info, child_name)
            elif 'step10' in request.POST:
                return redirect(cc_other_info, child_name)
        else:
            print(child_form.errors)
    else:
        child_form = child_case_form()
        cc = Child_Case_Data.objects.get(child__username=child_name)
    return render(request, 'static_files/cc_family_history.html', {'obj': appoin, 'form': child_form, 'cc': cc})


def cc_social_development(request, child_name):
    appoin = Appointment.objects.get(child__username=child_name)
    cc = ''
    if request.method == "POST":
        child_form = child_case_form(request.POST)
        if child_form.is_valid():
            # Get data
            friends = child_form.cleaned_data['friends']
            siblings = child_form.cleaned_data['siblings']
            parents = child_form.cleaned_data['parents']
            adults = child_form.cleaned_data['adults']
            maid = child_form.cleaned_data['maid']
            maid_rel_age = child_form.cleaned_data['maid_rel_age']
            fam_auth = child_form.cleaned_data['fam_auth']
            link_fam = child_form.cleaned_data['link_fam']
            punishment_reward = request.POST['punishment_reward']
            punisher = child_form.cleaned_data['punisher']
            punishment = request.POST['punishment']
            spending_time = child_form.cleaned_data['spending_time']
            hobbies_child = child_form.cleaned_data['hobbies_child']
            m_lang = child_form.cleaned_data['m_lang']
            o_lang = child_form.cleaned_data['o_lang']
            dialects = request.POST['dialects']

            cc = Child_Case_Data.objects.get(child__username=child_name)
            cc.friends = friends
            cc.siblings = siblings
            cc.parents = parents
            cc.adults = adults
            cc.maid = maid
            cc.age_maid = maid_rel_age
            cc.fam_auth = fam_auth
            cc.fam_close = link_fam
            cc.punishment_sys = punishment_reward
            cc.punisher = punisher
            cc.punishment = punishment
            cc.spent_time_in = spending_time
            cc.fav_hobby = hobbies_child
            cc.main_lang = m_lang
            cc.other_lang = o_lang
            cc.dilects = dialects

            cc.save()

            if 'prev' in request.POST:
                return redirect(cc_family_history, child_name)
            elif 'next' in request.POST:
                return redirect(cc_child_beh, child_name)
            elif 'step1' in request.POST:
                return redirect(child_case, child_name)
            elif 'step2' in request.POST:
                return redirect(cc_child_history, child_name)
            elif 'step3' in request.POST:
                return redirect(cc_condition, child_name)
            elif 'step4' in request.POST:
                return redirect(cc_stages_of_growth, child_name)
            elif 'step5' in request.POST:
                return redirect(cc_family_history, child_name)
            elif 'step7' in request.POST:
                return redirect(cc_child_beh, child_name)
            elif 'step8' in request.POST:
                return redirect(cc_school_history, child_name)
            elif 'step9' in request.POST:
                return redirect(cc_diff_info, child_name)
            elif 'step10' in request.POST:
                return redirect(cc_other_info, child_name)
        else:
            print(child_form.errors)
    else:
        child_form = child_case_form()
        cc = Child_Case_Data.objects.get(child__username=child_name)
    return render(request, 'static_files/cc-social-development.html', {'obj': appoin, 'form': child_form, 'cc': cc})


def cc_child_beh(request, child_name):
    appoin = Appointment.objects.get(child__username=child_name)
    cc = ''
    if request.method == "POST":
        child_form = child_case_form(request.POST)
        if child_form.is_valid():
            # Get data
            mental_illness = request.POST['mental_illness']
            mental_illnesses = child_form.cleaned_data['mental_illnesses']
            time_alone = request.POST['time_alone']
            specific_friend = request.POST['specific_friend']
            diff_friend = request.POST['diff_friend']
            quarrel_friends = request.POST['quarrel_friends']
            o_like_play = request.POST['o_like_play']
            o_avoid_play = request.POST['o_avoid_play']
            f_older = request.POST['f_older']
            f_younger = request.POST['f_younger']
            attention_seeker = request.POST['attention_seeker']
            confi_ability = request.POST['confi_ability']
            quite = request.POST['quite']
            impulsive = request.POST['impulsive']
            activity_normal = request.POST['activity_normal']
            cooperative = request.POST['cooperative']
            lies = request.POST['lies']
            moody = request.POST['moody']
            bored = request.POST['bored']
            comp_tasks = request.POST['comp_tasks']
            sad = request.POST['sad']
            cheerful = request.POST['cheerful']
            aggressive = request.POST['aggressive']
            avoid_competition = request.POST['avoid_competition']
            compete_others = request.POST['compete_others']
            lazy = request.POST['lazy']
            leadership = request.POST['leadership']
            autonomy = request.POST['autonomy']
            time_task = request.POST['time_task']
            anxious = request.POST['anxious']
            feel_afraid = request.POST['feel_afraid']

            cc = Child_Case_Data.objects.get(child__username=child_name)
            cc.mental_illness_bool = mental_illness
            cc.mental_illness = mental_illnesses
            cc.spends_time_alone = time_alone
            cc.no_friend = specific_friend
            cc.diff_friend = diff_friend
            cc.quarrels_friend = quarrel_friends
            cc.like_to_play = o_like_play
            cc.avoid_to_play = o_avoid_play
            cc.older_friend = f_older
            cc.younger_friend = f_younger
            cc.seeker_attention = attention_seeker
            cc.confidence_ability = confi_ability
            cc.quite = quite
            cc.impulsive = impulsive
            cc.normal_activity = activity_normal
            cc.cooperative = cooperative
            cc.lies = lies
            cc.moody = moody
            cc.gets_bored = bored
            cc.completes_tasks = comp_tasks
            cc.sad = sad
            cc.cheerful = cheerful
            cc.aggressive = aggressive
            cc.avoid_competition = avoid_competition
            cc.compete_others = compete_others
            cc.lazy = lazy
            cc.leadership = leadership
            cc.self_reliance = autonomy
            cc.long_time_tasks = time_task
            cc.anxious = anxious
            cc.afraid = feel_afraid

            cc.save()

            if 'prev' in request.POST:
                return redirect(cc_social_development, child_name)
            elif 'next' in request.POST:
                return redirect(cc_school_history, child_name)
            elif 'step1' in request.POST:
                return redirect(child_case, child_name)
            elif 'step2' in request.POST:
                return redirect(cc_child_history, child_name)
            elif 'step3' in request.POST:
                return redirect(cc_condition, child_name)
            elif 'step4' in request.POST:
                return redirect(cc_stages_of_growth, child_name)
            elif 'step5' in request.POST:
                return redirect(cc_family_history, child_name)
            elif 'step6' in request.POST:
                return redirect(cc_social_development, child_name)
            elif 'step8' in request.POST:
                return redirect(cc_school_history, child_name)
            elif 'step9' in request.POST:
                return redirect(cc_diff_info, child_name)
            elif 'step10' in request.POST:
                return redirect(cc_other_info, child_name)
        else:
            print(child_form.errors)


    else:
        child_form = child_case_form()
        cc = Child_Case_Data.objects.get(child__username=child_name)
    return render(request, 'static_files/cc_child_beh.html', {'obj': appoin, 'form': child_form, 'cc': cc})


def cc_school_history(request, child_name):
    appoin = Appointment.objects.get(child__username=child_name)
    cc = ''
    if request.method == "POST":
        child_form = child_case_form(request.POST)
        if child_form.is_valid():
            # Get data
            s_name_1 = child_form.cleaned_data['s_name_1']
            s_enroll_1 = child_form.cleaned_data['s_enroll_1']
            s_beh_1 = child_form.cleaned_data['s_beh_1']
            s_name_2 = child_form.cleaned_data['s_name_2']
            s_enroll_2 = child_form.cleaned_data['s_enroll_2']
            s_beh_2 = child_form.cleaned_data['s_beh_2']
            s_name_3 = child_form.cleaned_data['s_name_3']
            s_enroll_3 = child_form.cleaned_data['s_enroll_3']
            s_beh_3 = child_form.cleaned_data['s_beh_3']

            first_stage = child_form.cleaned_data['first_stage']
            stages_failed = request.POST['stages_failed']
            failure_class = child_form.cleaned_data['failure_class']
            failure_subjs = child_form.cleaned_data['failure_subjs']
            private_tutors = request.POST['private_tutors']
            advantage = child_form.cleaned_data['advantage']
            diff_teaching = request.POST['diff_teaching']
            teachers_note = child_form.cleaned_data['teachers_note']
            supervision_teaching = request.POST['supervision_teaching']
            achievement = child_form.cleaned_data['achievement']
            motivation = child_form.cleaned_data['motivation']
            enthusiasm = child_form.cleaned_data['enthusiasm']
            time_punctuality = child_form.cleaned_data['time_punctuality']
            fav_articles = child_form.cleaned_data['fav_articles']
            least_fav_material = child_form.cleaned_data['least_fav_material']
            rel_teachers = child_form.cleaned_data['rel_teachers']
            desire_school = child_form.cleaned_data['desire_school']
            absent_reasons = child_form.cleaned_data['absent_reasons']

            cc = Child_Case_Data.objects.get(child__username=child_name)
            cc.school_name_1 = s_name_1
            cc.enroll_date_1 = format_date_model(s_enroll_1)
            cc.attitude_school_1 = s_beh_1
            cc.school_name_2 = s_name_2
            cc.enroll_date_2 = format_date_model(s_enroll_2)
            cc.attitude_school_2 = s_beh_2
            cc.school_name_3 = s_name_3
            cc.enroll_date_3 = format_date_model(s_enroll_3)
            cc.attitude_school_3 = s_beh_3
            cc.first_stage = first_stage
            cc.failed = stages_failed
            cc.failed_class = failure_class
            cc.failed_subjs = failure_subjs
            cc.private_tutors = private_tutors
            cc.take_advantage = advantage
            cc.difficult_teaching = diff_teaching
            cc.teachers_note = teachers_note
            cc.supervision = supervision_teaching
            cc.academic_achievement = achievement
            cc.motivation = motivation
            cc.enthusiasm = enthusiasm
            cc.time_punctual = time_punctuality
            cc.fav_articles = fav_articles
            cc.least_fav_material = least_fav_material
            cc.rel_teachers = rel_teachers
            cc.desire_school = desire_school
            cc.reason_absent = absent_reasons

            cc.save()

            if 'prev' in request.POST:
                return redirect(cc_child_beh, child_name)
            elif 'next' in request.POST:
                return redirect(cc_diff_info, child_name)
            elif 'step1' in request.POST:
                return redirect(child_case, child_name)
            elif 'step2' in request.POST:
                return redirect(cc_child_history, child_name)
            elif 'step3' in request.POST:
                return redirect(cc_condition, child_name)
            elif 'step4' in request.POST:
                return redirect(cc_stages_of_growth, child_name)
            elif 'step5' in request.POST:
                return redirect(cc_family_history, child_name)
            elif 'step6' in request.POST:
                return redirect(cc_social_development, child_name)
            elif 'step7' in request.POST:
                return redirect(cc_child_beh, child_name)
            elif 'step9' in request.POST:
                return redirect(cc_diff_info, child_name)
            elif 'step10' in request.POST:
                return redirect(cc_other_info, child_name)
        else:
            print(child_form.errors)

    else:
        child_form = child_case_form()
        cc = Child_Case_Data.objects.get(child__username=child_name)
        cc.enroll_date_1 = format_date_html(cc.enroll_date_1)
        cc.enroll_date_2 = format_date_html(cc.enroll_date_2)
        cc.enroll_date_3 = format_date_html(cc.enroll_date_3)
    return render(request, 'static_files/cc_school_history.html', {'obj': appoin, 'form': child_form, 'cc': cc})


def cc_diff_info(request, child_name):
    appoin = Appointment.objects.get(child__username=child_name)
    cc = ''
    if request.method == "POST":
        child_form = child_case_form(request.POST)
        if child_form.is_valid():
            # Get data
            reading_d = request.POST['reading_d']
            dictating_d = request.POST['dictating_d']
            writing_d = request.POST['writing_d']
            remembering_nearby_d = request.POST['remembering_nearby_d']
            recog_time = request.POST['recog_time']
            recog_days = request.POST['recog_days']
            recog_dir = request.POST['recog_dir']
            work_on_time = request.POST['work_on_time']
            focus_attention = request.POST['focus_attention']
            understanding = request.POST['understanding']
            remembering_remote_d = request.POST['remembering_remote_d']
            relationships = request.POST['relationships']
            expressing = request.POST['expressing']
            remembering_d = request.POST['remembering_d']
            blackboard = request.POST['blackboard']
            printed = request.POST['printed']
            flip = request.POST['flip']
            numbers_letters = request.POST['numbers_letters']
            verbal_ins = request.POST['verbal_ins']
            listening = request.POST['listening']
            repeat = request.POST['repeat']
            dis_numbers = request.POST['dis_numbers']
            multiplication = request.POST['multiplication']
            phone_numbers_m = request.POST['phone_numbers_m']
            counting = request.POST['counting']
            add_subt = request.POST['add_subt']
            maths_sym = request.POST['maths_sym']
            size = request.POST['size']

            cc = Child_Case_Data.objects.get(child__username=child_name)
            cc.reading = reading_d
            cc.dictating = dictating_d
            cc.writing = writing_d
            cc.remembering_nearby = remembering_nearby_d
            cc.recog_time = recog_time
            cc.recog_days = recog_days
            cc.recog_directions = recog_dir
            cc.completing_work = work_on_time
            cc.focus_attention = focus_attention
            cc.understanding = understanding
            cc.remembering_remote = remembering_remote_d
            cc.relationships = relationships
            cc.expressing_ideas = expressing
            cc.remembering_skills = remembering_d
            cc.moving_blackboard = blackboard
            cc.copying_printed = printed
            cc.flip_words = flip
            cc.confuses_numbers = numbers_letters
            cc.understanding_verbal = verbal_ins
            cc.learning_listening = listening
            cc.repeat_instruction = repeat
            cc.distinguish_numbers = dis_numbers
            cc.memorizing_multiplication = multiplication
            cc.memorizing_phone = phone_numbers_m
            cc.counting_up = counting
            cc.performing_add_subt = add_subt
            cc.understanding_mathematical = maths_sym
            cc.distinguish_size = size

            cc.save()

            if 'prev' in request.POST:
                return redirect(cc_school_history, child_name)
            elif 'next' in request.POST:
                return redirect(cc_other_info, child_name)
            elif 'step1' in request.POST:
                return redirect(child_case, child_name)
            elif 'step2' in request.POST:
                return redirect(cc_child_history, child_name)
            elif 'step3' in request.POST:
                return redirect(cc_condition, child_name)
            elif 'step4' in request.POST:
                return redirect(cc_stages_of_growth, child_name)
            elif 'step5' in request.POST:
                return redirect(cc_family_history, child_name)
            elif 'step6' in request.POST:
                return redirect(cc_social_development, child_name)
            elif 'step7' in request.POST:
                return redirect(cc_child_beh, child_name)
            elif 'step8' in request.POST:
                return redirect(cc_school_history, child_name)
            elif 'step10' in request.POST:
                return redirect(cc_other_info, child_name)
        else:
            print(child_form.errors)

    else:
        child_form = child_case_form()
        cc = Child_Case_Data.objects.get(child__username=child_name)
    return render(request, 'static_files/cc_diff_info.html', {'obj': appoin, 'form': child_form, 'cc': cc})


def cc_other_info(request, child_name):
    appoin = Appointment.objects.get(child__username=child_name)
    cc = ''
    if request.method == "POST":
        child_form = child_case_form(request.POST)
        if child_form.is_valid():
            # Get data
            follow_up = request.POST['follow_up']
            reason_1 = request.POST['reason_1']
            reason_2 = request.POST['reason_2']
            reason_3 = request.POST['reason_3']
            reason_4 = request.POST['reason_4']
            reason_5 = request.POST['reason_5']
            iq_test = request.POST['iq_test']
            date_last_a = child_form.cleaned_data['date_last_a']
            place_last_a = child_form.cleaned_data['place_last_a']
            other_info = request.POST['other_info']

            cc = Child_Case_Data.objects.get(child__username=child_name)
            cc.parents_cooperation = follow_up
            cc.reason_1 = reason_1
            cc.reason_2 = reason_2
            cc.reason_3 = reason_3
            cc.reason_4 = reason_4
            cc.reason_5 = reason_5
            cc.prev_iq = iq_test
            cc.date_last_assessment = format_date_model(date_last_a)
            cc.place_last_assessment = place_last_a
            cc.other_info = other_info

            cc.save()

            if 'prev' in request.POST:
                return redirect(cc_diff_info, child_name)
            elif 'next' in request.POST:
                return redirect(appointment_list)
            elif 'step1' in request.POST:
                return redirect(child_case, child_name)
            elif 'step2' in request.POST:
                return redirect(cc_child_history, child_name)
            elif 'step3' in request.POST:
                return redirect(cc_condition, child_name)
            elif 'step4' in request.POST:
                return redirect(cc_stages_of_growth, child_name)
            elif 'step5' in request.POST:
                return redirect(cc_family_history, child_name)
            elif 'step6' in request.POST:
                return redirect(cc_social_development, child_name)
            elif 'step7' in request.POST:
                return redirect(cc_child_beh, child_name)
            elif 'step8' in request.POST:
                return redirect(cc_school_history, child_name)
            elif 'step9' in request.POST:
                return redirect(cc_diff_info, child_name)
        else:
            print(child_form.errors)

    else:
        child_form = child_case_form()
        cc = Child_Case_Data.objects.get(child__username=child_name)
        cc.date_last_assessment = format_date_html(cc.date_last_assessment)
    return render(request, 'static_files/cc_other_info.html', {'obj': appoin, 'form': child_form, 'cc': cc})
