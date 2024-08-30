from django import forms
from Account.models import User

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
        
       
