from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User

@admin.register(User)
class UserAdmin(UserAdmin):

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'is_staff')
    list_filter = ('date_joined', 'groups', 'is_staff', 'is_superuser','is_active')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')

    fieldsets = (
		(_('Credentials'), {'fields': ('username', 'password')}),
		(_('Personal info'), {
			'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
		(_('Others'), {'fields': ('bio', 'profile_picture',)}),
		(_('Permissions'), {
			'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
		}),
		(_('Important dates'), {'fields': ('last_login', 'date_joined')}),
	)

    add_fieldsets = (
        (None, {
	        'classes': ('wide',),
	        'fields': ('username', 'email', 'phone_number', 'password1', 'password2'),
        }),
    )

