from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def home(request):
        return render(request, 'core/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}! You can now log in.')
                return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
         # This block runs for GET requests (when the page is first loaded).
        # We create a fresh, empty form to display.
           
    else:
            form = UserCreationForm()
    # This single render statement handles both:
    # 1. Initial GET requests (displaying the empty form).
    # 2. Invalid POST requests (re-displaying the form with user's input and errors).
            return render(request, 'core/register.html', {'form': form})
    