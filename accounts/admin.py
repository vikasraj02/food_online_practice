from django.contrib import admin
from .models import User,UserProfile
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomerUserAdmin(UserAdmin): 
    list_display = ('username', 'email', 'first_name', 'last_name','role','is_active')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
    
    
admin.site.register(User,CustomerUserAdmin)
admin.site.register(UserProfile)
