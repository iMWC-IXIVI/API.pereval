from django.urls import path

from .views import SubmitData, DetailSubmitData


urlpatterns = [
    # Базовые пути REST API
    path('submitData/', SubmitData.as_view(), name='submit_post_api'),
    path('submitData/<int:pk>/', DetailSubmitData.as_view(), name='detail_patch_api'),
]
