from rest_framework import serializers

from .models import PerUser, Cords, Level, Pereval, Image


class PerevalSerializer(serializers.Serializer):
    """Сериализатор перевала"""
    id = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    beauty_title = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=100)
    other_titles = serializers.CharField(max_length=100)
    connect = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)
    add_time = serializers.DateTimeField()

    user = serializers.PrimaryKeyRelatedField(queryset=PerUser.objects.all())
    coords = serializers.PrimaryKeyRelatedField(queryset=Cords.objects.all())
    level = serializers.PrimaryKeyRelatedField(queryset=Level.objects.all())

    def create(self, validated_data):
        return Pereval.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.beauty_title = validated_data.get('beauty_title', instance.beauty_title)
        instance.title = validated_data.get('title', instance.title)
        instance.other_titles = validated_data.get('other_titles', instance.other_titles)
        instance.connect = validated_data.get('connect', instance.connect)
        instance.add_time = validated_data.get('add_time', instance.add_time)

        instance.save()

        return instance


class PerUserSerializer(serializers.Serializer):
    """Сериализатор пользователя"""
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(max_length=255)
    fam = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)
    otc = serializers.CharField(max_length=100)
    phone = serializers.CharField()

    def create(self, validated_data):
        return PerUser.objects.create(**validated_data)


class CordsSerializer(serializers.Serializer):
    """Сериализатор координат"""
    id = serializers.IntegerField(read_only=True)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    height = serializers.IntegerField()

    def create(self, validated_data):
        return Cords.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.height = validated_data.get('height', instance.height)

        instance.save()

        return instance


class LevelSerializer(serializers.Serializer):
    """Сериализатор уровеня доступности"""
    id = serializers.IntegerField(read_only=True)
    winter = serializers.CharField(max_length=2, allow_null=True, allow_blank=True)
    summer = serializers.CharField(max_length=2, allow_null=True, allow_blank=True)
    autumn = serializers.CharField(max_length=2, allow_null=True, allow_blank=True)
    spring = serializers.CharField(max_length=2, allow_null=True, allow_blank=True)

    def create(self, validated_data):
        return Level.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.winter = validated_data.get('winter', instance.winter)
        instance.summer = validated_data.get('summer', instance.summer)
        instance.autumn = validated_data.get('autumn', instance.autumn)
        instance.spring = validated_data.get('spring', instance.spring)

        instance.save()

        return instance


class ImageSerializer(serializers.Serializer):
    """Сериализатор фотографий"""
    id = serializers.IntegerField(read_only=True)
    data = serializers.ImageField()
    title = serializers.CharField(max_length=100)

    pereval = serializers.PrimaryKeyRelatedField(queryset=Pereval.objects.all())

    def create(self, validated_data):
        return Image.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.data = validated_data.get('data', instance.data)
        instance.title = validated_data.get('title', instance.title)

        instance.save()

        return instance
