import re
from .models import UserNamesList

def extract_username_and_assignment(file_name):

    # Remove the ".zip" extension from the file name
    file_name = file_name.replace(".zip", "")

    if "_" in file_name:
        username, assignment_number = file_name.split("_")
        
        # Validate assignment number
        if not re.match(r"^\d{2}$", assignment_number):
            assignment_number = None
    else:
        username = file_name
        assignment_number = None

    # Validate username
    if not re.match(r"^\w+$", username):
        None,None

    return username,assignment_number

def check_username_exists(username):
    exists = UserNamesList.objects.filter(user_name=username).exists()
    return exists
