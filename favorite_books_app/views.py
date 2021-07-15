from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.

def homePage(request):
    return render(request, 'homePage.html')

def verify_registration(request):
    errors = User.objects.userValidation(request.POST)
    user_email = User.objects.filter(email = request.POST['email'])
    if user_email:
        messages.error(request, "Email already exists")
        return redirect('/')

    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/')

    password = request.POST['password']
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = hashed_password
        )
    request.session['logged_in_user'] = new_user.id
    return redirect('/books')

def verify_login(request):
    user = User.objects.filter(email=request.POST['login_email'])
    if user:
        login_user = user[0]
        if bcrypt.checkpw(request.POST['login_password'].encode(), login_user.password.encode()):
            request.session['logged_in_user'] = login_user.id
            return redirect('/books')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('/')
    messages.error(request, "Invalid email address")
    return redirect('/')

def login_successful(request):
    context = {
        "user": User.objects.get(id=request.session['logged_in_user']),
        "books": Book.objects.all()
    }
    return render(request, 'add_books.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def addBook(request):
    title = request.POST['title']
    description = request.POST['description']
    if len(title) < 2:
        messages.error(request, "Title must be at least 2 characters")
    if len(description) < 5:
        messages.error(request, "Description must be at least 5 characters")
        return redirect('/books')
    user_id = User.objects.get(id=request.session["logged_in_user"])
    new_book = Book.objects.create(
        title = request.POST['title'],
        description = request.POST['description'],
        uploaded_by = user_id,
    )
    user_id.books_liked.add(new_book)
    return redirect('/books')

# def editBook(request, id):
#     book = Book.objects.get(id=id)
#     context = {
#         "user": User.objects.get(id=request.session["logged_in_user"]),
#         "liked_by": book.liked_by.all(),
#         "all_users": User.objects.all(),
#         "this_book": book
#     }
#     return render(request, 'edit_books.html', context)

def viewBook(request, id):
    book = Book.objects.get(id=id)
    context = {
        "user": User.objects.get(id=request.session["logged_in_user"]),
        "liked_by": book.liked_by.all(),
        "all_users": User.objects.all(),
        "this_book": book
    }
    return render(request, 'view_books.html', context)

def updateBook(request, id):
    book = Book.objects.get(id=id)
    book.title = request.POST['update_title']
    book.description = request.POST['update_description']
    book.save()
    return redirect('/books')

def addFavorite(request, id):
    user1 = User.objects.get(id=request.session['logged_in_user'])
    book = Book.objects.get(id=id)
    book.liked_by.add(user1)
    return redirect(f'/books/{id}')

def removeFavorite(request, id):
    user1 = User.objects.get(id=request.session['logged_in_user'])
    book = Book.objects.get(id=id)
    book.liked_by.remove(user1)
    return redirect(f'/books/{id}')

def deleteBook(request, id):
    this_book = Book.objects.get(id=id)
    this_book.delete()
    return redirect('/books')