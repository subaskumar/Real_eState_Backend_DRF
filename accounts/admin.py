from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import UserAccount
from .forms import UserAdminCreationForm

# Register your models here.

class UserAccountAdmin(BaseUserAdmin):
    
    add_form = UserAdminCreationForm 
    list_display = ['email', 'is_active', 'is_staff','is_admin']
    list_filter = ('staff','active' ,'admin', )
    search_fields = ['email','name','is_active']
    filter_horizontal = ()
    ordering = ('email','name')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('admin','staff','active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','name', 'password1', 'password2')}
        ),
    )

    
admin.site.register(UserAccount,UserAccountAdmin)
