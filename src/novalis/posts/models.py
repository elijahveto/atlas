from users.models import Company, User
from django.urls import reverse
from django.db import models
from tinymce.models import HTMLField
from datetime import datetime
# Create your models here.

class Section(models.Model):
    company = models.ForeignKey(Company, on_delete= models.CASCADE)
    name = models.CharField(max_length = 80, blank=False, null=False)

    def get_absolute_url(self):
        return reverse('posts:section-detail', kwargs ={'id':self.id})

class Post(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, blank=False, null=False)
    text = HTMLField(blank=False, null=False, default="some text")
    #text = models.TextField(blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null= True)
    date = models.DateField(default = datetime.now)

    def get_absolute_url(self):
        return reverse('posts:post-detail', kwargs ={'id':self.id})

    def count_likes(self):
        try:
            return len(Likes.objects.filter(post_id = self.id, comment_id=None))
        except Likes.DoesNotExist:
            return None

    def who_liked(self):
        try:
            users = [User.objects.get(user_id = like.user_id).get_full_name() for like in Likes.objects.filter(post_id=self.id, comment_id=None)]
            return users
        except Likes.DoesNotExist:
            return None


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null= True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(blank=False, null=False)
    date = models.DateField(default=datetime.now)

    def count_likes(self):
        return len(Likes.objects.filter(comment_id = self.id))

    def who_liked(self):
        try:
            users = [User.objects.get(user_id = like.user_id).get_full_name() for like in Likes.objects.filter(comment_id=self.id)]
            return users
        except Likes.DoesNotExist:
            return None

class Likes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null= True, default=None)
    user =models.ForeignKey(User, on_delete=models.SET_NULL, null=True)



