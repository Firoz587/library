from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib import messages
from .forms import BookForm, CommentForm
from .models import Book, Borrowing
# Create your views here.
from django.core.mail import send_mail
from .models import UserProfile
from .forms import DepositForm
from .models import Book, Borrowing
from django.utils.timezone import now
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime
from django.db.models import Sum
from django.http import HttpResponseNotFound
def send_transaction_email(user, amount, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()
@login_required
def borrow_book(request, book_id):
    book = Book.objects.get(id=book_id)
    profile = UserProfile.objects.get(user=request.user)

    if book.quantity < 1:
        messages.error(request, "Book is out of stock!")
        return redirect('home')

    if profile.balance < book.price:
        messages.error(request, "Insufficient balance!")
        return redirect('home')

    # Deduct balance and create borrowing record
    profile.balance -= book.price
    profile.save()
    Borrowing.objects.create(user=request.user, book=book, amount_deducted=book.price)
    book.quantity -= 1
    book.save()


    messages.success(request, f"You borrowed {book.title} successfully!")
    
    return redirect('profile')

# @login_required
# def deposit_money(request):
#     if request.method == "POST":
#         form = DepositForm(request.POST)
#         if form.is_valid():
#             amount = form.cleaned_data['amount']
#             profile = UserProfile.objects.get(user=request.user)
#             profile.balance += amount
#             profile.save()

#             # Send email confirmation
#             send_mail(
#                 "Deposit Confirmation",
#                 f"Dear {request.user.username}, you have successfully deposited {amount} Taka.",
#                 "mdfirozislam940@gmail.com",
#                 [request.user.email],
#             )

#             messages.success(request, f"{amount} Taka deposited successfully!")
#             return redirect('user_profile')
#     else:
#         form = DepositForm()

#     return render(request, 'deposit_money.html', {'form': form})
class DepositMoneyView(LoginRequiredMixin, FormView):
    template_name = 'deposit_money.html'
    form_class = DepositForm
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        amount = form.cleaned_data['amount']
        
        # Ensure the user has a UserProfile
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        profile.balance += amount
        profile.save()


        messages.success(self.request, f"{amount} Taka deposited successfully!")
        # messages.success(
        #     self.request,
        #     f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        # )
        send_transaction_email(self.request.user, amount, "Deposite Message", "deposite_email.html")
        return redirect('profile')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class BookDetailsView(DetailView):
    model = Book
    pk_url_kwarg = 'id'
    template_name = 'view_book.html'
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentForm(data=request.POST)
        
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.book = self.object
            new_comment.save()
            return redirect('view_book', id=self.object.pk)
        
        return self.get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        comments = book.comments.all().order_by('-id')        
        comment_form = CommentForm()
        context['comments'] = comments
        context['comment_form'] = comment_form
        return context
@method_decorator(login_required, name='dispatch')
class AddBookView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'add_book.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        messages.success(self.request, 'Book Added Successfully!')
        return super().form_valid(form)
@method_decorator(login_required, name='dispatch')
class EditBookView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'edit_book.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('home')
    
@method_decorator(login_required, name='dispatch')
class DeleteBookView(DeleteView):
    model = Book
    template_name = 'delete_book.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('home')

@login_required
def BuyBookView(request, id):
    book = Book.objects.get(pk=id)
    if book.quantity > 0:
        book.quantity -= 1
        book.save()
        Borrowing.objects.create(user=request.user, book=book, quantity=1)
        return render(request, 'buy_book.html', {'book': book, 'tag': 'success', 'msg': 'You successfully bought this book!'})
    else:
        return render(request, 'buy_book.html', {'book': book, 'tag': 'danger', 'msg': 'Oops! This Book stock is out!'})
    
@login_required
def return_book(request, borrowing_id):
    # borrowing = Borrowing.objects.get(id=borrowing_id, user=request.user, returned_date__isnull=True)
    borrowing = Borrowing.objects.filter(id=borrowing_id, user=request.user, returned_date__isnull=True).first()
    if not borrowing:
        messages.error(request, "Invalid request!")
        return redirect('profile')
    
    # if not borrowing:
    #     return HttpResponseNotFound("The borrowing record does not exist or is already returned.")

    # Refund the amount
    profile = UserProfile.objects.get(user=request.user)
    profile.balance += borrowing.amount_deducted
    profile.save()

    # Mark the book as returned
    borrowing.returned_date = now()
    borrowing.save()

    book = borrowing.book
    book.quantity += 1
    book.save()

    messages.success(request, f"Successfully returned {book.title}.")
    return redirect('profile')

@login_required
def borrowing_history(request):
    borrowings = Borrowing.objects.filter(user=request.user)
    return render(request, 'borrowing_history.html', {'borrowings': borrowings})