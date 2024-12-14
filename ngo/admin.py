from django.contrib import admin

# Register your models here.
from .models import Donation
from .models import PendingGroupRequest
from django.contrib.auth.models import User,Group
from unfold.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from unfold.decorators import action  # Import @action decorator from Unfold
from django.db.models import QuerySet
from django.http import HttpRequest


from unfold.admin import ModelAdmin


admin.site.unregister(User)
admin.site.unregister(Group)



admin.site.site_title = "Foundation"
admin.site.site_header = "Foundation Dashbaord"
admin.site.index_title = "Dashbaord"



@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass




@admin.register(PendingGroupRequest)
class PendingGroupRequestAdmin(ModelAdmin):
    list_display = ('name', 'phone_number', 'is_approved', 'created_at','email')
    list_filter = ('is_approved', 'created_at')
    actions = ['approve_requests', 'reject_requests']

    @action(description="Approve selected requests")
    def approve_requests(self,request: HttpRequest, queryset: QuerySet):
        for pending_request in queryset.filter(is_approved=False):
            user = pending_request.name
            password = pending_request.password
            group = Group.objects.get(name="Volunters")
            new_user = User.objects.create_user(username=user)
            new_user.set_password(password)
            new_user.email = pending_request.email
            new_user.save()
            print("here")

            new_user.groups.add(group)    # Mark as approved
            pending_request.save()

    @action(description="Reject selected requests")
    def reject_requests(self, request, queryset):
        queryset.filter(is_approved=False).delete()



admin.site.register(Donation)
