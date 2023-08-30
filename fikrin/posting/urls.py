from django.urls import path
from . import views


app_name = 'posting'

urlpatterns = [
    path('add-quote/', views.add_quote, name='add_quote'),
    path('edit_post/<int:post_id>/', views.edit_post_view, name='edit_post'),
    path('delete_post/', views.delete_post_view, name='delete_post'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('unlike_post/<int:post_id>/', views.unlike_post, name='unlike_post'),
    path('comment_view/<int:item_id>/', views.comment_view, name='comment_view'),
    path('delete_comment/', views.delete_comment, name='delete_comment'),
    path('replay_view/<int:item_id>/<int:parent_comment_id>/', views.replay_view, name='replay_view'),

]


