from django.contrib import admin
from .models import User, Interaction, Post, Comment

# Register your models here.

admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Interaction)
admin.site.register(Post)
