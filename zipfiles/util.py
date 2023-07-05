import re

def extract_username_and_assignment(file_name):
    pattern = r'^(.*)_([0-9]+)\.zip$'
    match = re.match(pattern, file_name)
    if match:
        username = match.group(1)
        assignment = int(match.group(2))
        return username, assignment
    else:
        return None,None
