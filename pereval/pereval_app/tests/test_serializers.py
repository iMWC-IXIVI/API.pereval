import pdb

from django.test import TestCase

from pereval_app.serializers import (PerUserSerializer, CordsSerializer,
                                     LevelSerializer, PerevalSerializer,
                                     ImageSerializer)

from .test_urls import CreateData


class SerializersTestCase(TestCase, CreateData):
    def test_user(self):
        data = self.user_create()
        serializer = PerUserSerializer(data).data
        static_data = {
            'id': data.pk,
            'email': data.email,
            'fam': data.fam,
            'name': data.name,
            'otc': data.otc,
            'phone': data.phone
        }
        self.assertEqual(serializer, static_data)

    def test_cords(self):
        data = self.cords_create()
        serializer = CordsSerializer(data).data
        static_data = {
            'id': 1,
            'latitude': 45.3842,
            'longitude': 7.1525,
            'height': 1200
        }
        self.assertEqual(serializer, static_data)

    def test_level(self):
        data = self.level_create()
        serializer = LevelSerializer(data).data
        static_data = {
            'id': 2,
            'winter': '',
            'summer': '1A',
            'autumn': '1A',
            'spring': '',
        }
        self.assertEqual(serializer, static_data)

    def test_pereval(self):
        data = self.pereval_create()
        serializer = PerevalSerializer(data).data
        static_data = {
            'id': 2,
            'status': 'new',
            'beauty_title': 'пер.',
            'title': 'Пхия',
            'other_titles': 'Триев',
            'connect': '',
            'add_time': '2021-09-22 13:18:13',
            'user': 2,
            'coords': 3,
            'level': 3
        }
        self.assertEqual(serializer, static_data)

    def test_images(self):
        data = self.data_create()
        serializer = ImageSerializer(data['images']).data
        static_data = {
            'id': 1,
            'data': '/images/test_image.jpg',
            'title': 'Test',
            'pereval': 1
        }
        self.assertEqual(serializer, static_data)
        data['images'].data.delete(save=True)
