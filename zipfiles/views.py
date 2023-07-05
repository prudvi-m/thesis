import json
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import File_Results, UserNamesList
from .forms import FileForm, UserNamesListForm
from automate import delete_extracted_and_run
from .util import extract_username_and_assignment

# Create your views here.

#region Files Crud
def index(request):
  return render(request, 'zipfiles/index.html', {
    'zipfiles': File_Results.objects.all()
  })

def automate(request):
  result = delete_extracted_and_run()

  # Convert JSON data to a string
  # json_string = json.dumps(result)
  print(json.dumps(result))
  
  files = File_Results.objects.all()
  files_len = len(files)
  result_len = len(result)
  r = min([files_len,result_len])
  for i in range(r):
     
     
  
  return render(request, 'zipfiles/index.html', {
    'zipfiles': File_Results.objects.all()
  })

def view_student(request, id):
  return HttpResponseRedirect(reverse('index'))

def add(request):
  if request.method == 'POST':
    form = FileForm(request.POST)
    if form.is_valid():
      new_id_number = form.cleaned_data['id_number']
      new_user_name = form.cleaned_data['user_name']
      new_db_name = form.cleaned_data['db_name']
      new_email = form.cleaned_data['email']
      new_is_build_succeeded = form.cleaned_data['is_build_succeeded']
      new_dotnet_version = form.cleaned_data['dotnet_version']

      new_file = File_Results(
        id_number=new_id_number,
        user_name=new_user_name,
        db_name=new_db_name,
        email=new_email,
        is_build_succeeded=new_is_build_succeeded,
        dotnet_version=new_dotnet_version
      )
      new_file.save()
      return render(request, 'zipfiles/add.html', {
        'form': FileForm(),
        'success': True
      })
  else:
    form = FileForm()
  return render(request, 'zipfiles/add.html', {
    'form': FileForm()
  })


def edit(request, id):
  if request.method == 'POST':
    zipfile = File_Results.objects.get(pk=id)
    form = FileForm(request.POST, instance=zipfile)
    if form.is_valid():
      form.save()
      return render(request, 'zipfiles/edit.html', {
        'form': form,
        'success': True
      })
  else:
    zipfile = File_Results.objects.get(pk=id)
    form = FileForm(instance=zipfile)
  return render(request, 'zipfiles/edit.html', {
    'form': form
  })


def delete(request, id):
  if request.method == 'POST':
    zipfile = File_Results.objects.get(pk=id)
    zipfile.delete()
  return HttpResponseRedirect(reverse('index'))

# Create your views here.
def files(request):
    return render(request, 'zipfiles/files.html', {
    'zipfiles': File_Results.objects.all()
  })

def send_files(request):
    if request.method == "POST" :
        
        myfile = request.FILES.getlist("uploadfoles")
        for f in myfile:
            user_name, assignment_number = extract_username_and_assignment(f.name)
            fileSize = float(format(f.size / 1024, f".1f"))
            if fileSize >= 1024:
              fileSize = f'{format((fileSize / 1024), f".1f")}MB'
            else:
              fileSize = f'{fileSize}KB'
            File_Results(f_name=f.name,myfiles=f,f_size=fileSize, user_name = user_name, assignment_number = assignment_number).save()
        return HttpResponseRedirect(reverse('index'))

#endregion 

#region CRUD UserNames

def user_create(request):
    if request.method == 'POST':
        form = UserNamesListForm(request.POST)
        if form.is_valid():
            user_names = form.cleaned_data['user_name'].split(',')
            for user_name in user_names:
                UserNamesList.objects.create(user_name=user_name.strip(), email=f'{user_name.strip()}@student.govst.edu')
            # return redirect('zipfiles/user_list')
            return redirect('user_list')

    else:
        form = UserNamesListForm()

    return render(request, 'zipfiles/user_create.html', {'form': form})

def user_list(request):
    users = UserNamesList.objects.all()
    return render(request, 'zipfiles/user_list.html', {'users': users})

def user_update(request, pk):
    user = get_object_or_404(UserNamesList, pk=pk)
    
    if request.method == 'POST':
        form = UserNamesListForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('zipfiles/user_list')
    else:
        form = UserNamesListForm(instance=user)
    
    return render(request, 'zipfiles/user_update.html', {'form': form})

def delete_user(request, pk):
    user = get_object_or_404(UserNamesList, pk=pk)

    if request.method == 'POST':
        user.delete()
        return redirect('user_list')

    return render(request, 'zipfiles/user_delete.html', {'user': user})

#endregion