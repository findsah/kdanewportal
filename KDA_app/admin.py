from django.contrib import admin
from .models import Person, Role, Hosted_Centres, Appointment, Availability, Slot, Child_Case_Data, Intervention


# Register your models here.


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'full_name', 'role']

    # prepopulated_fields = {'slug': ('full_name',)}

    class Meta:
        model = Person


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'created_date']

    class Meta:
        model = Role


@admin.register(Hosted_Centres)
class Hosted_CentresAdmin(admin.ModelAdmin):
    list_display = ['id', 'centre_name', 'spoc_f_name', 'spoc_email']

    class Meta:
        model = Hosted_Centres


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'child', 'appointment_s_time', 'appointment_e_time', 'psychologist']

    class Meta:
        model = Appointment


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ['id', 'psychologist']

    class Meta:
        model = Availability


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ['id', 'psychologist', 's_time', 'e_time', 'available', 'day']

    class Meta:
        model = Slot


@admin.register(Child_Case_Data)
class Child_Case_DataAdmin(admin.ModelAdmin):
    list_display = ['id', 'child']

    class Meta:
        model = Child_Case_Data


@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    list_display = ['id', 'teacher', 'student', 'day', 'time']

    class Meta:
        model = Intervention
