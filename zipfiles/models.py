from django.db import models


# Create your models here.
class Fileslist(models.Model):
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

class myuploadfile(models.Model):
    f_name = models.CharField(max_length=255)
    myfiles = models.FileField(upload_to="")

    def __str__(self):
        return self.f_name
