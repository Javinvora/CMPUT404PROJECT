from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from stream.models import Post 
from .models import FriendRequest, Inbox, Profile
'''
messages.debug
messages.info
messages.success
messages.warning
messages.error
'''

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            messages.success(request, f"Your account has been created! It will need to be approved by an administrator before you can use it.")
            return redirect("register")
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {"form": form})

@login_required
def profile(request):
    return render(request, "users/profile.html")

@login_required
def update(request):
    if request.method == "POST":
        posts = Post.objects.filter()
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid and p_form.is_valid:
            u_form.save()
            p_form.save()
            messages.success(request, f"Your profile has been updated!")
            return redirect(profile)

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "u_form": u_form,
        "p_form": p_form,
    }

    return render(request, "users/update.html", context)


def inbox(request):
    # context={}
    # if request.method == "POST":
    #     friend_request_id = request.POST.get("accept") or request.POST.get("decline")
    #     print(friend_request_id)
    #     request_type = request.POST.get('type')
    #     #ASK BIGYAN ABOUT VALIDATING FRIEND REQUEST
    #     #checks request type making sure it's a follow request
    #     if request_type == 'follow':           
    #         profile_id = request.POST.get('profile_id')
    #         actor= Profile.objects.get(pk=profile_id)
    #         object= Profile.objects.get(pk=request.user.profile.id)
    #         summary=  f"{actor} wants to follow {object}"
    #         friend_request= FriendRequest.objects.create(summary=summary, actor = actor, object= object)
    #         inbox = Inbox.objects.create(profile=object)
    #         inbox.friend_requests.add(friend_request)
    #         context={
    #             "summary": summary,
    #             "username": actor,
    #         }
    #         return redirect(profile)
    # else:
    #         return render(request, 'users/inbox.html',context)

    context={}
    if request.method == "POST":
        friend_request_id = request.POST.get("accept") or request.POST.get("decline")
        print(friend_request_id)
        request_type = request.POST.get('type')
        context={}
        #checks request type making sure it's a follow request
        if request_type == 'follow':
            profile_id = request.POST.get('profile_id')
            actor= Profile.objects.get(pk=profile_id)
            object= Profile.objects.get(pk=request.user.profile.id)
            summary=  f"{actor} wants to follow {object}"
            friend_request_exists = FriendRequest.objects.filter(actor=actor, object=object).exists()
            if friend_request_exists:
                messages.warning(request, f"You already have sent a friend request to {object}!")
            else:
                friend_request= FriendRequest.objects.create(summary=summary, actor=actor, object=object)
                inbox = Inbox.objects.create(profile=object)
                inbox.friend_requests.add(friend_request)
                context = {
                    'friend_requests': friend_requests
                }
            return redirect('profile')
        
        else:
            inbox = Inbox.objects.get(profile=request.user.profile)
            friend_requests = inbox.friend_requests.all()
            context = {
                'friend_requests': friend_requests
            }
            return render(request, 'users/inbox.html', context)
    return render(request, 'users/inbox.html', context)

