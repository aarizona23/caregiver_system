from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... other URL patterns ...
    path('', views.custom_login, name='custom_login'),
    path('register/', views.registration, name='registration'),
    path('address_register/', views.address_register, name='address_register'),
    path('complete_registration/', views.complete_registration, name='complete_registration'),
    path('profile_view/', views.profile_view, name='profile_view'),
    path('profile_view/create_job/<int:member_user_id>', views.create_job, name='create_job'),
    path('profile_view/view_jobs/', views.view_jobs, name='view_jobs'),
    path('profile_view/accept/<int:appointment_id>', views.accept, name='accept'),
    path('profile_view/reject/<int:appointment_id>', views.reject, name='reject'),
    path('profile_view/view_appointment/<int:appointment_id>', views.view_appointment, name='view_appointment'),
    path('profile_view/search_caregivers/', views.search_caregivers, name='search_caregiver'),
    path('profile_view/appointments/', views.appointments, name='appointments'),
    path('profile_view/my_appointments/', views.caregiver_appointments, name='caregiver_appointments'),
    path('profile_view/make_appointment/<int:caregiver_user_id>', views.make_appointment, name='make_appointment'),
    path('profile_view/apply_job/<int:job_id>', views.apply_job, name='apply_job'),
    path('profile_view/applications', views.applications, name='applications'),
    path('profile_view/applicants/<int:job_id>', views.applicants, name='applicants'),
    path('profile_view/applicant_profile/<int:caregiver_user_id>', views.view_applicant, name='view_applicant'),
    path('logout/', LogoutView.as_view(next_page='custom_login'), name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)