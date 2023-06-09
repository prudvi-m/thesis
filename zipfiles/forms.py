from django import forms
from .models import Fileslist


class ZipfileForm(forms.ModelForm):
  class Meta:
    model = Fileslist
    fields = ['id_number', 'user_name', 'db_name', 'email', 'is_build_succeeded', 'dotnet_version']
    labels = {
      'id_number': 'Id Number',
      'user_name': 'User Name',
      'db_name': 'Database Name',
      'email': 'Email',
      'is_build_succeeded': 'Is Build Succeeded',
      'dotnet_version': 'Dotner version'
    }
    widgets = {
      'id_number': forms.NumberInput(attrs={'class': 'form-control'}),
      'user_name': forms.TextInput(attrs={'class': 'form-control'}),
      'db_name': forms.TextInput(attrs={'class': 'form-control'}),
      'email': forms.EmailInput(attrs={'class': 'form-control'}),
      'is_build_succeeded': forms.TextInput(attrs={'class': 'form-control'}),
      'dotnet_version': forms.NumberInput(attrs={'class': 'form-control'}),
    }
