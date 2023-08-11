from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView,DetailView,DeleteView,ListView
from django.http import Http404
from braces.views import SelectRelatedMixin
from django.contrib import messages
# Create your views here.

from . import models
from . import forms
from groups.models import Group

from django.contrib.auth import get_user_model
User = get_user_model()

class PostList(SelectRelatedMixin,ListView):
    model = models.Post
    select_related = ('user','group')

class UserPosts(ListView):
    model = models.Post
    template_name = 'post/user_post.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context

class PostDetail(SelectRelatedMixin,DetailView):
    model = models.Post
    select_related = ('user','group')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact = self.kwargs.get('username'))

class CreatePost(LoginRequiredMixin,SelectRelatedMixin,CreateView):
    model = models.Post
    fields = ('message','group')

    def form_valid(self, form ):
        query_se = list(Group.objects.filter(members=self.request.user).values_list('name',flat=True))
        current = form.cleaned_data['group']        #get value from form field
        if str(current) in query_se:
            self.object  = form.save(commit = False)
            self.object.user = self.request.user
            self.object.save()
            return super().form_valid(form)
        else:
            messages.error(self.request, "You are not member of this group.")
            return super().get(request=form)




class DeletePost(DeleteView,SelectRelatedMixin,LoginRequiredMixin):
    model = models.Post
    select_related = ('user','group')
    success_url = reverse_lazy('posts:all')
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        message.success(self.request,'Post Deleted')
        return super().delete(*args,**kwargs)

