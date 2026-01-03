from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from feed.models import Post
from users.models import Profile   


# Create your views here.
@login_required
@never_cache
def account_details(request):
    user = request.user

    # Profile (OneToOne with User)
    profile = Profile.objects.get(user=user)

    # Only this user's posts
    posts = Post.objects.filter(author=user).order_by('-created_at')

    context = {
        'user_obj': user,
        'profile': profile,
        'posts': posts
    }

    return render(request, 'account_details.html', context)
