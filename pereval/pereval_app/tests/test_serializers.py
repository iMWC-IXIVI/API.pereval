from django.test import TestCase

from pereval_app.serializers import PerUserSerializer

from .test_urls import CreateData


# class SerializersTestCase(TestCase, CreateData):
#     def test_user(self):
#         data = self.data_create()['user']
#         serializer = PerUserSerializer(data).data
#         success_data = {
#             'id': data.pk,
#             'email': data.email,
#             'fam': data.fam,
#             'name': data.name,
#             'otc': data.otc,
#             'phone': data.phone
#         }
#         self.assertEqual(serializer, success_data)
