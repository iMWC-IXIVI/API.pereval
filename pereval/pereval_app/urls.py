from django.urls import path

from .views import SubmitData, DetailSubmitData


urlpatterns = [
    path('submitData/', SubmitData.as_view()),
    path('submitData/<int:pk>/', DetailSubmitData.as_view()),
    path('submitData/?user__email=<str:email>/', DetailSubmitData.as_view()),
]
