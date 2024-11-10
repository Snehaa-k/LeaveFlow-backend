from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser, Group, Permission


# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(max_length=223, null=True)
    email = models.EmailField(max_length=223, unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    password = models.CharField(max_length=223)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=254, null=True)
    groups = models.ManyToManyField(Group, related_name="custom_user_groups")
    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_user_permissions"
    )

    def __str__(self):
        return self.username

    def generate_otp(self):
        otp = get_random_string(length=6, allowed_chars="1234567890")
        # self.otp_expiration = now + timedelta(seconds=60)
        self.otp = otp
        self.save()
        self.otp_expiration = timezone.now() + timedelta(seconds=60)
        self.send_otp_email()

    def is_otp_expired(self):
        now = timezone.now()
        return now > self.otp_expiration

    def send_otp_email(self):
        subject = "Your OTP for Signup"
        message = f"Your OTP is {self.otp}. Enter this code to complete your signup."
        from_email = "worldmagical491@gmail.com"
        to_email = [self.email]
        send_mail(subject, message, from_email, to_email)


class Leaveapplication(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="leave_applications"
    )
    leave_type = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(max_length=334)
    document = models.ImageField(upload_to="media", blank=True, null=True)
    status = models.CharField(max_length=200, default="pending")

    def __str__(self):
        return f"Leave application by {self.user} - {self.status}"


class Userprofile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="media", blank=True, null=True)
