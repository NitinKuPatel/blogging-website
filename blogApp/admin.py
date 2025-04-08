from django.contrib import admin
from blogApp.models import Post, files
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields':('address', 'contact')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields':('address', 'contact')}),
    )
    list_display=['id','username','first_name','last_name','password','address','contact']


class PostAdmin(admin.ModelAdmin):
    list_display=('title','slug','author','created','status','publish')
    list_filter=('status','created','publish')
    prepopulated_fields={'slug':('title',)}
    raw_id_fields=('author',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(files)
admin.site.register(Post,PostAdmin)