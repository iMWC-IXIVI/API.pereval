from django.db import transaction

from rest_framework import views, response, status

from .serializers import (PerUserSerializer, CordsSerializer,
                          LevelSerializer, PerevalSerializer,
                          ImageSerializer)
from .models import PerUser, Cords, Level, Pereval
from .constant import NEW


class SubmitData(views.APIView):

    def post(self, request, *args, **kwargs):

        try:
            user = request.data.pop('user')
            cords = request.data.pop('coords')
            level = request.data.pop('level')
            images = request.data.pop('images')
        except KeyError as e:
            return response.Response({'status': status.HTTP_400_BAD_REQUEST,
                                      'message': f'Ошибка в названии поля {e}'})

        try:
            with transaction.atomic():
                user_serializer = PerUserSerializer(data=user)
                user_serializer.is_valid(raise_exception=True)
                user_serializer.save()

                cords_serializer = CordsSerializer(data=cords)
                cords_serializer.is_valid(raise_exception=True)
                cords_serializer.save()

                level_serializer = LevelSerializer(data=level)
                level_serializer.is_valid(raise_exception=True)
                level_serializer.save()

                request.data['user'] = PerUser.objects.last().pk
                request.data['coords'] = Cords.objects.last().pk
                request.data['level'] = Level.objects.last().pk
                request.data['status'] = NEW
                pereval_serializer = PerevalSerializer(data=request.data)
                pereval_serializer.is_valid(raise_exception=True)
                pereval_serializer.save()

                for image in images:
                    image['pereval'] = Pereval.objects.last().pk
                    image_serializer = ImageSerializer(data=image)
                    image_serializer.is_valid()
                    image_serializer.save()
        except Exception as e:
            return response.Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                                      'message': f'Данные не сохранены. Ошибка: {e}'})

        return response.Response(data={'status': status.HTTP_200_OK,
                                       'message': 'Данные сохранены',
                                       'id': PerevalSerializer(Pereval.objects.last()).data['id']})


class DetailSubmitData(views.APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        pereval = Pereval.objects.get(pk=pk)

        serializer = PerevalSerializer(pereval).data
        serializer['user'] = PerUserSerializer(PerUser.objects.get(pk=serializer['user'])).data

        return response.Response({'data': serializer})

    def put(self, request, *args, **kwargs):
        pass
