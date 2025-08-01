from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib import messages
from .models import profile
from datetime import datetime
import requests
from django.core.files.base import ContentFile
import os

# Create your views here.
def join(request):
    if request.method == "POST":
        action = request.POST.get("action")                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
        if action == "register":
            username = request.POST.get("username")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            password = request.POST.get("password")
            if User.objects.filter(username=username).exists():
                messages.error(request, "That username is already taken. Please choose another.")
                return redirect('/accounts/join?form=register')
            User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            user = auth.authenticate(request,username=username,password=password)
            auth.login(request,user)
            
            return redirect('home')
        
        if action == "login":
            username = request.POST.get("username")
            password = request.POST.get("password")
            
            user = auth.authenticate(request,username=username,password=password)
            
            if user is not None:
                auth.login(request,user)
                return redirect("home")
            
            messages.error(request, "Invalid username or password!")
            return redirect('join')
                
    return render(request,'accounts/join.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect("main")

@login_required
def profile_page(request):
    user = request.user
    prof, created = profile.objects.get_or_create(
        user=user,
        defaults={'avatar': 'profile_images/default_avatar.png'}
    )

    avatar_choices = [
        "https://cdn-icons-png.flaticon.com/512/9308/9308904.png",
        "https://cdn-icons-png.flaticon.com/512/3906/3906579.png",
        "https://i.ibb.co/9mT39Z5r/43a2aa9a-5862-4fb7-8bdb-98d2b16e2d6a.png",
        "https://i.ibb.co/XrphShCb/d424b267-709f-40c4-942d-26deef561f2b.png",
        "https://i.ibb.co/vvvmdPGr/58cb1782-f3e7-46b4-b894-9e8a9111968a.png",
        "https://i.ibb.co/cS8cjRb9/6e6f4341-efa0-4380-ae30-908fefd8f59c.png",
        "https://i.ibb.co/pjtBf71c/d5ec05f4-1abd-48fd-a353-00ad1f9a0ffe.png",
        "https://i.ibb.co/MyT6p7rH/image.png",
        "https://i.ibb.co/zWMSSGj4/7569bbd6-f234-4b45-b6fb-4896aac6593d.png",
        "https://i.ibb.co/678MzLLS/42b96bce-f50c-4a72-996b-be530ab82ac9.png"
    ]
    
    if request.method == 'POST':
        # --- Save text fields first ---
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()

        prof.phone = request.POST.get('phone') 
        prof.gender = request.POST.get('gender')
        # ... (Your existing dob logic) ...
        prof.save()

        # --- New Logic for Avatars ---
        # Case 1: A pre-selected avatar was chosen from the grid
        if 'avatar' in request.POST and request.POST.get('avatar'):
            avatar_url = request.POST.get('avatar')
            try:
                response = requests.get(avatar_url, stream=True)
                if response.status_code == 200:
                    filename = os.path.basename(avatar_url)
                    # Save the downloaded content to the ImageField
                    prof.avatar.save(filename, ContentFile(response.content), save=True)
                else:
                    messages.error(request, "Could not download the selected avatar.")
            except requests.exceptions.RequestException:
                messages.error(request, "Could not reach the avatar server.")
        
        # Case 2: A new file was uploaded
        elif 'avatar_upload' in request.FILES:
            prof.avatar = request.FILES['avatar_upload']
            prof.save()
            
        return redirect("profile_page") 
    
    return render(request, 'accounts/profile.html', {
        'user': user,
        'prof': prof,
        'avatar_choices': avatar_choices
    })