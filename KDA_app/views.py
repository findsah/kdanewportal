from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Person, Role, Hosted_Centres, Appointment, Availability, Slot
from django.contrib import messages
from .forms import login_form, register_form, register_centre_form, add_appointment_form
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
    two_hours = int(str(x.time()).split(':')[0])
    if slotss:
        slotss = Slot.objects.filter(psychologist_id=id1, day=date, available=True)
        if current_time.date() == date:
            for slot in slotss:
                slot_time = int(str(slot.s_time).split(':')[0])
                if slot_time < two_hours:
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
            Appointment.objects.create(psychologist_id=id1, child_id=id2, appointment_date=date, appointment_s_time=time_s,
                                       appointment_e_time=time_e, status=True)
            slot = Slot.objects.get(psychologist_id=id1, day=date, s_time=time_s, e_time=time_e)
            if slot.available == False:
                messages.warning(request, "Slot not available, Kindly select slot again")
                return redirect(check_slots, id1, id2, date)
            else:
                slot.available = False
                slot.save()
                messages.success(request, message="Appointment Added")
                return redirect(add_appointment)
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