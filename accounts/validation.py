import os
import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import ungettext, ugettext_lazy as _

mobile_regex = RegexValidator(regex=r'^\d{10,13}$',
                              message=_("Please Enter correct Contact no.")
                              )
alphabetic = RegexValidator(r'^[a-zA-Z]*$',
                            message=_('Only alphabet are allowed.')
                            )
otherpassvalidation = RegexValidator(r"^[a-zA-Z0-9]*$",
                                     message=_('Only alphabet and numbers')
                                     )
alphanumric = RegexValidator(r'^[a-zA-Z0-9]*$',
                             message=_('Only alphanumric characters are allowed.')
                             )
uppernumric = RegexValidator(r'^[A-Z0-9]*$',
                             message=_('Only Uppercase alphabet and numbers '
                                       'are allowed.')
                             )
alphaspace = RegexValidator(r'^[a-zA-Z  .]*$',
                            message=_('Only alphabet are allowed.')
                            )
digits = RegexValidator(r'^[0-9]*$',
                        message=_('Only digits are allowed.')
                        )
alphanumspacedot = RegexValidator(r'^[a-zA-Z0-9 .]*$',
                                  message=_('Only alphabet are allowed.')
                                  )
AlphaSpaceNumUnderscoreDot = RegexValidator(r'^[a-zA-Z0-9_ .,]*$',
                                            message=_('Only alphabet are allowed.')
                                            )


class MaximumLengthValidator(object):
    """
    Validate whether the password max character length.
    """
    def __init__(self, max_length=32):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(
                ungettext(
                    "This password is too long. It must contain at "
                    "least %(max_length)d character.",
                    "This password is too long. It must contain at "
                    "least %(max_length)d characters.",
                    self.max_length
                ),
                code='password_too_long',
                params={'max_length': self.max_length},
            )

    def get_help_text(self):
        return ungettext(
            "Your password must contain at least %(max_length)d character.",
            "Your password must contain at least %(max_length)d characters.",
            self.max_length
        ) % {'max_length': self.max_length}


def image_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extension = ['.jpg', '.png', '.jpeg', '.gif', '.JPG', '.PNG', '.JPEG', '.GIF']
    if not ext.lower() in valid_extension:
        raise ValidationError(_('Unsupported image extension.'))
