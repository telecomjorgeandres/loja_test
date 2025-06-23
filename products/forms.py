from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
        # This form will need improvement later (e.g., custom widgets, more validation)
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image']

def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Populate category choices
            self.fields['category'].queryset = Category.objects.all()
