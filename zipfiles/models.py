from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.validators import MinLengthValidator
from django.utils import timezone
import os

# Create your models here.
class File_Results(models.Model):
  id_number = models.PositiveIntegerField(null=True)
  f_name = models.CharField(max_length=255,null=True)
  f_size = models.CharField(max_length=50,null=True)
  myfiles = models.FileField(upload_to="")
  user_name = models.CharField(max_length=50,null=True)
  db_name = models.CharField(max_length=50,null=True)
  email = models.EmailField(max_length=100,null=True)
  is_build_succeeded = models.CharField(max_length=50,null=True)
  dotnet_version = models.CharField(max_length=20,null=True)
  
  def __str__(self):
    return f'files: {self.user_name} {self.db_name}'
  
@receiver(pre_delete, sender=File_Results)
def delete_file_on_delete(sender, instance, **kwargs):
    # Get the file path
    file_path = instance.myfiles.path
    
    # Check if the file exists and delete it
    if os.path.exists(file_path):
        os.remove(file_path)

pre_delete.connect(delete_file_on_delete, sender=File_Results)


class myuploadfile(models.Model):
    f_name = models.CharField(max_length=255)
    myfiles = models.FileField(upload_to="")

    def __str__(self):
        return self.f_name

class UserNamesList(models.Model):
    user_name = models.CharField(
        max_length=255,
        unique=True,
        validators=[
            MinLengthValidator(3, message='Username must have at least 3 characters.'),
        ]
    )
    email = models.EmailField()
    enable = models.BooleanField(default=True)
    updated_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Prefix the user_name to the email for @student.govst.edu
        self.email = f'{self.user_name}@student.govst.edu'
        super().save(*args, **kwargs)
    class Meta:
        verbose_name_plural = 'UserNamesList'
