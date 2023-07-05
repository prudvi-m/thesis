import re

def extract_username_and_assignment(file_name):
    pattern = r'^(.*)_([0-9]+)\.zip$'
    match = re.match(pattern, file_name)
    if match:
        username = match.group(1)
        assignment = int(match.group(2))
        return username, assignment
    else:
        raise '',None

# Test the function
file_names = ['Sai_1.zip', 'shiva_1.zip', 'mohan_1.zip']

for file_name in file_names:
    try:
        username, assignment = extract_username_and_assignment(file_name)
        print(f"Username: {username}")
        print(f"assignment: {assignment}")
    except ValueError as e:
        print(f"Invalid file name: {file_name}")
        print(e)
    print()
