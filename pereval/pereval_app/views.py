import os

from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import views, response, status, renderers

from .serializers import (PerUserSerializer, CordsSerializer,
                          LevelSerializer, PerevalSerializer,
                          ImageSerializer)
from .models import PerUser, Cords, Level, Pereval, Image
from .constant import NEW


class SubmitData(views.APIView):

    def get(self, request, *args, **kwargs):

        if not request.GET.get('user__email'):
            return response.Response({'Error': 'Incorrectly path'})

        email = request.GET['user__email'][:-1]
        perevals = Pereval.objects.filter(user__email=email)

        if not perevals:
            return response.Response({'Error': 'Email not found'})

        serializer = PerevalSerializer(perevals, many=True).data

        for data in serializer:

            del data['user']
            data['coords'] = CordsSerializer(Cords.objects.get(pk=data['coords'])).data
            data['level'] = LevelSerializer(Level.objects.get(pk=data['level'])).data
            images = data['images'] = ImageSerializer(Image.objects.filter(pereval__user__email=email), many=True).data

            for image in images:
                del image['pereval']

        return response.Response({email: serializer})

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
                if not PerUser.objects.filter(email=user['email']):
                    user_serializer = PerUserSerializer(data=user)
                    user_serializer.is_valid(raise_exception=True)
                    user_serializer.save()

                cords_serializer = CordsSerializer(data=cords)
                cords_serializer.is_valid(raise_exception=True)
                cords_serializer.save()

                level_serializer = LevelSerializer(data=level)
                level_serializer.is_valid(raise_exception=True)
                level_serializer.save()

                request.data['user'] = PerUser.objects.get(email=user['email']).pk
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

    def get_serializer_class(self):
        return PerevalSerializer


class DetailSubmitData(views.APIView):
    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')

        try:
            pereval = Pereval.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return response.Response({'Error': 'data not found'})

        serializer = PerevalSerializer(pereval).data
        serializer['user'] = PerUserSerializer(PerUser.objects.get(pk=serializer['user'])).data
        serializer['coords'] = CordsSerializer(Cords.objects.get(pk=serializer['coords'])).data
        serializer['level'] = LevelSerializer(Level.objects.get(pk=serializer['level'])).data
        serializer['images'] = ImageSerializer(Image.objects.filter(pereval_id=pk), many=True).data

        for data in serializer['images']:
            del data['pereval']

        return response.Response({f'data #{pk}': serializer})

    def patch(self, request, *args, **kwargs):

        pk = kwargs.get('pk')

        try:
            pereval = Pereval.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return response.Response({'state': 0,
                                      'message': 'data not found'})

        if Pereval.objects.get(pk=kwargs['pk']).status != NEW:
            return response.Response({'state': 0,
                                      'message': f'status not {NEW}'})

        if request.data.get('user'):
            del request.data['user']

        if request.data.get('coords'):

            coords = request.data.pop('coords')

            serializer = CordsSerializer(data=coords, instance=pereval.coords, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        if request.data.get('level'):

            level = request.data.pop('level')

            serializer = LevelSerializer(data=level, instance=pereval.level, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        if request.data.get('images'):

            images = request.data.pop('images')
            instance = Image.objects.filter(pereval=pk)

            if len(images) != len(instance):
                return response.Response({'state': 0,
                                          'message': 'Количество загружаемых объектов превышает количество объектов, '
                                                     'находящихся в базе данных'})

            for counter, data in enumerate(images):
                for instance_counter, instance_data in enumerate(instance):
                    if counter == instance_counter:
                        if data['data']:
                            instance_data.data.delete(save=True)
                        serializer = ImageSerializer(data=data, instance=instance_data, partial=True)
                        serializer.is_valid(raise_exception=True)
                        serializer.save()

        serializer = PerevalSerializer(data=request.data, instance=pereval, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response({'state': 1,
                                  'message': 'success'})

    def get_serializer_class(self):
        return PerevalSerializer
