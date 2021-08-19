from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.utils import timezone

from .forms import TodoForm
from .models import TodoItem


def home(request):

    return render(
        request,
        'todo/home.html',
        { }
    )

@login_required
def completed_todos(request):

    items = TodoItem.objects.filter(user = request.user, date_completed__isnull=False).order_by('-date_completed')

    return render(
        request,
        'todo/completed.html',
        { 'items' : items }
    )


def signupuser(request):

    if request.method == 'GET':

        return render(
            request,
            'todo/signupuser.html',
            { 'form': UserCreationForm() }
        )

    else:

        if request.POST['password1'] == request.POST['password2']:

            try:
                # create a new user
                user = User.objects.create_user(
                    request.POST['username'],
                    password = request.POST['password1']
                )

                user.save()

                login(request, user)

                return redirect('current_todos')

            except IntegrityError as err:
                return render(
                    request,
                    'todo/signupuser.html',
                    { 'form': UserCreationForm(), 'error': 'The user has already been taken. Please choose a new username' }
                )



        # passwords dont match
        else:

            return render(
                request,
                'todo/signupuser.html',
                { 'form': UserCreationForm(), 'error': 'Passwords didnt match' }
            )



@login_required
def current_todos(request):

    items = TodoItem.objects.filter(user = request.user, date_completed__isnull=True)

    return render(
        request,
        'todo/current_todos.html',
        { 'items' : items }
    )


def login_user(request):
    if request.method == 'GET':

        return render(
            request,
            'todo/login.html',
            { 'form': AuthenticationForm() }
        )

    else:

        if len(request.POST['password']) > 0:

            user = authenticate(
                request,
                username=request.POST['username'],
                password=request.POST['password']
            )

            if user is None:

                return render(
                    request,
                    'todo/login.html',
                    { 'form': AuthenticationForm(), 'error': 'Username/Password didnt match' }
                )
            else:
                login(request, user)
                return redirect('home')


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def create_todo(request):

    if request.method == 'GET':

        return render(
            request,
            'todo/create_todo.html',
            { 'form': TodoForm()  }
        )

    else:

        try:

            form = TodoForm(request.POST)
            newItem = form.save(commit = False)
            newItem.user = request.user
            newItem.save()

        except ValueError:

            return render(
                request,
                'todo/create_todo.html',
                { 'form': TodoForm(), 'error': 'Bad data passed in. Try again.' }
            )

        # ok
        return redirect('current_todos')


@login_required
def view_todo(request, todo_pk):

    itm = get_object_or_404(TodoItem, pk = todo_pk, user = request.user)


    if request.method == 'GET':

        form = TodoForm(instance = itm)

        return render(
            request,
            'todo/view_todo.html',
            { 'itm': itm, 'form': form }
        )

    else:

        try:

            form = TodoForm(request.POST, instance = itm)
            form.save()

        except ValueError:

            return render(
                request,
                'todo/view_todo.html',
                { 'form': TodoForm(), 'itm': itm, 'error': 'Bad data passed in. Try again.' }
            )

        # ok
        return redirect('current_todos')



@login_required
def complete_todo(request, todo_pk):

    itm = get_object_or_404(TodoItem, pk = todo_pk, user = request.user)

    if request.method == 'POST':

        itm.date_completed = timezone.now()
        itm.save()

        return redirect('current_todos')


@login_required
def delete_todo(request, todo_pk):

    itm = get_object_or_404(TodoItem, pk = todo_pk, user = request.user)

    if request.method == 'POST':

        itm.delete()

        return redirect('current_todos')
