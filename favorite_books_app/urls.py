from django.urls import path
from .views import *

urlpatterns = [
    path('', homePage),
    path('verify_registration', verify_registration),
    path('verify_login', verify_login),
    path('books', login_successful),
    path('books/addBook', addBook),
    # path('books/edit/<int:id>', editBook),
    path('books/<int:id>', viewBook),
    path('books/update/<int:id>', updateBook),
    path('books/addFavorite/<int:id>', addFavorite),
    path('books/removeFavorite/<int:id>', removeFavorite),
    path('books/delete/<int:id>', deleteBook),
    path('logout', logout),
]