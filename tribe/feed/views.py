from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from .models import Post,Comment,Like
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from feed.models import Post,Comment,Like
from django.http import JsonResponse
from django.views.decorators.http import require_POST

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
    
@login_required
@require_POST
def add_comment(request):
    post_id = request.POST.get('post_id')
    content = request.POST.get('content', '').strip()

    if not content:
        return JsonResponse({'error': 'Comment cannot be empty'}, status=400)

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

    comment = Comment.objects.create(
        author=request.user,
        post=post,
        content=content
    )

    return JsonResponse({
        'author': comment.author.username,
        'content': comment.content,
        'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M')
    })

@login_required
@require_POST
def toggle_like(request):
    post_id = request.POST.get('post_id')

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        # Like already existed → unlike
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        'liked': liked,
        'like_count': post.likes.count()
    })
