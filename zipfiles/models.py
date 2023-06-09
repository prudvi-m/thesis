from django.db import models


# Create your models here.
class Zipfile(models.Model):
  id_number = models.PositiveIntegerField()
  user_name = models.CharField(max_length=50)
  db_name = models.CharField(max_length=50)
  email = models.EmailField(max_length=100)
  is_build_succeeded = models.CharField(max_length=50)
  dotnet_version = models.FloatField()

  def __str__(self):
    return f'Zipfile: {self.user_name} {self.db_name}'

class myuploadfile(models.Model):
    f_name = models.CharField(max_length=255)
    myfiles = models.FileField(upload_to="")

    def __str__(self):
        return self.f_name
