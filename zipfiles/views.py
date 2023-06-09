from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Zipfile, myuploadfile
from .forms import ZipfileForm


# Create your views here.
def index(request):
  return render(request, 'zipfiles/index.html', {
    'zipfiles': Zipfile.objects.all()
  })


def view_student(request, id):
  return HttpResponseRedirect(reverse('index'))


def add(request):
  if request.method == 'POST':
    form = ZipfileForm(request.POST)
    if form.is_valid():
      new_id_number = form.cleaned_data['id_number']
      new_user_name = form.cleaned_data['user_name']
      new_db_name = form.cleaned_data['db_name']
      new_email = form.cleaned_data['email']
      new_is_build_succeeded = form.cleaned_data['is_build_succeeded']
      new_dotnet_version = form.cleaned_data['dotnet_version']

      new_student = Zipfile(
        id_number=new_id_number,
        user_name=new_user_name,
        db_name=new_db_name,
        email=new_email,
        is_build_succeeded=new_is_build_succeeded,
        dotnet_version=new_dotnet_version
      )
      new_student.save()
      return render(request, 'zipfiles/add.html', {
        'form': ZipfileForm(),
        'success': True
      })
  else:
    form = ZipfileForm()
  return render(request, 'zipfiles/add.html', {
    'form': ZipfileForm()
  })


def edit(request, id):
  if request.method == 'POST':
    zipfile = Zipfile.objects.get(pk=id)
    form = ZipfileForm(request.POST, instance=zipfile)
    if form.is_valid():
      form.save()
      return render(request, 'zipfiles/edit.html', {
        'form': form,
        'success': True
      })
  else:
    zipfile = Zipfile.objects.get(pk=id)
    form = ZipfileForm(instance=zipfile)
  return render(request, 'zipfiles/edit.html', {
    'form': form
  })


def delete(request, id):
  if request.method == 'POST':
    zipfile = Zipfile.objects.get(pk=id)
    zipfile.delete()
  return HttpResponseRedirect(reverse('index'))

# Create your views here.
def files(request):
    return render(request, 'zipfiles/files.html', {
    'zipfiles': myuploadfile.objects.all()
  })

def send_files(request):
    if request.method == "POST" :
        myfile = request.FILES.getlist("uploadfoles")
        for f in myfile:
            myuploadfile(f_name=f.name,myfiles=f).save()
        return HttpResponseRedirect(reverse('files'))