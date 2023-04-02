from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from stream.models import Post 
from .models import FriendRequest, Inbox, Profile,Follower
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

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

# @login_required
# def profile(request, id):
#     author = get_object_or_404(Profile, id=id)
#     return render(request, 'users/profile.html', {'author': author})

@login_required
def profile(request, id):
    author = get_object_or_404(Profile, id=id)
    return render(request, 'users/profile.html', {'author': author})

@login_required
def user_profile(request, id):
    author = get_object_or_404(Profile, id=id)
    return render(request, 'users/user_link.html', {'author': author})


@login_required
def profile_edit(request, id):
    if request.method == "POST":
        posts = Post.objects.filter()
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid and p_form.is_valid:
            u_form.save()
            p_form.save()
            messages.success(request, f"Your profile has been updated!")
            return redirect(profile, id)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "u_form": u_form,
        "p_form": p_form,
    }


@login_required
def followers(request):
    profile = request.user.profile
    followers = profile.followers.all()
    return render(request, 'users/followers.html', {'followers': followers})




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

@login_required
def inbox(request):
    context={}
    if request.method == "POST":        
        request_type = request.POST.get('type')
        if request_type == 'follow':           
            profile_id = request.POST.get('profile_id')
            actor= Profile.objects.get(pk=request.user.profile.id)
            object = Profile.objects.get(pk=profile_id)
            summary=  f"{actor} wants to follow {object}"
            friend_request= FriendRequest.objects.create(summary=summary, actor = actor, object= object)
            inbox = Inbox.objects.create(profile=object)
            inbox.friend_requests.add(friend_request)
            context={
                "summary": summary,
                "username": actor,
            }
            return redirect(user_profile,profile_id)
    else:
            return render(request, 'users/inbox.html',context)

@login_required
@csrf_exempt        

def accept(request, id):
    if request.method == 'POST':
        # profile_id = request.POST.get('profile_id')    
        # friend_request = FriendRequest.objects.get_or_create(id=id)
        friend_request = get_object_or_404(FriendRequest, id=id)
        friend_profile = friend_request.actor
        # friend_profile = request.user.profile
        delete_request_id = request.POST.get('delete')
        friend_request_id = request.POST.get('accept')
        # friend_profile = get_object_or_404(Profile, id=profile_id)
        follows_profile = request.user.profile

        #accepts friend request
        if friend_request_id:
            #Add to follower model
            follower = Follower.objects.create()

            follower.items.set([friend_profile])
            # Add the accepted profile to the list of followed profiles
            follows_profile.followers.add(friend_profile) 
            # delete friend request and inbox object
            # Delete friend request and inbox object
            friend_request = FriendRequest.objects.filter(actor=friend_profile, object=follows_profile).first()
            if friend_request:
                friend_request.delete()
            inbox = Inbox.objects.filter(profile=follows_profile).first()
            if inbox:
                inbox.friend_requests.remove(friend_request)
                if inbox.friend_requests.count() == 0:
                    inbox.delete()
            messages.success(request, f"You are now friends with {friend_profile.user.username}!")
        
        #deletes friend request
        elif delete_request_id:
            friend_request = FriendRequest.objects.filter(actor=friend_profile, object=follows_profile).first()
            if friend_request:
                friend_request.delete()
            inbox = Inbox.objects.filter(profile=follows_profile).first()
            if inbox:
                inbox.friend_requests.remove(friend_request)
                if inbox.friend_requests.count() == 0:
                    inbox.delete()
        
        # Get the updated friend requests after accepting or deleting a request
        friend_requests = FriendRequest.objects.filter(object=request.user.profile)
        context = {
            'friend_requests': friend_requests,
        }
        return render(request, 'users/inbox.html', context)
            
    # Redirect to inbox after processing the request
    return redirect('inbox')

