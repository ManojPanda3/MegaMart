from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# Register your models here.
from .models import User, Category, Listing, Comment

class ListingInline(admin.TabularInline):
    model = Listing

class CommentAdmin(admin.ModelAdmin):
    inlines = [
        ListingInline,
    ]




admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Comment)