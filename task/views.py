
# Create your views here.
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from task.models import *
from .forms import *
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm
from datetime import date

# Create your views here.
def home(request):
    """
    :param request:
    :return: переход на главную страницу
    """

    return render(request, 'task/homepage.html', )


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    redirect(dashboard)
                else:
                    return HttpResponse('Disabled account')
            else:
                return render(request, 'task/login.html', {'form': form})
        else:
            return render(request, 'task/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'task/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        image_form = PhotoEditForm(request.POST)
        if user_form.is_valid() and image_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            new_image = image_form.save()
            # Save the User object
            new_user.save()
            profile = Profile.objects.create(user=new_user, photo=new_image)
            themeform = ThemeForm()
            new_theme = themeform.save(commit=False)
            new_theme.user = request.user
            new_theme.name = "Common"
            new_theme.short_description = "All tasks without theme"
            new_theme.save()
            return render(request, 'task/register_done.html', {'new_user': new_user, 'new_image': new_image})
    else:
        user_form = UserRegistrationForm()
        image_form = PhotoEditForm()
    return render(request, 'task/register.html', {'user_form': user_form, 'image_form': image_form})

@login_required
def dashboard(request):
    print(request.user)
    # themes = Theme.objects.filter(user=request.user.profile.id)
    user = User.objects.get(id=request.user.id)
    themes = Theme.objects.filter(user=request.user.profile.id)
    count = themes.count()
    return render(request, 'task/dashboard.html', {'section': 'dashboard', 'themes': themes, 'count':count})

def logout_view(request):
    logout(request)
    return render(logout(request), 'task/logged_out.html', {'section': 'dashboard'})
    # Redirect to a success page.

@login_required
def user_profile(request):
    user_info = User.objects.get(id=request.user.id)
    # profile_info = Profile.objects(id = request.user.profile.id)
    # photo_info = Image.objects(id = request.user.profile.photo.id)
    print(request.user.first_name)
    return render(request, 'task/profile_user.html', {
        'user_info': user_info,
    })

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        photo_form = PhotoEditForm(instance=request.user.profile.photo, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            photo_form.save()
            return redirect(dashboard)
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        photo_form = PhotoEditForm(instance=request.user.profile.photo, data=request.POST, files=request.FILES)
        return render(request,
                      'task/editprofile.html',
                      {'user_form': user_form,
                       'profile_form': profile_form,
                       'photo_form': photo_form,
                       })
    return render(request,
                  'task/editprofile.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'photo_form': photo_form })

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'task/password_change_form.html', {
        'form': form
    })

def add_task(request):
    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_task = task_form.save(commit=False)
            new_task.user = request.user.profile
            new_task.save()
            # note = Note.objects.create()
            return redirect(current_tasks)
    else:
        task_form = TaskForm()
    return render(request, 'task/addtask.html', {'task_form': task_form})

def current_tasks(request):
    tasks = Note.objects.filter(user=request.user.profile).filter(done=False).order_by('-deadline')
    count = tasks.count()
    print(tasks)
    return render(request, 'task/current_tasks.html',{
        'tasks': tasks,
        'count': count,
    })


def finished_tasks(request):
    tasks = Note.objects.filter(user=request.user.profile).filter(done=True).order_by('-deadline')
    count = tasks.count()
    print(tasks)
    print(tasks.count())
    return render(request, 'task/finished_tasks.html', {
        'tasks': tasks,
        'count': count,
    })

def theme(request, theme_id):
    if request.method == 'GET':
        checkbox_input = request.GET.get("1")
        print(checkbox_input)
        checkbox_input = request.GET.get("2")
        print(checkbox_input)

        themes = Theme.objects.get(user=request.user.profile,id_theme=theme_id)
        tasks = Note.objects.filter(user=request.user.profile).filter(id_theme=theme_id)
        count = tasks.count()
        return render(request, 'task/themes.html', {
            'tasks': tasks,
            'theme': themes,
            'count': count,
        })

    if request.method == 'POST':
        print('xyi')
        tasks = Note.objects.filter(user=request.user.profile).filter(id_theme=theme_id)
        print(tasks)
        checkbox_input = request.POST.getlist('task')
        print(checkbox_input)
        themes = Theme.objects.get(user=request.user.profile,id_theme=theme_id)
        tasks = Note.objects.filter(user=request.user.profile).filter(id_theme=theme_id)
        count = tasks.count()
        return render(request, 'task/themes.html', {
            'tasks': tasks,
            'theme': themes,
            'count': count,
        })

def add_theme(request):
    if request.method == 'POST':
        theme_form = ThemeForm(request.POST)
        print(theme_form.is_valid())
        if theme_form.is_valid():
            print('z nen')
            # Create a new user object but avoid saving it yet
            new_theme = theme_form.save(commit=False)
            new_theme.user = request.user.profile
            new_theme.save()
            print('all ok')
            # note = Note.objects.create()
        return redirect(dashboard)
    else:
        theme_form = ThemeForm()
        return render(request, 'task/addtheme.html', {'theme_form': theme_form})

def edit_task(request, note):
    task_form = TaskForm(instance = Note.objects.get(id_task=note))
    if request.method == 'POST':
        task_form = TaskForm(request.POST, instance=Note.objects.get(id_task=note))
        if task_form.is_valid():
            # Create a new user object but avoid saving it yet
            print('ya tut')
            task_form.save()

            # note = Note.objects.create()
            return redirect(current_tasks)
        else:
            messages.error(request, 'Error updating your task')
    else:
        task_form = TaskForm(instance =  Note.objects.get(id_task=note))
        return render(request,
                  'task/edittask.html',
                  { 'task_form': task_form, })

def edit_theme(request, theme_id):
    if request.method == 'POST':
        theme_form = ThemeForm(request.POST, instance=Theme.objects.get(id_theme=theme_id))
        if theme_form.is_valid():
            # Create a new user object but avoid saving it yet
            print('ya tut')
            theme_form.save()

            # note = Note.objects.create()
            return redirect(dashboard)
        else:
            messages.error(request, 'Error updating your theme')
    else:
        theme_form = ThemeForm(instance=Theme.objects.get(id_theme=theme_id))
        return render(request,
                      'task/edittheme.html',
                      {'theme_form': theme_form, })

def table_tasks(request):
    tasks = Note.objects.filter(user=request.user.profile).filter(done=False).order_by('-deadline')
    count = tasks.count()
    print(tasks)
    return render(request, 'task/table_task.html', {
        'tasks': tasks,
        'count': count,
    })

def task(request, task_id):
    task_form = Note.objects.get(user=request.user.profile, id_task=task_id)
    steps = Step.objects.filter(user_id=request.user.profile).filter(note_id=task_id)
    print(steps)
    count = steps.count()
    return render(request,
                  'task/task.html',
                  { 'task': task_form,
                    'count':count,
                    'steps':steps,})