from random import randint
from django.utils import timezone
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.baseconv import base56

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .forms import ImageForm, LoginForm
from .models import Image, Like
# Create your views here.


def index(request):
    form = ImageForm()
    images = Image.objects.all().order_by('-upload_datetime')[:12]
    msg = 'Недавно загруженные'
    return render(
        request, 'index.html', {'form': form, 'images': images, 'msg': msg})


def load_pic(request):
    if request.method == 'POST':
        form = ImageForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            print(dir(image))
            image.key = base56.encode(randint(0, 0x7fffff))
            image.file_size = round(image.picture.size / (1024 * 1024), 3)
            image.save()
            if request.user.is_authenticated():
                image.user = User.objects.get(username=request.user.username)
                image.save()
                return redirect('/profile/{}/'.format(request.user.id))
            return redirect('/{}'.format(image.key))
    return redirect('index')


def pic_page(request, key):
    image = get_object_or_404(Image, key=key)
    image.last_view_datetime = timezone.now()
    image.view_count = F('view_count') + 1
    image.save()
    image.refresh_from_db()
    likes = Like.objects.filter(image=image).count()
    likes = likes if likes > 0 else ''
    owner = request.user == image.user
    return render(
        request, 'pic_page.html',
        {'image': image, 'likes': likes, 'owner': owner})


def del_image(request):
    image_key = request.POST.get('key', None)
    image = get_object_or_404(Image, key=image_key)
    user = get_object_or_404(User, username=request.user.username)
    if image and image.user.username == user.username:
        image.picture.storage.delete(image.picture.path)
        image.delete()
        return HttpResponse(1)


def popular(request):
    images = Image.objects.all().order_by('-view_count')[:12]
    msg = 'Самые просматриваемые изображения'
    return render(request, 'popular.html', {'images': images, 'popular': msg})


def set_like(request):
    image_key = request.POST.get('key', None)
    if image_key:
        image = get_object_or_404(Image, key=image_key)
        user = get_object_or_404(User, username=request.user.username)
        likes = Like.objects.filter(image=image).count()
        user_like, create = Like.objects.get_or_create(user=user, image=image)
        if create:
            return HttpResponse(likes + create)
        else:
            _ = user_like.delete()
            return HttpResponse(likes - 1)
    return HttpResponse(0)


# USER
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        msg = form.errors
        return render(request, 'register.html', {'form': form, 'msg': msg})
    form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required(login_url='/login/')
def profile(request, user_id):
    if not user_id.isdigit() or int(user_id) != request.user.pk:
        return redirect('index')
    user = get_object_or_404(User, id=user_id)
    images = Image.objects.filter(user=user).order_by('-upload_datetime')
    return render(request, 'profile.html', {'images': images})


def login_view(request):
    if request.user.is_authenticated():
        return redirect('/profile/{}/'.format(request.user.id))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                # the password verified for the user
                if user.is_active:
                    login(request, user)
                    return redirect('/profile/{}/'.format(user.id))
    form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')
