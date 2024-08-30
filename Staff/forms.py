from Product.models import Category,CategoryFeatures,FeatureOptions,ProductModel,ShopModel
from django import forms
from Account.models import User
from django.contrib.auth.hashers import make_password

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = ['name', 'description', 'price', 'thumbnail', 'category', 'colors', 'discount', 'place','shop', 'currency','uploader','verified']
        def __init__(self, *args, **kwargs):
            super(ProductForm, self).__init__(*args, **kwargs)
            
            # Check if we are editing an existing instance
            if self.instance and self.instance.id:
                # Make thumbnail optional if editing
                self.fields['thumbnail'].required = False
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter product name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter product description',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter product price',
            }),
            'thumbnail': forms.ClearableFileInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            }),
            'category': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            }),
            'colors': forms.CheckboxSelectMultiple(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            }),
            'discount': forms.NumberInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter discount percentage',
            }),
            'place': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            }),
            'shop':forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            }),
            'currency': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            }),
            'verified': forms.CheckboxInput(attrs={
                'class': ' border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            }),
            
           
        }
class UserForm(forms.ModelForm):
    seller = forms.NullBooleanField(
        widget=forms.Select(
            attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            },
            choices= [(False, 'No'),(True, 'Yes')]  # Default choices for NullBooleanField
        )
    )
    is_staff = forms.NullBooleanField(
        widget=forms.Select(
            attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            },
            choices=[ (False, 'No'),(True, 'Yes')]  # Default choices for NullBooleanField
        )
    )
    verified = forms.NullBooleanField(
        widget=forms.Select(
            attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            },
            choices=[ (False, 'No'),(True, 'Yes')]  # Default choices for NullBooleanField
        )
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password','profile','phone_number','seller','id_number','id_card','selfie','is_staff','first_name','last_name','verified','account_status']  
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter username',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter First Name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter Last Name',
            }),
            'email':forms.EmailInput(
                attrs={
                    'class':'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                    'placeholder': 'Enter email address',
                }
            ),
            'password':forms.PasswordInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter password',
            }),
            'profile': forms.ClearableFileInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            }),
            'phone_number': forms.NumberInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter phone number',
            }),
            # 'seller': forms.NullBooleanField(attrs={
            #     'class': 'w-full border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            # }),
            'id_number': forms.NumberInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter ID number',
            }),
            'id_card': forms.ClearableFileInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            }),
            'selfie': forms.ClearableFileInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            }),
            'account_status': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            }),
        }   
    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        # Check if the password has changed
        if self.cleaned_data['password']:
            user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user       
class ShopForm(forms.ModelForm):
    verified=forms.NullBooleanField(
        widget=forms.Select(
            attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            },
            choices=[ (False, 'No'),(True, 'Yes')]
        )
    )
    class Meta:
        model = ShopModel
        fields=['name','shop_category','slug','owner','location','contact','thumbnail','verified']

        widgets={
            'name': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter shop name',
            }),
            'shop_category': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            }),
            'owner': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring',
                'placeholder': 'Enter shop location',
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring',
                'placeholder': 'Enter shop Slug',
            }),
            'contact': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring',
                'placeholder': 'Enter shop contacts',
            }),
            'thumbnail': forms.ClearableFileInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring',
            }),
        }