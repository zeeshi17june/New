from django.contrib import admin
from groups.models import Group,GroupMember
# Register your models here.

#use inline tabluar class to edit sub model class inside main group in admin interface
class GroupMemberInline(admin.TabularInline):
    model = GroupMember


admin.site.register(Group)
