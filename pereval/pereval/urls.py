from django.contrib import admin
from django.urls import path, include

from drf_spectacular import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pereval_app.urls')),

    path('api/schema/', views.SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', views.SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
