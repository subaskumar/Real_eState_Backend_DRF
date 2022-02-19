from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email,name, password=None, is_staff=False, is_active=True, is_admin=False):
        if not email:
            raise ValueError('users must have a phone number')

        if not password:
            raise ValueError('user must have a password')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active
        user.save(using=self._db) # or user.save()
        return user

    def create_staffuser(self, email,name, password=None):
        user = self.create_user(email,name, password=password,is_staff=True,)
        return user

    def create_superuser(self, email,name, password=None):
        user = self.create_user(email,name, password=password,is_staff=True,is_admin=True,)
        return user


class UserAccount(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    name        = models.CharField(max_length = 20, blank = True, null = True)
    active      = models.BooleanField(default=True)
    staff       = models.BooleanField(default=False)
    admin       = models.BooleanField(default=False)
    timestamp   = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return str(self.email)

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):

        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active