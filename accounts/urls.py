from django.conf.urls import url, include
from .views import *


urlpatterns = [
    url(r'^category/list/$', CategoryAPIViewSet.as_view({'get': 'list', }),
        name='category_list'),
    url(r'^category/create/$', CategoryAPIViewSet.as_view({'post': 'create', }),
        name='post_create'),
    url(r'^subcategory/list/$', SubCategoryAPIViewSet.as_view({'get': 'list', }),
        name='sub_category_list'),
    url(r'^subcategory/create/$', SubCategoryAPIViewSet.as_view({'post': 'create', }),
        name='post_create'),
    url(r'^app/login/', obtain_jwt_token),
    url(r'^app/signup/$', NormalUserCreateViewSet.as_view({'post': 'create', }),
        name='normal_user_create'),
    url(r'^app/otp_verify/$', NormalUserViewSet.as_view({'post': 'verify_mobile', }),
        name='otp_verify'),
    url(r'^app/otp_resend/$', NormalUserViewSet.as_view({'post': 'resend_otp', }),
        name='otp_resend'),
    url(r'^app/password/change/$', ChangePasswordView.as_view(),
        name='password_change'),
    url(r'^app/reset/email/$', PasswordOtpAPI.as_view(),
        name='reset_password_email'),
    url(r'^app/reset/otp/$', ResetPasswordAPI.as_view({'post': 'otp_email',}),
        name='reset_password_otp'),
    url(r'^app/reset/new_password/$', ResetPasswordAPI.as_view({'post': 'new_password', }),
        name='reset_new_password'),
    url(r'^app/profile/$', NormalUserViewSet.as_view({'get': 'profile', }),
        name='profile'),
    url(r'^app/update/profile/$', NormalUserViewSet.as_view({'post': 'update_profile', }),
        name='profile'),
    url(r'^app/post/', include('events.urls')),
    url(r'^app/user/profile/$',
        OtherProfilePage.as_view({'post': 'friend_profile'}),
        name='friend_profile'),
    url(r'^login/$', SuperAdminApiView.as_view({'post': 'login', }), name='super_login'),
]
