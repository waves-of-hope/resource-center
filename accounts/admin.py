from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'is_staff')
    list_filter = ('date_joined', 'groups', 'is_staff', 'is_superuser','is_active')
    search_fields = ('first_name', 'last_name', 'phone_number')
    ordering = ('first_name',)

    fieldsets = (
		('Credentials', {'fields': ('email', 'password')}),
		('Personal info', {
			'fields': ('first_name', 'last_name', 'phone_number')}),
		('Others', {'fields': ('bio', 'profile_picture',)}),
		('Permissions', {
			'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
		}),
		('Important dates', {'fields': ('last_login', 'date_joined')}),
	)

    add_fieldsets = (
        (None, {
	        'classes': ('wide',),
	        'fields': ('first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2'),
        }),
    )
