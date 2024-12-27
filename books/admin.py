from django.contrib import admin
from .models import Book, Comment, Borrowing,UserProfile
# Register your models here.
admin.site.register(Book)
admin.site.register(Comment)
admin.site.register(Borrowing)
admin.site.register(UserProfile)