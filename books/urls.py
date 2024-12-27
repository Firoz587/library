from django.urls import path
from .views import BookDetailsView, AddBookView, EditBookView, DeleteBookView, BuyBookView,DepositMoneyView
from . import views
urlpatterns = [    
    path('view/<int:id>/', BookDetailsView.as_view(), name='view_book'),
    path('add/', AddBookView.as_view(), name='add_book'),
    path('edit/<int:id>', EditBookView.as_view(), name='edit_book'),
    path('delete/<int:id>', DeleteBookView.as_view(), name='delete_book'),
    # path('buy_now/<int:id>/', BuyBookView, name='buy_now'),
    # path('deposit/', views.deposit_money, name='deposit_money'),
    path('deposit/', DepositMoneyView.as_view(), name='deposit_money'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('return/<int:borrowing_id>/', views.return_book, name='return_book'),
    path('history/', views.borrowing_history, name='borrowing_history'),
]