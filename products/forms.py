# marketplace_project/products/forms.py
from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    """
    Form for creating and updating Product instances.
    Includes custom validation for product fields and adds UI enhancements.
    """
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image']

    def __init__(self, *args, **kwargs):
        """
        Initializes the ProductForm.
        - Populates the category choices from the database.
        - Adds placeholder text to input fields for better user experience.
        - Explicitly sets fields as required.
        """
        super().__init__(*args, **kwargs)
        # Populate category choices dynamically from the Category model
        self.fields['category'].queryset = Category.objects.all()

        # Add placeholders to form fields for user guidance
        self.fields['name'].widget.attrs.update({'placeholder': 'Enter product name'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Provide a detailed description'})
        self.fields['price'].widget.attrs.update({'placeholder': 'e.g., 99.99'})

        # Explicitly mark fields as required.
        # While Django models often define 'blank=False' or 'null=False' which implies required,
        # setting it here ensures client-side validation hints and consistent form behavior.
        self.fields['name'].required = True
        self.fields['description'].required = True
        self.fields['price'].required = True
        self.fields['category'].required = True

    def clean_price(self):
        """
        Custom validation for the 'price' field.
        Ensures that the entered price is a positive number.
        """
        price = self.cleaned_data.get('price')
        # Check if price is provided and if it's less than or equal to zero
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be a positive number.")
        return price

    def clean(self):
        """
        General form validation method.
        This method runs after individual field clean methods.
        It's used here to provide custom error messages if fields are empty,
        even though `field.required = True` also handles this.
        This can be useful for more specific messaging or complex cross-field validation.
        """
        cleaned_data = super().clean()
        
        # Retrieve cleaned data for each field
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')
        price = cleaned_data.get('price')
        category = cleaned_data.get('category')

        # Add specific error messages if required fields are empty
        # Note: This is somewhat redundant with 'field.required = True' but allows for custom messages.
        if not name:
            self.add_error('name', "Product name is required.")
        if not description:
            self.add_error('description', "Product description is required.")
        if not price:
            self.add_error('price', "Price is required.")
        if not category:
            self.add_error('category', "Category is required.")

        return cleaned_data

