import uuid

from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User

def upload_to(self, filename):
    return '/'.join(['uploads', str(self.id), filename])

# Create your models here.
class Dataset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=upload_to, null=True, blank=False)

    created_by = models.ForeignKey(User, null=True, blank=False, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)

    @property
    def is_expired(self):
        return self.validity < timezone.now()
    
    @property
    def validity(self):
        return self.created_on + timedelta(days=1)

