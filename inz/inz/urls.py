from django.urls import re_path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.shortcuts import redirect

def redirect_to_login(request):
    return redirect('/account/login_user')

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^account/', include('django.contrib.auth.urls')),
    re_path(r'^account/', include('account.urls')),
    re_path(r'^events/', include('events.urls')),
    re_path(r'^reservation/', include('reservation.urls')),
    re_path(r'^support/', include('support.urls')),
    re_path(r'^company/', include('company.urls')),
    re_path(r'^product/', include('product.urls')),
    re_path(r'home', views.home, name="home"),
    re_path(r'^$', redirect_to_login, name='home-redirect-to-login'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#Configure admin Titles
admin.site.site_header = "Praca Inz"
admin.site.site_title = "Panel Administracyjny"
admin.site.index_title = "Panel Administracyjny"