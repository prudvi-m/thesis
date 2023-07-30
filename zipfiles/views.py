from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import File_Results, UserNamesList
from .forms import FileForm, UserNamesListForm
from .util import extract_username_and_assignment, get_user_name, get_file_result, get_file_size, apply_script_and_update_db
from django.db.models import Count
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
import os
from .tasks import automate_zipfile

# Create your views here.

def send_files(request):
    if request.method == "POST" :
      myfile = request.FILES.getlist("uploadfoles")
      failed_files = []
      for f in myfile:
          user_name, assignment_number = extract_username_and_assignment(f.name)

          if not user_name or not assignment_number:
            failed_files.append(f.name)
            continue

          username_instance = get_user_name(user_name)
          # Check the user name existance in the db from the table UserNamesList username
          if not username_instance:
            failed_files.append(f.name)
            continue
          fileSize = get_file_size(f.size)
          existed = get_file_result(user_name,assignment_number)
          if not existed:
            File_Results(f_name=f.name,myfiles=f,f_size=fileSize, user_name = username_instance, assignment_number = assignment_number).save()
          else:
             data = {
                "f_name" : f.name,
                "f_size" : fileSize,
                "myfiles" : f,
                "user_name" : username_instance,
                "db_name" : None,
                "db_type" : None,
                "is_build_succeeded" : None,
                "dotnet_version" : None,
                "assignment_number" : assignment_number,
                "folder_name" : None,
                "instruction_passed" : None,
              }
             existed.update_attributes(data)
      if failed_files:
          # Store the failed_files in the session
          request.session['failed_files'] = failed_files
          messages.error(request, 'Some files failed to upload.')
      return HttpResponseRedirect(reverse('index'))

def automate(request, id):
  if request.method == 'GET':
    # Retrieve the File_Results instance
    apply_script_and_update_db(id)
    return HttpResponseRedirect(reverse('index'))
  
def automate_all(request):
    if request.method == 'GET':
        zipfiles = File_Results.objects.all()

        # Trigger the Celery task for each zipfile
        for zipfile in zipfiles:
            automate_zipfile.delay(zipfile.id)
    return HttpResponseRedirect(reverse('index'))


#region Files Crud
def index(request):
  # Retrieve failed_files from the session if available
  failed_files = request.session.pop('failed_files', [])
  file_results = File_Results.objects.all()
  return render(request, 'zipfiles/index.html', {
    'zipfiles': file_results,
    'failed_files': failed_files
  })

def view_info(request, id):
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
  if not request.method == 'POST':
    return render(request, 'zipfiles/edit.html', {
      'id': id
    })
  zipfile = File_Results.objects.get(pk=id)
  myfile = request.FILES.getlist("uploadfoles")
  failed_files = []
  for f in myfile:
      user_name, assignment_number = extract_username_and_assignment(f.name)

      if not user_name or not assignment_number:
        failed_files.append(f.name)
        continue

      username_instance = get_user_name(user_name)
      # Check the user name existance in the db from the table UserNamesList username
      if not username_instance:
        failed_files.append(f.name)
        continue

      # user_name, assignment_number = extract_username_and_assignment(f.name)
      fileSize = fileSize = get_file_size(f.size)
      data = {
        "f_name" : f.name,
        "f_size" : fileSize,
        "myfiles" : f,
        "user_name" : zipfile.user_name,
        "db_name" : None,
        "db_type" : None,
        "is_build_succeeded" : None,
        "dotnet_version" : None,
        "assignment_number" : assignment_number,
        "folder_name" : None,
        "instruction_passed" : None,
      }
      zipfile.update_attributes(data)

  if failed_files:
      # Store the failed_files in the session
      request.session['failed_files'] = failed_files
      messages.error(request, 'Some files failed to upload.')

  return HttpResponseRedirect(reverse('index'))
        

  
def dashboard(request):
   # Retrieve data from the File_Results model
    dotnet_data = File_Results.objects.filter(dotnet_version__isnull=False)
    database_data = File_Results.objects.filter(db_name__isnull=False)
    build_data = File_Results.objects.filter(is_build_succeeded__isnull=False)

    # Count the occurrences of each DotNet version
    dotnet_counts = dotnet_data.values('dotnet_version').annotate(count=Count('dotnet_version'))
    dotnet_labels = [item['dotnet_version'] for item in dotnet_counts]
    dotnet_values = [item['count'] for item in dotnet_counts]

    # Count the occurrences of each database type
    database_counts = database_data.values('db_type').annotate(count=Count('db_type'))
    database_labels = [item['db_type'] for item in database_counts]
    database_values = [item['count'] for item in database_counts]

    # Count the occurrences of build statuses
    build_failed_count = build_data.filter(is_build_succeeded='False').count()
    build_succeeded_count = build_data.filter(is_build_succeeded='True').count()

    # Prepare the data for the template
    dotnet_chart_data = {
        'labels': dotnet_labels,
        'datasets': [{
            'data': dotnet_values,
            'backgroundColor': ['#007bff', '#dc3545', '#ffc107'],
        }]
    }

    database_chart_data = {
        'labels': database_labels,
        'datasets': [{
            'data': database_values,
            'backgroundColor': ['#28a745', '#ffc107'],
        }]
    }

    build_chart_data = {
        'labels': ['Build Failed', 'Build Succeeded'],
        'datasets': [{
            'data': [build_failed_count, build_succeeded_count],
            'backgroundColor': ['#dc3545', '#28a745'],
        }]
    }

    dotnet_list_group_data = {item['dotnet_version']: item['count'] for item in dotnet_counts}

    database_list_group_data = {item['db_type']: item['count'] for item in database_counts}

    build_list_group_data = {'Build Failed': build_failed_count, 'Build Succeeded': build_succeeded_count}

    if build_failed_count == 0 and build_succeeded_count == 0:
       
       build_chart_data = {
          'labels': [],
          'datasets': [{
              'data': [],
              'backgroundColor': ['#dc3545', '#28a745'],
          }]
        }
       build_list_group_data = {}
       

    # Pass the data to the template
    context = {
        'dotnet_chart_data': dotnet_chart_data,
        'database_chart_data': database_chart_data,
        'build_chart_data': build_chart_data,
        'dotnet_list_group_data' : dotnet_list_group_data,
        'database_list_group_data': database_list_group_data,
        'build_list_group_data' : build_list_group_data
    }


    print("\n\nContext:\n\n*****\n\n", context,"\n\n***** \n\n")

    return render(request, 'zipfiles/dashboard.html', context)


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


def report(request):
    assignment_numbers = File_Results.objects.values_list('assignment_number', flat=True).distinct()
    database_types = File_Results.objects.values_list('db_type', flat=True).distinct()
    
    assignment_number = ''
    status = ''
    db_type = ''
    submission = 'Submitted'
    missing_user_names = []
    users = []
    if request.method == 'POST':
      submission = request.POST.get('submission')
      assignment_number = request.POST.get('assignment_number')
      status = request.POST.get('status')
      db_type = request.POST.get('db_type')
      
      
      filters = {}

      # Check if assignment_number is a valid integer
      if assignment_number.isdigit():
        filters['assignment_number'] = int(assignment_number)
      
      if submission != 'Not Submitted':
      
                
        # Apply filter based on status
        if status == 'Failed':
            filters['is_build_succeeded'] = 'False'
        elif status == 'Success':
            filters['is_build_succeeded'] = 'True'
        
        # Apply filter based on db_type if it is not empty
        if db_type and db_type != "":
            filters['db_type'] = db_type
        
        users = File_Results.objects.filter(**filters)

      else:
        file_result_user_names = File_Results.objects.filter(**filters).values_list('user_name__user_name', flat=True).distinct()
        user_names_list = UserNamesList.objects.values_list('user_name', flat=True).distinct()
        missing_user_names = set(user_names_list) - set(file_result_user_names)

      
    else:
        users = File_Results.objects.all()
    context = {
      'users': users,
      'assignment_numbers': assignment_numbers,
      'database_types': database_types,
      'selected_assignment': '' if not assignment_number.isdigit() else int(assignment_number),
      'selected_status': status,
      'selected_db_type': db_type,
      'selected_submission': submission,
      'missing_user_names' : missing_user_names
    }
    
    return render(request, 'zipfiles/report.html', context)

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


def download_file(request, id):
    # Retrieve the File_Results instance
    zipfile = get_object_or_404(File_Results, pk=id)
    
    # Construct the file path
    file_path = os.path.join(settings.MEDIA_ROOT, str(zipfile.f_name))
    
    # Check if the file exists
    if os.path.exists(file_path):
        # Open the file in binary mode for reading
        with open(file_path, 'rb') as file:
            # Create the HTTP response with the file as the content
            response = HttpResponse(file.read(), content_type='application/zip')
            # Set the Content-Disposition header to force download
            response['Content-Disposition'] = f'attachment; filename="{zipfile.f_name}"'
            return response
    else:
        # Return a 404 Not Found response if the file does not exist
        return HttpResponse(status=404)

def delete_all(request):
  if request.method == 'GET':
      # Delete all File_Results instances
      File_Results.objects.all().delete()
      
      return redirect('index')