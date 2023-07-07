from django import forms
from .models import File_Results, UserNamesList
from django.core.validators import MinLengthValidator


class FileForm(forms.ModelForm):
  class Meta:
    model = File_Results

    fields = ['id_number','f_name','f_size','myfiles','user_name'
            ,'db_name','db_type','is_build_succeeded','dotnet_version'
            ,'error_details','assignment_number','folder_name','instruction_passed',]
    labels = {
      'id_number' : 'id_number',
      'f_name' : 'f_name',
      'f_size' : 'f_size',
      'myfiles' : 'myfiles',
      'user_name' : 'user_name',
      'db_name' : 'db_name',
      'db_type' : 'db_type',
      'is_build_succeeded' : 'is_build_succeeded',
      'dotnet_version' : 'dotnet_version',
      'error_details' : 'error_details',
      'assignment_number' : 'assignment_number',
      'folder_name' : 'folder_name',
      'instruction_passed' : 'instruction_passed',
    }
    widgets = {
      'id_number': forms.NumberInput(attrs={'class': 'form-control'}),
      'user_name': forms.TextInput(attrs={'class': 'form-control'}),
      'db_name': forms.TextInput(attrs={'class': 'form-control'}),
      'is_build_succeeded': forms.TextInput(attrs={'class': 'form-control'}),
      'dotnet_version': forms.NumberInput(attrs={'class': 'form-control'}),
    }

class UserNamesListForm(forms.ModelForm):
    class Meta:
        model = UserNamesList
        fields = ['user_name', 'enable']

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        if len(user_name) < 3:
            raise forms.ValidationError('Username must have at least 3 characters.')
        return user_name

    def clean(self):
        cleaned_data = super().clean()
        user_name = cleaned_data.get('user_name')

        if user_name:
            existing_user = UserNamesList.objects.filter(user_name=user_name).exists()
            if existing_user:
                self.add_error('user_name', 'Username already exists. Please choose a different username.')

        return cleaned_data