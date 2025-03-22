import random
import string
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib import messages
from main.models.user import User
from django.core.mail import send_mail




def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            if user.role == 'BANK_WORKER':
                return redirect('/create-user')  # Redirect bank workers to /create-user
            elif user.role == 'CUSTOMER':
                return redirect('/customer-home')  # Redirect customers to their home page
        else:
            messages.error(request, "Invalid credentials")
            return redirect('/login')

    return render(request, 'login.html')

@login_required
def customer_home(request):
    if request.user.role != 'CUSTOMER':
        return redirect('/login')  # Redirect if the user is not a customer
    return render(request, 'customer_home.html', {'user': request.user})

def generate_random_password(length=8):
    """Generate a random password with a mix of letters, digits, and symbols."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


@login_required
def create_user(request):
    if request.user.role != 'BANK_WORKER':
        return HttpResponseForbidden("You are not authorized to perform this action.")

    if request.method == 'POST':
        email = request.POST['email']
        role = request.POST['role']
        password = request.POST['password']  # Accept the password from the form

        if User.objects.filter(email=email).exists():
            messages.error(request, "A user with this email already exists.")
            return redirect('/create-user')

        user = User.objects.create_user(username=email, email=email, role=role, password=password)
        messages.success(request, "User created successfully.")
        return redirect('/create-user')

    return render(request, 'create_user.html')