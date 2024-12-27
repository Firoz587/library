from django.urls import path
from .views import AddCategoryView
urlpatterns = [    
    path('add/', AddCategoryView.as_view(), name='add_category'),
]