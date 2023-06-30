from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Model(models.Model):
    id = models.AutoField(primary_key=True)
    nama_cabang = models.CharField(max_length=100, unique=True)
    deskripsi = models.TextField()
    sejarah = models.TextField()

    def __str__(self):
        return str(self.id) + " | "+self.nama_cabang
    
# class UserManager(BaseUserManager):
#     def _create_user(self, username, email, password, **extra_fields):
#         """
#         membuat user dan menyimpan user dengan memberikan username, email, dan password
#         """
#         if not username:
#             raise ValueError(
#                 _("The given username must be set")
#             )
        
#         email = self.normalize_email(email)
#         GlobalUserModel = apps.get_model(
#             self.model._meta.app_label,
#             self.model._meta.object_name
#         )
#         username = GlobalUserModel.normalize_username(username)
#         user = self.model(
#             username=username,
#             email=email,
#             **extra_fields
#         )
#         user.password = make_password(password)
#         user.save(using=self._db)
#         return user

#     def create_user(self, username, email=None, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(
#             username, email, password, **extra_fields
#         )
    
#     def create_superuser(self, username, email=None, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get("is_staff") is not True:
#             raise ValueError("Superuser must have is_staff=True.")
#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser must have is_superuser=True.")
        
#         return self._create_user(
#             username, email, password, **extra_fields
#         )
    
# class User(AbstractBaseUser, PermissionsMixin):
#     username_validator = UnicodeUsernameValidator()
#     username = models.CharField(
#         max_length=10,
#         unique=True,
#         verbose_name=_("username"),
#         help_text=_(
#             'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
#         ),
#         validators=[username_validator],
#         error_messages={
#             "unique": _("A user with that username already exists.")
#         }
#     )
#     email = models.EmailField(
#         _("email address"),
#         blank=True
#     )
#     full_name = models.CharField(
#         _('Full Name'),
#         max_length=255
#     )
#     phone_number = models.CharField(
#         _('Phone number'),
#         max_length=15
#     )
#     is_staff = models.BooleanField(
#         _('Staff status'),
#         default=False,
#         help_text=_("Designates whether the user can log into this admin site."),
#     )
#     is_active = models.BooleanField(
#         _('active'),
#         default=True,
#         help_text=_(
#             "Designates whether this user should be treated as active. "
#             "Unselect this instead of deleting accounts."
#         )
#     )
#     date_joined = models.DateTimeField(
#         _("date joined"),
#         default=timezone.now
#     )

#     objects = UserManager()

#     EMAIL_FIELD = "email"
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = [
#         'fullname'
#     ]

#     class Meta:
#         verbose_name = _('user')
#         verbose_name_plural = _('users')

#     def clean(self):
#         super().clean()
#         self.email = self.__class__.objects.normalize_email(
#             self.email
#         )
    
#     def email_user(self, subject, message, from_email=None, **kwargs):
#         """send email to this user"""
#         send_mail(subject, message, from_email, [self.email], **kwargs)

#     def __str__(self):
#         return self.full_name