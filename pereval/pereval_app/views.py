from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import views, response, status

from .serializers import (PerUserSerializer, CordsSerializer,
                          LevelSerializer, PerevalSerializer,
                          ImageSerializer)
from .models import PerUser, Cords, Level, Pereval, Image
from .constant import NEW

from drf_spectacular.utils import (extend_schema, OpenApiParameter, OpenApiExample,
                                   OpenApiResponse, OpenApiTypes, OpenApiRequest)


class SubmitData(views.APIView):

    @extend_schema(parameters=[OpenApiParameter(name='user__email',
                                                description='Введите email пользователя',
                                                type=OpenApiTypes.EMAIL)],
                   description='Поиск пользователя по его email!!!',
                   responses=OpenApiResponse(response=PerevalSerializer,
                                             description='Вывод перевела по email пользователя',
                                             examples=[OpenApiExample(name='Вывод объяснение',
                                                                      value={'id': 'Уникальный номер',
                                                                             'status': 'Статус модерации',
                                                                             'beauty_title': 'Главное название',
                                                                             'title': 'Название',
                                                                             'other_title': 'Альтернативное название',
                                                                             'connect': 'То что соединяет перевал',
                                                                             'add_time': 'Время добавления',
                                                                             'user': 'Добавивший пользователь',
                                                                             'coords': 'Координаты перевала',
                                                                             'level': 'Уровень прохождения 2 символа',
                                                                             'images': 'Список добавленных фотографий'}
                                                                      ),
                                                       OpenApiExample(name='Вывод типов данных',
                                                                      value={'id': 'integer',
                                                                             'status': 'string',
                                                                             'beauty_title': 'string',
                                                                             'title': 'string',
                                                                             'other_title': 'string',
                                                                             'connect': 'string',
                                                                             'add_time': 'datetime',
                                                                             'user': {'email': 'string email',
                                                                                      'fam': 'string',
                                                                                      'name': 'string',
                                                                                      'otc': 'string',
                                                                                      'phone': 'string'},
                                                                             'coords': {'latitude': 'float',
                                                                                        'longitude': 'float',
                                                                                        'height': 'integer'},
                                                                             'level': {'winter': 'string 2 symbol',
                                                                                       'summer': 'string 2 symbol',
                                                                                       'autumn': 'string 2 symbol',
                                                                                       'spring': 'string 2 symbol'},
                                                                             'images': [{'data': 'File (image)',
                                                                                         'title': 'string'}]
                                                                             }
                                                                      )
                                                       ]
                                             )
                   )
    def get(self, request, *args, **kwargs):

        if not request.GET:
            return response.Response({'Enter path': '?user__email=user_email'})

        if not request.GET.get('user__email'):
            return response.Response({'Error': 'Incorrectly path'})

        email = request.GET['user__email']
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

    @extend_schema(description='Добавление нового перевала',
                   request={'multipart/form-data': {'type': 'object',
                                                    'properties': {'beauty_title': {'type': 'string'},
                                                                   'title': {'type': 'string'},
                                                                   'other_titles': {'type': 'string'},
                                                                   'connect': {'type': 'string'},
                                                                   'add_time': {'type': 'string',
                                                                                'format': 'date-time'},
                                                                   'user': {'type': 'object',
                                                                            'format': 'byte',
                                                                            'properties': {'email': {'type': 'string',
                                                                                                     'format': 'email'},
                                                                                           'fam': {'type': 'string'},
                                                                                           'name': {'type': 'string'},
                                                                                           'otc': {'type': 'string'},
                                                                                           'phone': {'type': 'string'}
                                                                                           }
                                                                            },
                                                                   'coords': {'type': 'object',
                                                                              'format': 'byte',
                                                                              'properties': {'latitude': {'type': 'number',
                                                                                                          'format': 'float'},
                                                                                             'longitude': {'type': 'number',
                                                                                                           'format': 'float'},
                                                                                             'height': {'type': 'integer'}
                                                                                             }
                                                                              },
                                                                   'level': {'type': 'object',
                                                                             'format': 'byte',
                                                                             'properties': {'winter': {'type': 'string'},
                                                                                            'summer': {'type': 'string'},
                                                                                            'autumn': {'type': 'string'},
                                                                                            'spring': {'type': 'string'}
                                                                                            }
                                                                             },
                                                                   'image': {'type': 'string',
                                                                             'format': 'binary'},
                                                                   'title_image': {'type': 'string'}}}},
                   responses=OpenApiResponse(response=PerevalSerializer,
                                             description='Вывод данных',
                                             examples=[OpenApiExample(name='return 200',
                                                                      value={'status': 200,
                                                                             'message': 'Данные сохранены',
                                                                             'id': 'Номер добавленного перевала'},
                                                                      description='Успешное выполнение запроса'),
                                                       OpenApiExample(name='return 400',
                                                                      value={'status': 400,
                                                                             'message': 'Ошибка в названии поля',
                                                                             'id': None},
                                                                      description='В случае ошибки в названии поля'),
                                                       OpenApiExample(name='return 500',
                                                                      value={'status': 500,
                                                                             'message': 'Данные не сохранены. Ошибка:',
                                                                             'id': None},
                                                                      description='В случае какой-либо ошибки')]))
    def post(self, request, *args, **kwargs):
        import json

        try:
            if type(request.data['user']) is str:

                user = request.data['user']
                user = json.loads(user)

                cords = request.data['coords']
                cords = json.loads(cords)

                level = request.data['level']
                level = json.loads(level)

                images = [{'data': request.data['image'], 'title': request.data['title_image']}]

            else:
                user = request.data.pop('user')
                cords = request.data.pop('coords')
                level = request.data.pop('level')
                images = request.data.pop('images')
            print((type(user), user), (type(cords), cords), (type(level), level), (type(images), images), sep='\n')
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

    @extend_schema(responses=OpenApiResponse(response=PerevalSerializer,
                                             description='Вывод перевела по его уникальному номеру',
                                             examples=[OpenApiExample(name='Вывод объяснение',
                                                                      value={'Список уникальных номеров записей': f'{Pereval.objects.values("pk").order_by("pk")}',
                                                                             'id': 'Уникальный номер',
                                                                             'status': 'Статус модерации',
                                                                             'beauty_title': 'Главное название',
                                                                             'title': 'Название',
                                                                             'other_title': 'Альтернативное название',
                                                                             'connect': 'То что соединяет перевал',
                                                                             'add_time': 'Время добавления',
                                                                             'user': 'Добавивший пользователь',
                                                                             'coords': 'Координаты перевала',
                                                                             'level': 'Уровень прохождения 2 символа',
                                                                             'images': 'Список добавленных фотографий'}
                                                                      ),
                                                       OpenApiExample(name='Вывод типов данных',
                                                                      value={'id': 'integer',
                                                                             'status': 'string',
                                                                             'beauty_title': 'string',
                                                                             'title': 'string',
                                                                             'other_title': 'string',
                                                                             'connect': 'string',
                                                                             'add_time': 'datetime',
                                                                             'user': {'email': 'string email',
                                                                                      'fam': 'string',
                                                                                      'name': 'string',
                                                                                      'otc': 'string',
                                                                                      'phone': 'string'},
                                                                             'coords': {'latitude': 'float',
                                                                                        'longitude': 'float',
                                                                                        'height': 'integer'},
                                                                             'level': {'winter': 'string 2 symbol',
                                                                                       'summer': 'string 2 symbol',
                                                                                       'autumn': 'string 2 symbol',
                                                                                       'spring': 'string 2 symbol'},
                                                                             'images': [{'data': 'File (image)',
                                                                                         'title': 'string'}]
                                                                             }
                                                                      )
                                                       ]
                                             )
                   )
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
