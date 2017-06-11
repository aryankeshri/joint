from django.contrib.auth import update_session_auth_hash, authenticate
from django.conf import settings
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.serializers import (jwt_payload_handler, jwt_encode_handler,
                                            JSONWebTokenSerializer
                                            )
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from .models import *


class ExtendJSONWebTokenSerializer(JSONWebTokenSerializer):
    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }
        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                payload = jwt_payload_handler(user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user,
                }
            else:
                msg = _('Unable to login with provided credentials.')
                raise ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise ValidationError(msg)


class NormalUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,
                                     style={'input_type': 'password'}
                                     )

    class Meta:
        model = RdxUser
        fields = ('id', 'email', 'username', 'password', 'mobile')
        read_only_fields = ('id', 'date_joined', 'last_login',)
        extra_kwargs = dict(password={"write_only": True, })


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'image')
        read_only_fields = ('id',)


class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = SubCategory
        fields = ('id', 'category', 'sb_name')
        read_only_fields = ('id',)


class VerifyMobileSerializer(serializers.Serializer):
    otp = serializers.CharField(required=True)


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, required=True)
    new_password = serializers.CharField(max_length=128, required=True)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RdxUser
        fields = ('id', 'image', 'mobile', 'username', 'email', 'gender', 'age',
                  'location', 'description')
        read_only_fields = ('id',)


class UpdateProfileSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True)

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(UpdateProfileSerializer, self).__init__(*args, **kwargs)

        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

    class Meta:
        model = RdxUser
        fields = ('id', 'image', 'mobile', 'username', 'email', 'gender', 'age',
                  'location', 'description')
        read_only_fields = ('id',)


class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RdxUser
        fields = ('id', 'username', 'image')
        read_only_fields = ('id',)
