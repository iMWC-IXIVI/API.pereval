import pdb

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from rest_framework.test import APITestCase
from rest_framework import status

from pereval_app.models import Pereval, PerUser, Level, Cords, Image
from pereval_app.serializers import (PerevalSerializer, PerUserSerializer, LevelSerializer,
                                     CordsSerializer, ImageSerializer)


class CreateData:

    def data_create(self):
        user = PerUser.objects.create(email='test@test.test',
                                      fam='Testing',
                                      name='Test',
                                      otc='Testingovich',
                                      phone='+7 800 555 35 35')
        coords = Cords.objects.create(latitude=45.3842,
                                      longitude=7.1525,
                                      height=1200)
        level = Level.objects.create(winter='',
                                     summer='1A',
                                     autumn='1A',
                                     spring='')
        pereval = Pereval.objects.create(beauty_title='пер.',
                                         title='Пхия',
                                         other_titles='Триев',
                                         connect='',
                                         add_time='2021-09-22 13:18:13',
                                         user=PerUser.objects.last(),
                                         coords=Cords.objects.last(),
                                         level=Level.objects.last())
        images = Image.objects.create(title='Test', pereval=pereval)
        images.data = SimpleUploadedFile(name='test_image.jpg',
                                         content=open(f'{settings.STATIC_ROOT}/test.jpg', 'rb').read(),
                                         content_type='image/jpeg')
        images.save()

        return {'user': user, 'coords': coords, 'level': level, 'pereval': pereval, 'images': images}


class ViewsGetTestCase(APITestCase, CreateData):

    def test_submit_email(self):

        data = self.data_create()
        result = self.client.get(f'{reverse("submit_post_api")}?user__email={data["user"].email}')
        self.assertEqual(result.status_code, status.HTTP_200_OK)

        static_data = {
            'id': 2,
            'status': 'new',
            'beauty_title': 'пер.',
            'title': 'Пхия',
            'other_titles': 'Триев',
            'connect': '',
            'add_time': '2021-09-22T13:18:13',
            'coords': {'id': 2,
                       'latitude': 45.3842,
                       'longitude': 7.1525,
                       'height': 1200},
            'level': {'id': 2,
                      'winter': '',
                      'summer': '1A',
                      'autumn': '1A',
                      'spring': ''},
            'images': [{'id': 2,
                        'data': '/images/test_image.jpg',
                        'title': 'Test'}]
        }
        response_data = result.data[data['user'].email][0]
        self.assertEqual(response_data, static_data)
        data['images'].data.delete(save=True)

    def test_detail_pk(self):
        data = self.data_create()
        result = self.client.get(reverse(viewname='detail_patch_api', kwargs={'pk': data['pereval'].pk}))
        self.assertEqual(result.status_code, status.HTTP_200_OK)

        static_data = {
            'id': 1,
            'status': 'new',
            'beauty_title': 'пер.',
            'title': 'Пхия',
            'other_titles': 'Триев',
            'connect': '',
            'add_time': '2021-09-22T13:18:13',
            'user': {'id': 1,
                     'email': 'test@test.test',
                     'fam': 'Testing',
                     'name': 'Test',
                     'otc': 'Testingovich',
                     'phone': '+7 800 555 35 35'},
            'coords': {'id': 1,
                       'latitude': 45.3842,
                       'longitude': 7.1525,
                       'height': 1200},
            'level': {'id': 1,
                      'winter': '',
                      'summer': '1A',
                      'autumn': '1A',
                      'spring': ''},
            'images': [{'id': 1,
                        'data': '/images/test_image.jpg',
                        'title': 'Test'}]
        }
        response_data = result.data['result'][f'data #{data["pereval"].pk}']
        self.assertEqual(response_data, static_data)
        data['images'].data.delete(save=True)
