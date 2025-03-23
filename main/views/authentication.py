import random
import string
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib import messages
from main.decorators import role_required
from main.models.user import User
from django.core.mail import send_mail

from main.utils import log_action




def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            # Log successful login
            log_action(
                user=user,
                action=f"Successful login for user with email: {email}."
            )

            # Redirect based on user role
            if user.role == 'BANK_WORKER':
                return redirect('/create-user')  # Redirect bank workers to /create-user
            elif user.role == 'CUSTOMER':
                return redirect('/customer-home')  # Redirect customers to their home page
        else:
            # Log failed login attempt
            log_action(
                user=None,
                action=f"Failed login attempt for email: {email}."
            )

            messages.error(request, "Invalid credentials")
            return redirect('/login')

    return render(request, 'login.html')

@login_required
@role_required(allowed_roles=['CUSTOMER'])
def customer_home(request):
    if request.user.role != 'CUSTOMER':
        return redirect('/login')  # Redirect if the user is not a customer
    return render(request, 'customer_home.html', {'user': request.user})

def generate_random_password(length=8):
    """Generate a random password with a mix of letters, digits, and symbols."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


@login_required
@role_required(allowed_roles=['BANK_WORKER'])
def create_user(request):
    # Ensure only BANK_WORKER users can access this view
    if request.user.role != 'BANK_WORKER':
        log_action(
            user=request.user,
            action="Unauthorized access attempt to create_user view."
        )
        return HttpResponseForbidden("You are not authorized to perform this action.")

    if request.method == 'POST':
        email = request.POST.get('email')
        role = request.POST.get('role')
        password = request.POST.get('password')

        # Validate inputs
        if not email or not role or not password:
            messages.error(request, "All fields are required.")
            return redirect('/create-user')

        # Check if a user with the provided email already exists
        if User.objects.filter(email=email).exists():
            log_action(
                user=request.user,
                action=f"Failed attempt to create a user with an existing email: {email}."
            )
            messages.error(request, "A user with this email already exists.")
            return redirect('/create-user')

        # Create a new user
        user = User.objects.create_user(
            username=email,
            email=email,
            role=role,
            password=password
        )

        # Log the user creation action
        log_action(
            user=request.user,
            action=f"Created a new user with email: {email} and role: {role}."
        )

        messages.success(request, "User created successfully.")
        return redirect('/create-user')

    return render(request, 'create_user.html')


def forbidden_view(request):
    return render(request, '403.html', status=403)