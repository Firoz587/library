from django.shortcuts import render
from books.models import Book
from categories.models import Category
# Create your views here.
def home(request, category_slug = None):
    categorys = Category.objects.all().order_by('name')
    if category_slug is not None:
        category = Category.objects.get(slug=category_slug)
        books = Book.objects.filter(category=category).order_by('title')
    else:
        books = Book.objects.all().order_by('title')
    return render(request, 'home.html', {'books': books, 'categorys': categorys })