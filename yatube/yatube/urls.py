from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Главная страница:
    # если получен запрос без относительного адреса
    # (то есть это запрос к имени домена, например yatube.com),
    # будет вызвана функция index() из файла views.py
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', include('posts.urls', namespace='posts')),
    path('about/', include('about.urls', namespace='about')),
]
