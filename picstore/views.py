from random import randint
from django.utils import timezone
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.baseconv import base56

from .forms import ImageForm
from .models import Image
# Create your views here.


def index(request):
    form = ImageForm()
    return render(request, 'index.html', {'form': form})


def load_pic(request):
    if request.method == 'POST':
        form = ImageForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.key = base56.encode(randint(0, 0x7fffff))
            image.save()
            return redirect('/{}'.format(image.key))
    return redirect('index')


def pic_page(request, key):
    image = Image.objects.get(key=key)
    image.last_view_datetime = timezone.now()
    image.view_count = F('view_count') + 1
    image.save()
    image.refresh_from_db()
    return render(request, 'pic_page.html', {'image': image})


def remove_pic(request, key):
    pass
    # i = Image.objects.all()[0]
    # i.picture.storage.delete(i.picture.path)
    # i.delete()


def popular(request):
    images = Image.objects.all().order_by('-view_count', '-likes')[:10]
    return render(request, 'popular.html', {'images': images})


def set_like(request):
    image_key = request.POST.get('key', None)
    if image_key:
        image = Image.objects.get(key=image_key)
        image.likes = F('likes') + 1
        image.save()
        image.refresh_from_db()
        return HttpResponse(image.likes)
    return HttpResponse(0)
