from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.utils.http import urlsafe_base64_encode


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=200, null=True, validators=[RegexValidator(r'^\d+$', message='Phone number must be numeric')])
    cnic_no = models.CharField(max_length=200, default="XXXXX-XXXXXXX-X", null=True)
    next_of_kin = models.CharField(max_length=200, null=True)
    next_of_kin_phone = models.IntegerField(null=True)
    datetime = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_uidb64(self):
        """
        Generate uidb64 against user's email address
        """
        link = f"earn-nest$$/{urlsafe_base64_encode(self.email.encode())}"
        return link

    def __str__(self):
        return self.email
    

class UserDashboard(models.Model):
    user = models.ForeignKey('users.CustomUser', related_name='user_dashboard', on_delete=models.CASCADE)
    total_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profit_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profit_chart = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    referral_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profit_share = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    withdraw = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fund = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.user}'


class Deposit(models.Model):

    class Status(models.IntegerChoices):
        PENDING = 1, _("Pending")
        APPROVED = 2, _("Approved")

    user = models.ForeignKey('users.CustomUser', related_name='deposit', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deposit_date = models.DateField(null=True, blank=True, auto_now_add=True)
    payment_proof = models.ImageField(upload_to='deposit_images/')
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)
 
    def __str__(self):
        return f'{self.user}'     