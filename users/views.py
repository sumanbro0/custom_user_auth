from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from .models import User
# Create your views here.
def signup_view(request):

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user=User.objects.filter(email=email)
        if(user.exists()):
           print('user already exists')
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        user.set_password(password)
        user.save()
        return render(request, "signup.html")
        
    return render(request, "signup.html")

def activate_email(request, email_token):
    try:
        user = User.objects.get(uid=email_token)
        user.is_email_verified = True
        user.save()
        return redirect("/")
    except Exception as e:
        return HttpResponse("invalid token")
    

def login_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_email_verified:  # Assuming is_email_verified is an attribute on your custom user model
            login(request, user)
            print(" logged in ")
            return redirect('/')
        else:
            return HttpResponse('Invalid credentials or email not verified')

    return render(request, 'login.html')