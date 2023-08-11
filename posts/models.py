from django.db import models
from django.urls import reverse
from groups.models import Group
from django.conf import settings
from django.utils.timezone import now
# Create your models here.

import misaka

from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    message = models.TextField(max_length=200)
    message_html = models.TextField(editable=False,default='')
    group = models.ForeignKey(Group,on_delete=models.CASCADE,related_name='posts',null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    create_date = models.DateTimeField(default=now)

    def __str__(self):
        return self.message

    def save(self,*args,**kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('posts:single',kwargs={'username':self.user.username,'pk':self.pk})

    class Meta:
        ordering = ['-create_date']
        unique_together = ['user','message']
