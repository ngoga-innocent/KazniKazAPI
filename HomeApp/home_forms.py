from django import forms
from Product.models import ProductModel,ShopModel

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

class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = ['name', 'description', 'price', 'thumbnail', 'category', 'colors', 'discount', 'place','shop', 'currency','uploader']
        def __init__(self, *args, **kwargs):
            super(ProductForm, self).__init__(*args, **kwargs)
            
            # Check if we are editing an existing instance
            if self.instance and self.instance.id:
                # Make thumbnail optional if editing
                self.fields['thumbnail'].required = False
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 bg-slate-200 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter product name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 bg-slate-200 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter product description',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full p-2 border border-gray-300 bg-slate-200 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter product price',
            }),
            'thumbnail': forms.ClearableFileInput(attrs={
                'class': 'w-full p-2 border border-gray-300 bg-slate-200 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            }),
            'category': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 bg-slate-200 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            }),
            'colors': forms.CheckboxSelectMultiple(attrs={
                'class': 'w-full p-2 border border-gray-300 bg-slate-200 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            }),
            'discount': forms.NumberInput(attrs={
                'class': 'w-full p-2 border border-gray-300 bg-slate-200 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter discount percentage',
            }),
            'place': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 bg-slate-200 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            }),
            'shop':forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 bg-slate-200 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            }),
            'currency': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 bg-slate-200 rounded-md focus:outline-none focus:ring-2 focus:ring-primary',
            }),
            
            
           
        }