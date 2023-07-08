import re

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
        return {
            "username": None,
            "assignment": None
        }

    return {
        "username": username,
        "assignment": assignment_number
    }
        

    

file_names = ["jkl.zip", "mno_3.zip", "pqr", "xyz_26.zip","se@r"]

for i in file_names:
    print(extract_username_assignment(i))



