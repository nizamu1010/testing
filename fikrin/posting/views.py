from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from authentication.models import UserProfile


def add_quote(request):
    if request.method == 'POST':
        creater = request.user.username
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_pic = user_profile.profile_picture
        except UserProfile.DoesNotExist:
            profile_pic = None  
        content_text = request.POST.get('content-text')
        post = Post(creater=creater, content_text=content_text, profile_pic=profile_pic)
        post.save()
        return redirect('authentication:home')

    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})


def edit_post_view(request, post_id):

    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        
        new_content_text = request.POST.get('edit_text')
        post.edit_post(new_content_text=new_content_text)
        return redirect('authentication:home')  
    

    return render(request, 'index.html', {'post': post})


def delete_post_view(request):
    if request.method == 'GET':
        post_id = request.GET.get('post_id')  
        if post_id:
            post = get_object_or_404(Post, pk=post_id)
            post.delete()

            return redirect('authentication:home')  


    return render(request, 'index.html', {'post': post})



def like_post(request, post_id):

    post = Post.objects.get(pk=post_id)
    post.add_liker(request.user)
    post.save()
    return redirect('authentication:home')



def unlike_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    
    if request.user in post.likers.all():
        post.remove_liker(request.user)
        post.save()
        
    return redirect('authentication:home')


def comment_view(request, item_id):
    post = get_object_or_404(Post, id=item_id)

    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        parent_comment_id = request.POST.get('parent_comment_id')

        user_profile = UserProfile.objects.get(user=request.user)
        commenter_pic = user_profile.profile_picture

        parent_comment = None

        if parent_comment_id:
            parent_comment = Comment.objects.get(id=parent_comment_id)

        new_comment = Comment.objects.create(
            post=post,
            commenter=request.user,
            comment_content=comment_text,
            parent_comment=parent_comment,
            commenter_pic=commenter_pic
        )

        return redirect('posting:comment_view', item_id)

    comments = Comment.objects.filter(post=post, parent_comment=None).order_by('-comment_time')

    context = {
        'comments': comments,
        'post': post,
    }

    return render(request, 'cmd_box.html', context)



def replay_view(request, item_id, parent_comment_id):
    post = get_object_or_404(Post, id=item_id)
    parent_comment = get_object_or_404(Comment, id=parent_comment_id)

    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')

        user_profile = UserProfile.objects.get(user=request.user)
        commenter_pic = user_profile.profile_picture

        new_comment = Comment.objects.create(
            post=post,
            commenter=request.user,
            comment_content=comment_text,
            parent_comment=parent_comment,
            commenter_pic=commenter_pic
        )

        return redirect('posting:comment_view', item_id)

    comments = parent_comment.replies.all().order_by('-comment_time')

    context = {
        'comments': comments,
        'post': post,
        'parent_comment': parent_comment,
    }

    return render(request, 'replies.html', context)


def delete_comment(request):
    if request.method == 'GET':
        post_id = request.GET.get('post_id')  # Get the post_id parameter from the URL
        if post_id:
            comment = get_object_or_404(Comment, pk=post_id)
            comment.delete()

            return redirect('authentication:home') 


    return redirect('authentication:home') 

