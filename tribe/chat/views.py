from django.shortcuts import render,redirect

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatGroup, GroupMessage
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

@login_required
def chat_room(request, group_name):
    group = get_object_or_404(ChatGroup, group_name=group_name)

    # 🔒 SECURITY CHECK (THIS IS THE IMPORTANT PART)
    if request.user not in group.members.all():
        return HttpResponseForbidden("You are not a member of this chat.")

    messages = GroupMessage.objects.filter(group=group).order_by('created')

    return render(request, 'chat_room.html', {
        'group': group,
        'messages': messages
    })


@login_required
def chat_list(request):
    chats = ChatGroup.objects.filter(members=request.user)

    return render(request, 'chat_list.html', {
        'chats': chats
    })

@login_required
def create_chat(request):
    users = User.objects.exclude(id=request.user.id)

    if request.method == "POST":
        group_name = request.POST.get('group_name')
        member_ids = request.POST.getlist('members')

        if not group_name:
            return render(request, 'chat/create_chat.html', {
                'users': users,
                'error': 'Chat name is required'
            })

        # create chat group
        group = ChatGroup.objects.create(
            groupchat_name=group_name
        )

        # add creator
        group.members.add(request.user)

        # add selected users
        for user_id in member_ids:
            group.members.add(user_id)

        return redirect('chat_room', group_name=group.group_name)

    return render(request, 'create_chat.html', {
        'users': users
    })

@login_required
def leave_chat(request, group_name):
    group = get_object_or_404(ChatGroup, group_name=group_name)

    if request.user not in group.members.all():
        return HttpResponseForbidden()

    group.members.remove(request.user)

    return redirect('chat_list')

@login_required
def add_users(request, group_name):
    group = get_object_or_404(ChatGroup, group_name=group_name)

    if request.user not in group.members.all():
        return HttpResponseForbidden()

    existing_members = group.members.all()
    users = User.objects.exclude(id__in=existing_members)

    if request.method == "POST":
        user_ids = request.POST.getlist('members')

        for uid in user_ids:
            group.members.add(uid)

        return redirect('chat_room', group_name=group.group_name)

    return render(request, 'add_users.html', {
        'group': group,
        'users': users
    })
