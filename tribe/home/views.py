from django.shortcuts import render

# Create your views here.
def homepage(request):
    if request=='POST':
        pass
    else:
        return render(request,'index.html')