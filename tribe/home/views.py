from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from feed.models import Post,Comment,Like
from django.http import JsonResponse
from django.views.decorators.http import require_POST


# Create your views here.
@never_cache
@login_required
def homepage(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'posts': posts})


