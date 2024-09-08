from django import forms
from Account.models import User
from Jobs.models import Job
class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'profile', 'phone_number', 'id_number', 'id_card', 'selfie']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full p-2 border-0 border-b-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter username',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full p-2 border-0 border-b-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter email',
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'w-full p-2 border-0 border-b-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter password',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full p-2 border-0 border-b-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter First Name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full p-2 border-0 border-b-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter Last Name',
            }),
            'profile': forms.ClearableFileInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full p-2 border-0 border-b-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter Phone Number',
            }),
            'id_number': forms.NumberInput(attrs={
                'class': 'w-full p-2 border-0 border-b-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter ID Number',
            }),
            'id_card': forms.FileInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            }),
            'selfie': forms.FileInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            }),
        }
    
    # Specify required fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['email'].required = True
        self.fields['password'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['profile'].required = True
        self.fields['phone_number'].required = True
        
       
class PostJob(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'job_title', 'job_slug', 'job_description', 'job_location',
            'job_thumbnail', 'job_category', 'job_contact', 'company',
            'job_min_salary', 'job_max_salary', 'currency'
        ]
        widgets = {
            'job_title': forms.TextInput(attrs={
                'class': 'w-full p-2 border-0 border-b-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter Job Title',
            }),
            'job_slug': forms.TextInput(attrs={
                'class': 'w-full p-2 border-0 border-b-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter Job Slug',
            }),
            'job_description': forms.Textarea(attrs={
                'class': 'w-full p-2 border-0 border-b-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter Job Description',
                'rows': 4,
            }),
            'job_location': forms.TextInput(attrs={
                'class': 'w-full p-2 border-0 border-b-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter Job Location',
            }),
            'job_category': forms.Select(attrs={
                'class': 'w-full p-2 border-0 border-b-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            }),
            'job_thumbnail': forms.ClearableFileInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            }),
            'job_contact': forms.TextInput(attrs={
                'class': 'w-full p-2 border-0 border-b-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter Contact Information',
            }),
            'company': forms.TextInput(attrs={
                'class': 'w-full p-2 border-0 border-b-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter Company Name',
            }),
            'job_min_salary': forms.NumberInput(attrs={
                'class': 'w-full p-2 border-0 border-b-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter Minimum Salary',
            }),
            'job_max_salary': forms.NumberInput(attrs={
                'class': 'w-full p-2 border-0 border-b-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter Maximum Salary',
            }),
            'currency': forms.Select(attrs={
                'class': 'w-full p-2 border-0 border-b-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            }),
        }
