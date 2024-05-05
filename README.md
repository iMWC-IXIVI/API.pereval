# Pereval API
![PyPI - Version](https://img.shields.io/pypi/v/Django?label=django)
![PyPI - Version](https://img.shields.io/pypi/v/djangorestframework?label=DRF)
![PyPI - Version](https://img.shields.io/pypi/v/drf-spectacular?label=drf-pectacular)
___
___ФТСР___ - Организация, занимающаяся развитием и популяризацией спортивного туризма в России и 
руководящая проведением всероссийских соревнования в этом виде спорта.

__Pereval API__ - Компания _ФТСР_ ведёт базу горных перевалов, которая пополняется туристами. 
Задача API максимально автоматизировать процесс добавления перевалов.
Система требует изменения в виду отсутствия своевременной информации по перевалам.

+ ___Задачи___ - Во время проекта были поставлены задачи по разработке программного интерфейса приложения (API).
Задачи разделились на 3 недели:
  + ___1 неделя___ - Изменение базы данных, и создание метода по приему данных от пользователя;
  + ___2 неделя___ - Создание методов по изменению и выводу информации, а также деплой проекта на хостинге;
  + ___3 неделя___ - Создание тестов и подготовка документации.
___
## _Local installation_
___
Локальная установка проекта, выполните ряд команд:

1. Клонирование проекта: `git clone https://github.com/iMWC-IXIVI/API.pereval.git`;
2. Создание виртуального окружения: `python -m venv venv`;
3. Установка библиотек проекта: `pip install -r lib.txt`;
4. Изменение переменных в настройках проекта:
```python
SECRET_KEY = os.getenv('SECRET_KEY') # Ключ django
ALLOWED_HOSTS = [os.getenv('ALLOWED_HOSTS')] # Допустимые адресса
DATABASES = {
  'default': {
    'ENGINE': os.getenv('ENGINE'),
    'USER': os.getenv('USER'),
    'PASSWORD': os.getenv('PASSWORD'),
    'HOST': os.getenv('HOST'),
    'NAME': os.getenv('NAME'),
    'PORT': os.getenv('PORT'),
  } 
} # Настройка базы данных
```
5. Создание папку media в корневом каталоге проекта:
   1. Дерриктория media отвечает за загрузку image файлов перевала;
6. Запуск тестов:
   1. Для начала перейти в дерриктория с файлом manage.py: `cd pereval`;
   2. Запустить тесты: `python manage.py test`;
   
Все, проект полностью готов к работе, запуск проекта:
1. Перейти в дирректорию с файлом manage.py: `cd pereval`
2. Запустить сервер: `python manage.py runserver`
___
## _URLPATTERNS_ and _SWAGGER_
___
В проекте подключен SWAGGER для удобного тестирования API. Все возможные паттерны проекта:
```python
from django.contrib import admin
from django.urls import path, include

from drf_spectacular import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pereval_app.urls')),

    path('api/schema/', views.SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', views.SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
```
```python
from django.urls import path

from .views import SubmitData, DetailSubmitData


urlpatterns = [
    path('submitData/', SubmitData.as_view(), name='submit_post_api'),
    path('submitData/<int:pk>/', DetailSubmitData.as_view(), name='detail_patch_api'),
]
```
Пример: если вы развернули проекта локально, 
то путь до документации [SWAGGER](http://127.0.0.1:8000/api/schema/swagger-ui/), не забудьте запустить сервер. 
Сервер проекта находится [ТУТ](http://tta3k.pythonanywhere.com/api/schema/swagger-ui/#/).
