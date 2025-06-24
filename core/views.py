from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def home(request):
        return render(request, 'core/home.html')

def register(request):
    # This block handles form submissions (POST requests)
    if request.method == 'POST':
        form = UserCreationForm(request.POST) # Create form with submitted data
        if form.is_valid():
            # If data is valid, save user and redirect
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login') # IMPORTANT: Always redirect after successful POST
        else:
            # If data is NOT valid, add a general error message.
            # The 'form' object (which holds user's input and specific errors)
            # will then be passed to the render statement below.
            messages.error(request, 'Please correct the errors below.')
            # NO return HERE. We want to fall through to the final render.
    # This block handles initial page loads (GET requests)
    else:
        # For a GET request, create an empty form to display to the user.
        form = UserCreationForm()
    
    # This is the SINGLE return render statement for the entire view.
    # It will render the 'register.html' template with the 'form' object:
    # - If it was a GET request: 'form' will be an empty UserCreationForm.
    # - If it was an invalid POST request: 'form' will contain the user's
    #   submitted data AND all validation errors, which Django's template
    #   engine will automatically display.
    return render(request, 'core/register.html', {'form': form})
    