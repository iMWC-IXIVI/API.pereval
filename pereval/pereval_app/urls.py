from django.urls import path

from .views import SubmitData


urlpatterns = [
    path('', SubmitData.as_view())
]
