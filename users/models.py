import uuid
from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from django.dispatch import receiver
from base.emails import send_account_activation_email
from django.db.models.signals import post_save

# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name='',last_name='',is_active=False, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            is_active=is_active

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            is_active=True,
        )
        user.is_admin = True
        user.is_email_verified=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser,BaseModel):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    first_name=models.CharField(max_length=100,default='')
    last_name=models.CharField(max_length=100,default='')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_email_verified=models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
    


@receiver(post_save, sender=User)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            email_token = instance.uid
            email = instance.email
            send_account_activation_email(email, email_token)
    except Exception as e:
        print(e)