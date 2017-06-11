from django.conf import settings
from rest_framework import serializers
from .models import *
from accounts.serializers import ListUserSerializer


class PostListSerializer(serializers.ModelSerializer):
    p_user = ListUserSerializer(read_only=True)
    p_date = serializers.DateField(format=settings.DATE_FORMAT, input_formats=None)
    p_time = serializers.TimeField(format=settings.TIME_FORMAT, input_formats=None)

    class Meta:
        model = Post
        fields = ('id', 'p_user',  'p_title', 'p_date', 'p_time', 'p_veg', 'p_time_ago')
        read_only_fields = ('id',)


class PostCreateSerializer(serializers.ModelSerializer):
    p_date = serializers.DateField(format=settings.DATE_FORMAT,
                                   input_formats=None)
    p_time = serializers.TimeField(format=settings.TIME_FORMAT,
                                   input_formats=None)

    class Meta:
        model = Post
        fields = ('id', 'p_user',  'p_title', 'p_date', 'p_time', 'p_person',
                  'p_details')
        read_only_fields = ('id',)


class PostDetailSerializer(serializers.ModelSerializer):
    p_user = ListUserSerializer(read_only=True)
    p_date = serializers.DateField(format=settings.DATE_FORMAT, input_formats=None)
    p_time = serializers.TimeField(format=settings.TIME_FORMAT, input_formats=None)
    c_count = serializers.SerializerMethodField('get_comment_count')

    def get_comment_count(self, instance):
        count = Comment.objects.filter(c_post=instance, c_active=True).count()
        return count

    class Meta:
        model = Post
        fields = ('id', 'p_user',  'p_title', 'p_date', 'p_time', 'p_veg',
                  'p_person', 'p_details', 'c_count', 'p_time_ago')
        read_only_fields = ('id',)


class CommentReplySerializer(serializers.ModelSerializer):
    c_user = ListUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'c_user', 'c_content', 'c_time_ago')
        read_only_fields = ('id',)


class CommentListSerializer(serializers.ModelSerializer):
    c_user = ListUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'c_user', 'c_content', 'c_time_ago')
        read_only_fields = ('id',)


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'c_user', 'c_post', 'c_content')
        read_only = ('id',)
