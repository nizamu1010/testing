
from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'user', 'mobile_number','mobile_visible']






# Username (leave blank to use 'nizamu'): fkrn
# Email address: fkrn@gmail.com
# Password: fkrn
# Password (again): fkrn