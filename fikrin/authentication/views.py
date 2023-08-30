
from django.contrib import messages ,auth
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from posting.models import Post, Comment
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile




def home(request):
    posts = Post.objects.all().order_by('-date_created')
    comments = Comment.objects.count()
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.filter(user=request.user).get()
            return render(request, 'index.html', {'posts': posts, 'user_profile': user_profile})
        except ObjectDoesNotExist:
            pass
    
    return render(request, 'index.html', {'posts': posts,'comments':comments})



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username,password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect('authentication:home')
        else:
            error_message = 'Incorrect username or password.'
            return render(request, 'login.html',{'error_message':error_message})
        
    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        mobile_number = request.POST.get('mobile_number')

        # Define a regular expression validator for the mobile number
        mobile_number_validator = RegexValidator(
            regex=r'^\d{10}$',
            message='Invalid mobile number. Please enter a 10-digit number.'
        )

        if fullname and username and password and mobile_number:
            if User.objects.filter(username=username).exists():
                error_message = "This username is not available."
                return render(request, 'register.html', {'error_message': error_message})
            else:
                # Validate the mobile number
                try:
                    mobile_number_validator(mobile_number)
                except ValidationError as e:
                    messages.info(request, e.message)
                    return render(request, 'register.html', {'message': e.message})

                user = User.objects.create_user(username=username, password=password)
                user.save()

                user_profile, _ = UserProfile.objects.get_or_create(user=user)
                user_profile.mobile_number = mobile_number
                user_profile.fullname = fullname
                user_profile.save()

                user = auth.authenticate(username=username,password=password)
                
                if user is not None:
                    auth.login(request,user)
                    return redirect('authentication:home')

        else:
            messages.info(request, 'Please fill in all required fields.')
            return render(request, 'register.html', {'error_message': 'Please fill in all required fields.'})

    return render(request, 'register.html')



def signout(request):
    auth.logout(request)
    return redirect('authentication:home')



def compress_image(image, max_size=(800, 800)):
    img = Image.open(image)
    img.thumbnail(max_size)
    
    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG', quality=70)
    
    return InMemoryUploadedFile(
        output_buffer,
        'ImageField',  # Field name in your model
        f'{image.name.split(".")[0]}_compressed.jpg',  # Adjust the filename as needed
        'image/jpeg',  # MIME type
        img.tell, None
    )

def compress_cover_image(image, max_size=(1200, 800)):
    img = Image.open(image)
    img.thumbnail(max_size)
    
    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG', quality=70)
    
    return InMemoryUploadedFile(
        output_buffer,
        'ImageField',  # Field name in your model
        f'{image.name.split(".")[0]}_cover_compressed.jpg',  # Adjust the filename as needed
        'image/jpeg',  # MIME type
        img.tell, None
    )

@login_required
def profile(request):
    if request.method == 'POST':
        cover_image1 = request.FILES.get('cover_image1')
        profile_picture = request.FILES.get('profile_picture')
        username = request.POST.get('username')
        bio = request.POST.get('bio')
        mobile_number = request.POST.get('mobile_number')

        user = request.user
        user_profile, _ = UserProfile.objects.get_or_create(user=user)
        
        if cover_image1:
            compressed_cover_image = compress_cover_image(cover_image1)
            user_profile.cover_image1 = compressed_cover_image
        
        if profile_picture:
            compressed_profile_picture = compress_image(profile_picture)
            user_profile.profile_picture = compressed_profile_picture
            user_profile.save()
            
            posts = Post.objects.filter(creater=request.user)
            for post in posts:
                post.profile_pic = compressed_profile_picture
                post.save()
        if username:
            old_username = user.username  # Store the old username
            user_profile.username = username
            user.username = username
            user.save()
            
            # Step 1: Update the creater field in the associated Post instances
            posts = Post.objects.filter(creater=old_username)
            for post in posts:
                post.creater = username
                post.save()

            # Step 2: Update the creater field in the UserProfile and User models
            user_profile.creater = username
            user_profile.save()


        if bio:
            user_profile.bio = bio

        if mobile_number:
            user_profile.mobile_number = mobile_number

        user_profile.save()

        
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        posts = Post.objects.filter(creater=request.user).order_by('-date_created')
        
    except UserProfile.DoesNotExist:
        return render(request, 'profile.html')

    context = {
        'user_profile': user_profile,
        'posts': posts
    }

    return render(request, 'profile.html', context)




def change_password(request):

    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        old_pass = request.POST.get('old-password')
        new_pass = request.POST.get('new-password')
        confirm_pass = request.POST.get('confirm-password')
        
        user = request.user

        if not authenticate(username=user.username, password=old_pass):
            error_message = 'Invalid old password.'
            return render(request, 'profile.html', {'user_profile':user_profile, 'error_message': error_message})

        if old_pass == new_pass:
            error_message = 'New password cannot be the same as the old password.'
            return render(request, 'profile.html', {'user_profile':user_profile, 'error_message': error_message})
        if new_pass != confirm_pass:
            error_message = 'New password and confirm password do not match.'
            return render(request, 'profile.html', {'user_profile':user_profile, 'error_message': error_message})

        user.set_password(new_pass)
        user.save()

        return render(request, 'profile.html', {'user_profile':user_profile})

    return render(request, 'profile.html', {'user_profile':user_profile})



def creater_details(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(creater=user).order_by('-date_created')
    user_profile = UserProfile.objects.get(user=user)
   
    context = {
        'user_profile': user,
        'posts': posts,
        'user_profile': user_profile
    }

    return render(request, 'details.html', context)



def aboutme(request):
    return render(request,'aboutme.html')




