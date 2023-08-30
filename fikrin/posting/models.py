from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    creater = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to='profile_pic/', null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content_text = models.TextField()
    likers = models.ManyToManyField('auth.User', related_name='liked_posts')
    comment_count = models.PositiveIntegerField(default=0)

    def add_liker(self, liker):
        self.likers.add(liker)

    def remove_liker(self, liker):
        self.likers.remove(liker)

    def add_comment(self):
        self.comment_count += 1

    def add_saver(self, saver):
        self.savers.add(saver)

    def remove_saver(self, saver):
        self.savers.remove(saver)

    def edit_post(self, new_content_text):
        self.content_text = new_content_text
        self.save()

    def delete_post(self):
        self.delete()



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenters')
    commenter_pic = models.ImageField(upload_to='commenter_pic/', null=True)
    comment_content = models.TextField(max_length=90)
    comment_time = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"Post: {self.post} | Commenter: {self.commenter}"

    def serialize(self):
        return {
            "id": self.id,
            "commenter": self.commenter.serialize(),
            "body": self.comment_content,
            "replies": [reply.serialize() for reply in self.replies.all()]
        }

    def delete_post(self):
        self.delete()