import re
from .models import UserNamesList, File_Results
from django.shortcuts import get_object_or_404
from automate import apply_automate_script

def extract_username_and_assignment(file_name):

    # Remove the ".zip" extension from the file name
    file_name = file_name.replace(".zip", "")

    if "_" in file_name:
        username, assignment_number = file_name.split("_")
        
        # Validate assignment number
        if not re.match(r"^\d{1,2}$", assignment_number):
            assignment_number = None
    else:
        username = file_name
        assignment_number = None
    # Validate username
    if not re.match(r"^\w+$", username):
        None,None
    return username,assignment_number

def get_user_name(user_name):
    try:
        existed = UserNamesList.objects.get(user_name=user_name)
        return existed
    except UserNamesList.DoesNotExist:
        return None

def apply_script_and_update_db(id):

    zipfile = get_object_or_404(File_Results, pk=id)
    data = apply_automate_script(zipfile.f_name)
    
    # Update the attributes based on the data
    zipfile.db_name = data.get('db_name')
    zipfile.db_type = data.get('db_type')
    zipfile.dotnet_version = data.get('version')
    zipfile.folder_name = data.get('folder_name')
    zipfile.is_build_succeeded = data.get('build')
    zipfile.error_details = data.get('error_details')

    # Save the changes
    zipfile.save()



def get_file_result(user_name, assignment_number):
    try:
        file_result = File_Results.objects.get(user_name=user_name, assignment_number=assignment_number)
        return file_result
    except File_Results.DoesNotExist:
        return None


def get_file_size(size):
    fileSize = float(format(size / 1024, f".1f"))
    if fileSize >= 1024:
        return f'{format((fileSize / 1024), f".1f")}MB'
    return f'{fileSize}KB'
