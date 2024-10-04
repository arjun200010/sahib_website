from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def products(request):
    return render(request, 'products.html')


def signup(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        username = request.POST['username']
        lastname = request.POST['lastname']
        email = request.POST['email']
        location = request.POST['location']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            # Check if the email is unique
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(location=location, username = username, first_name=firstname, last_name=lastname, email=email, password=password,role="CUSTOMER")

                user.is_active = False  # Deactivate the user until verification
                verification_code = get_random_string(32)  # Generate a random code
                user.verification_code = verification_code
                user.save()

                # Send an email with the verification link
                subject = 'Email Verification'
                verification_url = request.build_absolute_uri(reverse('verify_email', args=[verification_code]))
                message = f'Click the following link to verify your email: {verification_url}'
                from_email = 'sahibecommerce@gmail.com'
                recipient_list = [email]
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                messages.success(request,"An account activation link is send to your email ,verify it to continue")
                return redirect('signup')  # Redirect to a login page with a message

            else:
                # Email already exists
                messages.error(request,"Email already exists")
                return render(request, 'signup.html')
        else:
            # Passwords do not match
            messages.error(request,"Password does not match")
            return render(request, 'signup.html')

    return render(request, 'signup.html')

def verify_email(request, verification_code):
    User = get_user_model()
    
    try:
        user = User.objects.get(verification_code=verification_code, is_active=False)
        user.is_active = True  # Activate the user
        user.is_verified = True  # Set the user as verified
        user.save()
        return redirect('login')
        
    except User.DoesNotExist:
        messages.error(request,"Invalid email.Please enter valid email")
        return render(request, 'signup.html') 

def check_user_email(request):
    userd = request.GET.get('email')
    data = {
        "exists": User.objects.filter(email=userd).exists()
    }
    return JsonResponse(data)

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Assuming the user's role can be obtained from the user object
            if user.role == "ADMIN":
                auth_login(request, user)  # Log in the user
                # request.session['username'] = username
                return redirect("adminpage")
            else:
                auth_login(request, user)  # Log in the user
                # request.session['username'] = username
                return redirect("customerpage")
        else:
            messages.error(request, 'Invalid login credentials or account is deactivated')
            return redirect('login')
    return render(request,'login.html')
    # response = render(request, 'login.html')
    # response['Cache-Control'] = 'no-store, must-revalidate'
    # return response

def handlelogout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')

def adminpage(request):
    return render(request,'adminpage.html')

def customerpage(request):
    return render(request,'customerpage.html')