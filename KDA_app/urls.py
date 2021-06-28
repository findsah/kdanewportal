from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('register-centre/', views.register_centre, name='register-centre'),
    path('receptionist/', views.receptionist_dashboard, name='receptionist'),
    path('appointment_list/', views.appointment_list, name='appointment_list'),
    path('add_appointment/', views.add_appointment, name='add_appointment'),
    path('success/', views.success, name='success'),
    path('search_psychologist/', views.search_psy, name='search_psy'),
    path('availability/<int:id>/', views.availability, name='availability'),
    path('availability/<int:id>/edit/', views.availability_edit, name='availability_edit'),
    path('slots/<int:id1>/<int:id2>/<str:date>/', views.check_slots, name='check_slots'),
    path('create-slots/<int:id>/<int:weekday>/', views.create_slots),
    path('slots/<int:id1>/<int:id2>/<str:date>/<str:time_s>/<str:time_e>/confirm-appointment/', views.confirm_appointment, name='confirm-appointment'),
    path('delete-appointment/<int:id>/', views.delete_appointment, name='delete-appointment'),
    path('reschedule/<int:id>/', views.rescheudle, name='reschedule'),
    path('child-case-form/<str:child_name>/', views.child_case, name='child-case'),
    path('cc-child-history/<str:child_name>/', views.cc_child_history, name='cc_child_history'),
    path('cc-condition/<str:child_name>/', views.cc_condition, name='cc_condition'),
    path('cc-stages-of-growth/<str:child_name>/', views.cc_stages_of_growth, name='cc_stages_of_growth'),
    path('cc-family-history/<str:child_name>/', views.cc_family_history, name='cc_family_history'),
    path('cc-social-development/<str:child_name>/', views.cc_social_development, name='cc_social_development'),
    path('cc-child-behaviour/<str:child_name>/', views.cc_child_beh, name='cc_child-behaviour'),
    path('cc-school-history/<str:child_name>/', views.cc_school_history, name='cc_school_history'),
    path('cc-difficulties/<str:child_name>/', views.cc_diff_info, name='cc_difficulties'),
    path('cc-other-info/<str:child_name>/', views.cc_other_info, name='cc_other_info'),
    path('send_link/<int:id>/', views.send_link_form, name='send_link')
]