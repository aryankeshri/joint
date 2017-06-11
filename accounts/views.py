import random

from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from rest_framework_jwt.views import jwt_response_payload_handler, JSONWebTokenAPIView

from .models import *
from .serializers import *
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets, views
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_auth.views import PasswordChangeView


def generate():
    chars = "1234567890"
    while True:
        value = "".join(random.choice(chars) for _ in range(6))
        return value


class CategoryAPIViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)

    def list(self, request, *args, **kwargs):
        cat_obj = Category.objects.all().order_by('-id')
        serializer = CategorySerializer(cat_obj, many=True)
        context = {
            'data': serializer.data,
        }
        return Response(context, status=status.HTTP_200_OK)


class SubCategoryAPIViewSet(viewsets.ModelViewSet):
    serializer_class = SubCategorySerializer
    permission_classes = (permissions.AllowAny,)

    def list(self, request, *args, **kwargs):
        sub_cat_obj = SubCategory.objects.all().order_by('-id')
        serializer = SubCategorySerializer(sub_cat_obj, many=True)
        context = {
            'data': serializer.data,
        }
        return Response(context, status=status.HTTP_200_OK)


class ExtendedJSONWebTokenAPIView(JSONWebTokenAPIView):
    permission_classes = ()
    authentication_classes = ()

    def get_serializer_context(self):
        return {
            'request': self.request,
            'view': self,
        }

    def get_serializer_class(self):
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__)
        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            content = {
                'response_data': jwt_response_payload_handler(token, user, request),
                'status': status.HTTP_200_OK,
            }
            return Response(content, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObtainJSONWebToken(ExtendedJSONWebTokenAPIView):
    serializer_class = ExtendJSONWebTokenSerializer


obtain_jwt_token = ObtainJSONWebToken.as_view()


#SignUp
class NormalUserCreateViewSet(viewsets.ModelViewSet):
    queryset = RdxUser.objects.all()
    serializer_class = NormalUserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        email = self.request.data['email']
        if email:
            user_qs = RdxUser.objects.filter(email__iexact=email, is_active=True)
            if user_qs.exists():
                context = {'message': "This user has already registered."}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_user = RdxUser.objects.create_user(**serializer.validated_data)
            otp = generate()
            new_user.otp = otp
            new_user.mobile_verify = False
            new_user.save()
            context = {
                'data': serializer.data,
                'id': new_user.id,
                'otp': otp,
                'status': status.HTTP_201_CREATED
            }
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            context = {
                'message': 'Could not create',
                'status': status.HTTP_400_BAD_REQUEST,
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class NormalUserViewSet(viewsets.ModelViewSet):
    serializer_class = VerifyMobileSerializer

    def verify_mobile(self, request):
        otp = request.data['otp']
        user = get_object_or_404(RdxUser, email=request.user.email)
        serializer = VerifyMobileSerializer(data=request.data)
        serializer.is_valid()
        if user.initial_reg is not True:
            if user.otp == otp:
                user.initial_reg = True
                user.mobile_verify = True
                user.save()
                context = {
                    'message': 'Mobile no verified.',
                    'status': status.HTTP_200_OK,
                }
                return Response(context, status=status.HTTP_200_OK)
            else:
                context = {
                    'message': 'OTP not correct.',
                    'status': status.HTTP_400_BAD_REQUEST,
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        else:
            context = {
                'message': 'Allready verify this no.',
                'initial_reg': user.initial_reg,
                'status': status.HTTP_400_BAD_REQUEST,
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def resend_otp(self, request):
        user = get_object_or_404(RdxUser, email=request.user.email)
        if user.mobile:
            otp = generate()
            user.otp = otp
            user.save()
            context = {
                'status': status.HTTP_200_OK,
                'otp': otp,
                'message': 'New otp sent.'
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            context = {
                'message': 'Mobile no not entered',
                'status': status.HTTP_400_BAD_REQUEST,
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def profile(self, request):
        user = get_object_or_404(RdxUser, email=request.user.email)
        serializer = ProfileSerializer(user)
        context = {
            'data': serializer.data,
            'status': status.HTTP_200_OK
        }
        return Response(context, status=status.HTTP_200_OK)

    def update_profile(self, request):
        user = get_object_or_404(RdxUser, id=request.user.id)
        new_mobile = request.data['mobile']
        if user.mobile != new_mobile:
            otp = generate()
            user.otp = otp
            user.save()
        if request.data['image'] is None:
            serializer = UpdateProfileSerializer(user, data=request.data,
                                                 remove_fields=('image',)
                                                 )
        else:
            serializer = UpdateProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
        context = {
            'data': serializer.data,
            'otp': otp if otp else '',
            'status': status.HTTP_200_OK
        }
        return Response(context, status=status.HTTP_200_OK)


# Change Password
class ChangePasswordView(PasswordChangeView):
    serializer_class = PasswordChangeSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """
        This method use for change your password
        :param request: old password, new password
        :return: success message or failre message
        """
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(RdxUser, email=request.user.email)
            user.set_password(request.data['new_password'])
            user.save()
            return Response({"message": _("New password has been saved.")})
        else:
            return Response({"message": _("Password not same as your email!"), })


# Forget Password Email
class PasswordOtpAPI(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data['email']
        user = get_object_or_404(RdxUser, email__iexact=email)
        otp = generate()
        user.otp = otp
        user.save()
        if user.initial_reg is True:
            context = {
                'otp': otp,
                'message': 'Successful'
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Initial registration not completed'},
                            status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPI(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)

    def otp_email(self, request):
        """
        OTP,email screen for otp
        :param request: otp, email
        :return: message
        """
        otp = request.data['otp']
        try:
            user = get_object_or_404(RdxUser, email__iexact=request.data['email'])
            if user.otp == otp:
                context = {'message': 'otp verified successful',
                           'status': status.HTTP_200_OK
                           }
                return Response(context, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'OTP did not match'},
                                status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'message': 'Could not reset password'},
                            status=status.HTTP_400_BAD_REQUEST)

    def new_password(self, request):
        """
        Enter New Password screen
        :param request: new_password, email
        :return:
        """
        password = request.data['new_password']
        try:
            user = get_object_or_404(RdxUser, email__iexact=request.data['email'])
            if password:
                user.set_password(password)
                user.save()
                context = {'message': 'Password set successful, '
                                      'login with new credentials',
                           'status': status.HTTP_200_OK
                           }
                return Response(context, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Could not reset password'},
                            status=status.HTTP_400_BAD_REQUEST)


class FriendProfilePage(viewsets.ViewSet):

    def friend_profile(self, request, user=None):
        user = get_object_or_404(RdxUser, id=user, is_active=True, blocked=False)
        if user:
            serializer = ProfileSerializer(user)
            context = {
                'status': status.HTTP_200_OK,
                'message': 'Other user profile page!',
                'data': serializer.data,
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            context = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'some error occur.',
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)