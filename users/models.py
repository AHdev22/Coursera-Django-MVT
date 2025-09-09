from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from .utils import generate_otp

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.conf import settings
from .utils import generate_otp

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', default='profiles/profile_login.png')
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    code_created_at = models.DateTimeField(blank=True, null=True)
    code_attempts = models.IntegerField(default=0)

    def generate_verification_code(self):
        self.verification_code = generate_otp()
        self.code_created_at = timezone.now()
        self.code_attempts = 0  # reset attempts
        self.save()
        return self.verification_code

    def code_is_valid(self):
        if not self.verification_code or not self.code_created_at:
            return False
        return timezone.now() < self.code_created_at + datetime.timedelta(
            minutes=settings.OTP_VALIDITY_MINUTES
        )

    def can_attempt(self):
        return self.code_attempts < 3

