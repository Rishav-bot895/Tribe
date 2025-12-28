from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from .models import Post,Comment,Like
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# Create your views here.
@login_required
@never_cache
def create_post(request):
    if request.method=='POST':
        caption = request.POST.get('caption')
        if not caption:
            return render(request, 'create_post.html', {
                'error': 'Caption cannot be empty'
            })

        image = request.FILES.get('image')

        Post.objects.create(
            author=request.user,
            caption=caption,
            image=image
        )
        return redirect('homepage')
    else:
        return render(request,'create_post.html')