from django.db import models
from django.contrib.auth.models import User
from categories.models import Category
from django.utils.timezone import now
# Create your models here.
class Book(models.Model):
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
class Borrowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowing_date = models.DateTimeField(auto_now_add=True)
    returned_date = models.DateTimeField(blank=True, null=True)
    amount_deducted = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def is_returned(self):
        return self.returned_date is not None

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.user.username} - Balance: {self.balance}"
    

class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.name}"