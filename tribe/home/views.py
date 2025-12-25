from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
@login_required
def homepage(request):
    if request.method=='POST':
        pass
    else:
        return render(request,'index.html')