from django.shortcuts import render,redirect

# Create your views here.
def user_login(request):
    if request.method=='POST':
        pass
    else:
        return render(request,'login.html')
    
def user_signup(request):
    if request.method=='POST':
        pass
    else:
        return render(request,'registration/signup.html')