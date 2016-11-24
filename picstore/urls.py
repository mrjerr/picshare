from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from . import views

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^load_pic/$', views.load_pic, name='load_pic'),
    url(r'^popular/$', views.popular, name='popular'),
    url(r'^set_like/$', views.set_like, name='set_like'),
    url(r'^del_image/$', views.del_image, name='del_image'),
    url(r'^profile/(\w+)/$', views.profile, name='profile'),
    url(r'^login/$', views.login_view, name='Login'),
    url(r'^register/$', views.register, name='Register'),
    url(r'^logout/$', views.logout_view, name='Logout'),
    url(r'^(\w+)/$', views.pic_page, name='pic_page'),

]

# add to the bottom of your file
if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
