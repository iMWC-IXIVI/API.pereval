from rest_framework import serializers

from .models import PerUser, Cords, Level, Pereval, Image


class PerevalSerializer(serializers.Serializer):

    beauty_title = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=100)
    other_titles = serializers.CharField(max_length=100)
    connect = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)
    add_time = serializers.DateTimeField(read_only=True)

    user = serializers.PrimaryKeyRelatedField(queryset=PerUser.objects.all())
    coords = serializers.PrimaryKeyRelatedField(queryset=Cords.objects.all())
    level = serializers.PrimaryKeyRelatedField(queryset=Level.objects.all())

    def create(self, validated_data):
        return Pereval.objects.create(**validated_data)


class PerUserSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=255)
    fam = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)
    otc = serializers.CharField(max_length=100)
    phone = serializers.CharField()

    def create(self, validated_data):
        return PerUser.objects.create(**validated_data)


class CordsSerializer(serializers.Serializer):

    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    height = serializers.IntegerField()

    def create(self, validated_data):
        return Cords.objects.create(**validated_data)


class LevelSerializer(serializers.Serializer):

    winter = serializers.CharField(max_length=2, allow_null=True, allow_blank=True)
    summer = serializers.CharField(max_length=2, allow_null=True, allow_blank=True)
    autumn = serializers.CharField(max_length=2, allow_null=True, allow_blank=True)
    spring = serializers.CharField(max_length=2, allow_null=True, allow_blank=True)

    def create(self, validated_data):
        return Level.objects.create(**validated_data)


class ImageSerializer(serializers.Serializer):

    data = serializers.ImageField()
    title = serializers.CharField(max_length=100)

    pereval = serializers.PrimaryKeyRelatedField(queryset=Pereval.objects.all())

    def create(self, validated_data):
        return Image.objects.create(**validated_data)
