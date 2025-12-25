from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User

# Create your views here.
def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            messages.error(request, "Invalid username or password")
    else:
        return render(request,'login.html')
    
def user_signup(request):
    if request.method=='POST':
        user = User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password']
        )
        user.profile.bio = request.POST.get('bio', '')
        user.profile.display_name = request.POST.get('display_name')
        user.profile.pfp = request.FILES.get('profile_photo')
        user.profile.save()

        return redirect('login')

    else:
        return render(request,'registration/signup.html')