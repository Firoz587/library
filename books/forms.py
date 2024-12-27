from django import forms
from .models import Book, Comment
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'comment']
        

class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=1.0)

class BorrowBookForm(forms.Form):
    book_id = forms.IntegerField()

        
