from functools import wraps
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from django.contrib.auth import login
from django.urls import reverse
from django.shortcuts import render, redirect
from .models import User, Caregiver, Member, Job, Appointment, Address
from .forms import CustomLoginForm, MemberForm, CaregiverForm, CustomUserCreationForm, JobForm, JobApplication, AddressForm, CaregiverSearchForm, AppointmentForm
from django.contrib.auth.decorators import login_required
import datetime

def custom_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('custom_login')  # Replace 'custom_login' with the actual URL name for your login view
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def custom_authenticate(email, password):
    try:
        user = User.objects.get(email=email, password=password)
        return user
    except User.DoesNotExist:
        return None

def custom_login(request):
    form = CustomLoginForm()
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Authenticate user
            user = custom_authenticate(email, password)
            if user is not None:
                login(request, user)
                # Check if the user is a caregiver or member
                request.session['user_info'] = {
                    'user_id': user.user_id,
                    'given_name': user.given_name,
                    'surname': user.surname,
                    'phone': user.phone_number,
                    'user_type': user.user_type
                    # Add other relevant user information here
                }
                print("here")
                return redirect('profile_view')
    return render(request, 'login.html', {'form': form})

def profile_view(request):
    user = request.session.get('user_info')
    if user:

        user_id = user['user_id']
        given_name = user['given_name']
        surname = user['surname']
        phone = user['phone']
        try:
            caregiver = Caregiver.objects.get(caregiver_user_id=user_id)
            return render(request, 'caregiver_profile.html', {'caregiver': caregiver, 'given_name': given_name, 'surname': surname, 'phone': phone})
        except Caregiver.DoesNotExist:
            pass

        try:
            member = Member.objects.get(member_user_id=user_id)
            return render(request, 'member_profile.html', {'member': member, 'given_name': given_name, 'surname': surname, 'phone': phone})
        except Member.DoesNotExist:
            pass
    else:
        return redirect('custom_login')
    
def registration(request):
    user_form = CustomUserCreationForm()

    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            request.session['user_inf'] = {'user_id': user.user_id, 'user_type': user.user_type}
            return redirect('complete_registration')

    return render(request, 'registration.html', {'user_form': user_form})

def complete_registration(request):
    user = request.session.get('user_inf')
    if user:

        user_id = user['user_id']
        user_type = user['user_type']

    if user_type == 'member':
        member_form = MemberForm()
        if request.method == 'POST':
            member_form = MemberForm(request.POST)
            if member_form.is_valid():
                member_form.save(user_id=user_id)
                return redirect('address_register')
            else:
                print("Member form errors:", member_form.errors)
        return render(request, 'complete_registration.html', {'user_type': user_type, 'member_form': member_form})
    elif user_type == 'caregiver':
        caregiver_form = CaregiverForm()
        if request.method == 'POST':
            caregiver_form = CaregiverForm(request.POST, request.FILES)
            if caregiver_form.is_valid():
                caregiver_form.save(user_id=user_id)
                return redirect('custom_login')
        return render(request, 'complete_registration.html', {'user_type': user_type, 'caregiver_form': caregiver_form})
    else:
        # Add a return statement for this case
        return redirect('custom_login')

def address_register(request):
    user = request.session.get('user_inf')
    if user:
        user_id = user['user_id']
    address_form = AddressForm()
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            address_form.save(user_id=user_id)
            return redirect('custom_login')
    return render(request, 'address_register.html', {'address_form': address_form})


def create_job(request, member_user_id):
    form = JobForm()

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save(member_user_id=member_user_id)
            return redirect('profile_view')

    return render(request, 'create_job.html', {'form': form})

def view_jobs(request):
    jobs = Job.objects.all()  # Define jobs outside the if-else blocks
    jobs_search_form = JobForm()
    if request.method == 'GET':
        jobs_search_form = JobForm(request.GET)
        if jobs_search_form.is_valid():
            caregiving_type = jobs_search_form.cleaned_data.get('required_caregiving_type')
            other_requirements_query = jobs_search_form.cleaned_data.get('other_requirements', '')
            jobs = Job.objects.filter(
                required_caregiving_type__icontains=caregiving_type,
                other_requirements__icontains=other_requirements_query
            )

    return render(request, 'job_list.html', {'jobs': jobs, 'jobs_search_form': jobs_search_form})

def search_caregivers(request):
    form = CaregiverSearchForm(request.GET)
    results = []

    if form.is_valid():
        caregiving_type = form.cleaned_data.get('caregiving_type')
        city = form.cleaned_data.get('city')

        # Filter caregivers based on search criteria
        caregivers_query = Caregiver.objects.all()

        if caregiving_type:
            caregivers_query = caregivers_query.filter(caregiving_type=caregiving_type)

        if city:
            caregivers_query = caregivers_query.filter(caregiver_user__city__icontains=city)

        results = caregivers_query.select_related('caregiver_user')

    return render(request, 'caregiver_list.html', {'form': form, 'results': results})

def apply_job(request, job_id):
    user = request.session.get('user_info')
    if user:
        user_id = user['user_id']

    if JobApplication.objects.filter(caregiver_user_id=user_id, job=job_id).exists():
        return redirect('view_jobs')

    job_application = JobApplication(caregiver_user_id=user_id, job_id=job_id, date_applied=timezone.now().date())
    job_application.save()

    return redirect('profile_view')

def make_appointment(request, caregiver_user_id):
    user = request.session.get('user_info')
    if user:
        user_id = user['user_id']
    form = AppointmentForm()
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save(caregiver_user_id=caregiver_user_id, member_user_id=user_id)
            return redirect('profile_view')

    return render(request, 'make_appointment.html', {'form': form})

def appointments(request):
    user = request.session.get('user_info')
    if user:
        user_id = user['user_id']
        results = Appointment.objects.filter(member_user_id=user_id)
        return render(request, 'appointments.html', {'results': results})
    else:
        # Handle the case where user_info is not present in the session
        return HttpResponse("User information not found.")
    
def caregiver_appointments(request):
    user = request.session.get('user_info')
    if user:
        user_id = user['user_id']
        results = Appointment.objects.filter(caregiver_user_id=user_id)
        return render(request, 'caregiver_appointments.html', {'results': results})
    else:
        # Handle the case where user_info is not present in the session
        return HttpResponse("User information not found.")
    
def accept(request, appointment_id):
    result = Appointment.objects.get(appointment_id=appointment_id)
    result.change(status = "Scheduled")
    return redirect(caregiver_appointments)

def reject(request, appointment_id):
    result = Appointment.objects.get(appointment_id=appointment_id)
    result.change(status = "Cancelled")
    return redirect(caregiver_appointments)

def view_appointment(request, appointment_id):
    result = Appointment.objects.get(appointment_id=appointment_id)
    address = Address.objects.get(member_user_id = result.member_user_id)
    user = User.objects.get(user_id = result.member_user_id)
    member = Member.objects.get(member_user_id = result.member_user_id)
    return render(request, "view_appointment.html", {'address': address, 'user': user, 'member': member})

def applications(request):
    user = request.session.get('user_info')
    if user:
        user_id = user['user_id']
        jobs = Job.objects.filter(member_user_id = user_id)
        return render(request, "my_jobs.html", {'jobs': jobs})
    else:
        # Handle the case where user_info is not present in the session
        return HttpResponse("User information not found.")
    
def applicants(request, job_id):
    applicants = JobApplication.objects.filter(job_id = job_id)
    all_caregivers = []
    for applcant in applicants:
        caregiver = Caregiver.objects.get(caregiver_user_id = applcant.caregiver_user_id)
        all_caregivers.append(caregiver)
    return render(request, "all_applicants.html", {'caregivers': all_caregivers})

def view_applicant(request, caregiver_user_id):
    caregiver = Caregiver.objects.get(caregiver_user_id = caregiver_user_id)
    user = User.objects.get(user_id = caregiver_user_id)
    return render(request, "applicants.html", {'caregiver': caregiver, 'user': user})
    

    






