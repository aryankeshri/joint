import uuid

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin
                                        )
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import Resize

from .validation import (mobile_regex, AlphaSpaceNumUnderscoreDot, image_extension)


GENDER_CHOICE = (
    ('female', 'Female'),
    ('male', 'Male')
)


def upload_image(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex, ext)
    return 'images/{0}/{1}/'.format(instance.__class__.__name__, filename)


# Institute user manager
class UserManager(BaseUserManager):

    def _create_user(self, email, username, mobile, password, **extra_fields):
        """
        Creates and saves a User with the given email, username, mobile and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)

        user = self.model(email=email, username=username, mobile=mobile,
                          date_joined=now,
                          **extra_fields
                          )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, username=None, mobile=None, password=None,
                    **extra_fields):
        """
        Create a Institute Admin User model.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, mobile, password, **extra_fields)

    def create_superuser(self, email, username, mobile, password, **extra_fields):
        """
        Create a Sarvam superadmin model.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')

        return self._create_user(email, username, mobile, password, **extra_fields)


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """ Institute user model """
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(_('Username'),
                                max_length=30,
                                blank=False,
                                null=False,
                                validators=[AlphaSpaceNumUnderscoreDot]
                                )
    mobile = models.CharField(_('Contact no'),
                              max_length=13,
                              blank=True,
                              null=False,
                              validators=[mobile_regex]
                              )
    date_joined = models.DateTimeField(_('date of joining'),
                                       default=timezone.now,
                                       blank=False
                                       )
    country_code = models.CharField(max_length=4, default='+91')
    iso = models.CharField(max_length=4, default='IN')
    is_active = models.BooleanField(_('active'), default=True)
    is_admin = models.BooleanField(_('admin'), default=False)
    is_staff = models.BooleanField(_('staff'), default=True)
    blocked = models.BooleanField(_('blocked'), default=False)
    image = ProcessedImageField(upload_to=upload_image,
                                blank=True, null=True,
                                validators=[image_extension],
                                processors=[Resize(100, 100)],
                                format='JPEG',
                                options={'quality': 70}
                                )

    modified = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    new_mobile = models.CharField(_('Contact no'),
                                  max_length=13,
                                  blank=True,
                                  null=False,
                                  validators=[mobile_regex]
                                  )
    new_country_code = models.CharField(max_length=4, default='+91')
    new_iso = models.CharField(max_length=4, default='IN')
    otp = models.CharField(max_length=6, blank=True, null=False)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=30, blank=True, default='male',
                              choices=GENDER_CHOICE
                              )
    initial_reg = models.BooleanField(default=False)
    final_reg = models.BooleanField(default=False)
    mobile_verify = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'mobile']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        abstract = True

    def __str__(self):
        return str(self.email)+'('+str(self.id)+')'

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def mobile_number(self):
        return self.country_code + self.mobile


class RdxUser(AbstractUser):

    class Meta(AbstractUser.Meta):  # noqa: D101
        swappable = 'AUTH_USER_MODEL'


class Category(models.Model):
    name = models.CharField(max_length=250, default='IN')
    image = ProcessedImageField(upload_to=upload_image,
                                blank=True, null=True,
                                validators=[image_extension],
                                processors=[Resize(100, 100)],
                                format='JPEG',
                                options={'quality': 70}
                                )
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
