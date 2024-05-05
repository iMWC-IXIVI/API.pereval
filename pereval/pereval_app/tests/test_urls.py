from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from rest_framework.test import APITestCase
from rest_framework import status

from pereval_app.models import Pereval, PerUser, Level, Cords, Image


class CreateData:
    """Класс по созданию объектов в базе данных"""
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

    def user_create(self):
        user = PerUser.objects.create(email='test@test.test',
                                      fam='Testing',
                                      name='Test',
                                      otc='Testingovich',
                                      phone='+7 800 555 35 35')
        return user

    def cords_create(self):
        coords = Cords.objects.create(latitude=45.3842,
                                      longitude=7.1525,
                                      height=1200)
        return coords

    def level_create(self):
        level = Level.objects.create(winter='',
                                     summer='1A',
                                     autumn='1A',
                                     spring='')
        return level

    def pereval_create(self):
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
                                         user=user,
                                         coords=coords,
                                         level=level)
        return pereval


class ViewGetEmailTestCase(APITestCase, CreateData):
    """Тестирование ответов по введенному в фильтре email"""
    def test_submit_email_100(self):

        url = reverse('submit_post_api')
        result = self.client.get(path=url)
        self.assertEqual(result.status_code, status.HTTP_100_CONTINUE)

        static_data = {'status': 100,
                       'message': 'enter path: ?user__email=user_email'}
        response_data = result.data
        self.assertEqual(response_data, static_data)

    def test_submit_email_200(self):

        data = self.data_create()
        result = self.client.get(f'{reverse("submit_post_api")}?user__email={data["user"].email}')
        self.assertEqual(result.status_code, status.HTTP_200_OK)

        static_data = {
            'id': 3,
            'status': 'new',
            'beauty_title': 'пер.',
            'title': 'Пхия',
            'other_titles': 'Триев',
            'connect': '',
            'add_time': '2021-09-22T13:18:13',
            'coords': {'id': 4,
                       'latitude': 45.3842,
                       'longitude': 7.1525,
                       'height': 1200},
            'level': {'id': 4,
                      'winter': '',
                      'summer': '1A',
                      'autumn': '1A',
                      'spring': ''},
            'images': [{'id': 2,
                        'data': '/images/test_image.jpg',
                        'title': 'Test'}]
        }
        response_data = result.data['result'][data['user'].email][0]
        self.assertEqual(response_data, static_data)
        data['images'].data.delete(save=True)

    def test_submit_email_404(self):
        url = f'{reverse("submit_post_api")}?user__emal=test'
        result = self.client.get(path=url)
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotIn('user__email', result.wsgi_request.GET)

    def test_submit_email_500(self):
        url = f'{reverse("submit_post_api")}?user__email=test'
        result = self.client.get(path=url)
        static_data = {
            'status': 500,
            'message': 'Email not found'
        }
        self.assertEqual(result.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(result.data, static_data)


class ViewGetPkTestCase(APITestCase, CreateData):
    """Тестирование ответов по введенному уникальному ключу перевала"""
    def test_detail_pk_200(self):
        data = self.data_create()
        result = self.client.get(reverse(viewname='detail_patch_api', kwargs={'pk': data['pereval'].pk}))
        self.assertEqual(result.status_code, status.HTTP_200_OK)

        static_data = {
            'id': 4,
            'status': 'new',
            'beauty_title': 'пер.',
            'title': 'Пхия',
            'other_titles': 'Триев',
            'connect': '',
            'add_time': '2021-09-22T13:18:13',
            'user': {'id': 5,
                     'email': 'test@test.test',
                     'fam': 'Testing',
                     'name': 'Test',
                     'otc': 'Testingovich',
                     'phone': '+7 800 555 35 35'},
            'coords': {'id': 5,
                       'latitude': 45.3842,
                       'longitude': 7.1525,
                       'height': 1200},
            'level': {'id': 5,
                      'winter': '',
                      'summer': '1A',
                      'autumn': '1A',
                      'spring': ''},
            'images': [{'id': 3,
                        'data': '/images/test_image.jpg',
                        'title': 'Test'}]
        }
        response_data = result.data['result'][f'data #{data["pereval"].pk}']
        self.assertEqual(response_data, static_data)
        data['images'].data.delete(save=True)

    def test_detail_pk_500(self):

        url = reverse(viewname='detail_patch_api', kwargs={'pk': 100})
        result = self.client.get(url)
        self.assertEqual(result.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

        static_data = {
            'status': 500,
            'message': 'data not found'
        }
        self.assertEqual(result.data, static_data)


class ViewPostTestCase(APITestCase):
    """Тест создания перевала"""
    def test_post_400(self):

        url = reverse(viewname='submit_post_api')
        result = self.client.post(path=url)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

        static_data = {
            'status': 400,
            'message': "Error field 'user'"
        }
        self.assertEqual(result.data, static_data)

        data = '''{"beauty_title": "пер. ",
                   "title": "Пхия",
                   "other_titles": "Триев",
                   "connect": "",
                   "add_time": "2021-09-22 13:18:13",
                   "user": {"email": "qwerty@mail.ru",
                            "fam": "Пупкин",
                            "name": "Василий",
                            "otc": "Иванович",
                            "phone": "+7 555 55 55"},
                   "coords": {"latitude": "45.3842",
                              "longitude": "7.1525",
                              "height": "1200"},
                   "level": {"winter": "",
                             "summer": "1А",
                             "autumn": "1А",
                             "spring": ""},
                   "imagess": [{"data": "😊", "title": "Седловина"},
                               {"data": "😊", "title": "Подъём"}]
                   }'''
        url = reverse(viewname='submit_post_api')
        result = self.client.post(path=url, data=data, content_type='application/json')
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

        static_data = {'status': 400,
                       'message': "Error field 'images'"}
        self.assertEqual(result.data, static_data)

    def test_post_500(self):
        url = reverse(viewname='submit_post_api')
        data = '''{"beauty_title": "пер. ",
                   "title": "Пхия",
                   "other_titles": "Триев",
                   "connect": "",
                   "add_time": "2021-09-22 13:18:13",
                   "user": {"email": "qwerty@mail.ru",
                            "fam": "Пупкин",
                            "name": "Василий",
                            "otc": "Иванович",
                            "phone": "+7 555 55 55"},
                   "coords": {"latitude": "45.3842",
                              "longitude": "7.1525",
                              "height": "1200"},
                   "level": {"winter": "",
                             "summer": "1А",
                             "autumn": "1А",
                             "spring": ""},
                   "images": [{"data": "😊", "title": "Седловина"},
                              {"data": "😊", "title": "Подъём"}]}'''
        result = self.client.post(path=url, data=data, content_type='application/json')
        self.assertEqual(result.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(result.data['status'], status.HTTP_500_INTERNAL_SERVER_ERROR)


class ViewPatchTestCase(APITestCase, CreateData):
    """Тест изменения перевала"""
    def test_patch_400(self):
        data = self.data_create()
        data['pereval'].status = 'not new'
        data['pereval'].save()

        url = reverse(viewname='detail_patch_api', kwargs={'pk': data['pereval'].pk})
        result = self.client.patch(path=url)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

        url = reverse(viewname='detail_patch_api', kwargs={'pk': data['pereval'].pk})
        result = self.client.patch(path=url, data={"": ""})
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        data['images'].data.delete(save=True)

    def test_patch_500(self):
        data = self.data_create()
        url = reverse(viewname='detail_patch_api', kwargs={'pk': 100})

        result = self.client.patch(path=url, data={'': ''})
        self.assertEqual(result.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        static_data = '''{"beauty_title": "пер. ",
                   "title": "Пхия",
                   "other_titles": "Триев",
                   "connect": "",
                   "add_time": "2021-09-22 13:18:13",
                   "user": {"email": "qwerty@mail.ru",
                            "fam": "Пупкин",
                            "name": "Василий",
                            "otc": "Иванович",
                            "phone": "+7 555 55 55"},
                   "coords": {"latitude": "45.3842",
                              "longitude": "7.1525",
                              "height": "1200"},
                   "level": {"winter": "",
                             "summer": "1А",
                             "autumn": "1А",
                             "spring": ""},
                   "images": [{"data": "😊", "title": "Седловина"},
                               {"data": "😊", "title": "Подъём"}]
                   }'''
        url = reverse(viewname='detail_patch_api', kwargs={'pk': data['pereval'].pk})
        result = self.client.patch(path=url, data=static_data, content_type='application/json')
        self.assertEqual(result.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        data['images'].data.delete(save=True)

    def test_patch_200(self):
        data = self.data_create()
        static_data = '''{"beauty_title": "пер. ",
                          "title": "Пхия",
                          "other_titles": "Триев",
                          "connect": "",
                          "add_time": "2021-09-22 13:18:13",
                          "user": {"email": "qwerty@mail.ru",
                                   "fam": "Пупкинc",
                                   "name": "Василийc",
                                   "otc": "Ивановичc",
                                   "phone": "+7 555 55 55"},
                          "coords": {"latitude": "45.3842",
                                   "longitude": "7.1525",
                                   "height": "1200"},
                          "level": {"winter": "",
                                    "summer": "1А",
                                    "autumn": "1А",
                                    "spring": ""},
                          "images": [{"title": "Седловина"}]
                          }'''
        url = reverse(viewname='detail_patch_api', kwargs={'pk': data['pereval'].pk})

        result = self.client.patch(path=url, data=static_data, content_type='application/json')
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        data['images'].data.delete(save=True)
