from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from betterforms.multiform import MultiModelForm
from .models import User, Caregiver, Job, JobApplication, Member, Appointment, Address
import datetime

class CustomLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('user_type', 'given_name', 'surname', 'city', 'phone_number', 'email', 'profile_description', 'password')

class CaregiverForm(forms.ModelForm):
    class Meta:
        model = Caregiver
        fields = ('image', 'gender', 'caregiving_type', 'hourly_rate')
    def save(self, commit=True, user_id=None):
        # Get the instance without saving it to the database
        instance = super().save(commit=False)
        
        # Set the 'type' field to 'Vehicle'
        instance.caregiver_user_id = user_id
        
        # Save the instance to the database if commit is True
        if commit:
            instance.save()

        return instance
    
class CaregiverSearchForm(forms.Form):
    caregiving_type = forms.ChoiceField(choices=Caregiver.Type.choices, required=False)
    city = forms.CharField(max_length=255, required=False)

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('house_rules',)
    def save(self, commit=True, user_id=None):
        # Get the instance without saving it to the database
        instance = super().save(commit=False)
        
        # Set the 'type' field to 'Vehicle'
        instance.member_user_id = user_id
        
        # Save the instance to the database if commit is True
        if commit:
            instance.save()
            print("saved")

        return instance

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['required_caregiving_type', 'other_requirements']
    def save(self, commit=True, member_user_id=None):
        # Get the instance without saving it to the database
        instance = super().save(commit=False)
        
        # Set the 'type' field to 'Vehicle'
        instance.member_user_id = member_user_id
        instance.date_posted = datetime.date.today()
        
        # Save the instance to the database if commit is True
        if commit:
            instance.save()
            print("saved")

        return instance
    

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'appointment_time', 'work_hours']
    def save(self, commit = True, caregiver_user_id = None, member_user_id = None):
        instance = super().save(commit=False)
        
        # Set the 'type' field to 'Vehicle'
        instance.member_user_id = member_user_id
        instance.caregiver_user_id = caregiver_user_id
        
        # Save the instance to the database if commit is True
        if commit:
            instance.save()
            print("saved")

        return instance
            

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['town', 'street', 'house_number']
    def save(self, commit=True, user_id=None):
        # Get the instance without saving it to the database
        instance = super().save(commit=False)
        
        # Set the 'type' field to 'Vehicle'
        instance.member_user_id = user_id
        
        # Save the instance to the database if commit is True
        if commit:
            instance.save()
            print("saved")

        return instance
