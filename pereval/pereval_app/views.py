from rest_framework import views, response

from django.conf import settings

from .serializers import (PerUserSerializer, CordsSerializer,
                          LevelSerializer, PerevalSerializer,
                          ImageSerializer)
from .models import PerUser, Cords, Level, Pereval


class SubmitData(views.APIView):

    def post(self, request, *args, **kwargs):

        images = request.data.pop('images')

        user = request.data.pop('user')
        user_serializer = PerUserSerializer(data=user)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        cords = request.data.pop('coords')
        cords_serializer = CordsSerializer(data=cords)
        cords_serializer.is_valid(raise_exception=True)
        cords_serializer.save()

        level = request.data.pop('level')
        level_serializer = LevelSerializer(data=level)
        level_serializer.is_valid(raise_exception=True)
        level_serializer.save()

        request.data['user'] = PerUser.objects.last().pk
        request.data['coords'] = Cords.objects.last().pk
        request.data['level'] = Level.objects.last().pk
        pereval_serializer = PerevalSerializer(data=request.data)
        pereval_serializer.is_valid(raise_exception=True)
        pereval_serializer.save()

        for image in images:
            image['pereval'] = Pereval.objects.last().pk
            image_serializer = ImageSerializer(data=image)
            image_serializer.is_valid(raise_exception=True)
            image_serializer.save()

        return response.Response({'Data': request.data})
