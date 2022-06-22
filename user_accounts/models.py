from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from .managers import CustomUserManager


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=200, unique=True)
    profile_img = models.ImageField(
        upload_to='user-profile-img/',
        default='user-default-img/user_default_img.png'
    )
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_profile_img(self):
        """
        :return: Profile Image Url
        """
        try:
            img = self.profile_img.url
        except FileExistsError:
            img = ''
        return img

    def has_perm(self, perm, obj=None):
        return self.is_admin or self.is_staff

    def has_module_perms(self, app_label):
        return self.is_admin or self.is_staff
