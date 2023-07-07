#region packages
import os
import subprocess
import zipfile
import re
import json
import shutil
import xml.etree.ElementTree as ET

#endregion

#region Global Varaibles
current_path = os.getcwd()
extract_path = f"{current_path}/{'media'}"
#endregion

#region 1.Extract zip file
def extract_zip(zip_file):
    extracted_folder = None
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        first_item = zip_ref.infolist()[0]
        extracted_folder = os.path.dirname(first_item.filename)
        zip_ref.extractall(extract_path)
    delete_mac_extract_folders()
    return extracted_folder

def delete_mac_extract_folders():
    for entry in os.listdir(extract_path):
        folder_path = os.path.join(extract_path, entry)
        if os.path.isdir(folder_path) and entry == "__MACOSX":
            # Use shutil.rmtree() to delete the entire folder and its contents
            shutil.rmtree(folder_path)


def delete_extracted_folders():
    print(f"\n* extract_path : {extract_path}")
    for item in os.listdir(extract_path):
        item_path = os.path.join(extract_path, item)
        # Check if the item is a folder and its name matches any zip file name
        if os.path.isdir(item_path) and item + ".zip" in os.listdir(extract_path):
            print("Folder to be deleted:", item)
            # Delete the folder
            shutil.rmtree(item_path)
#endregion

#region 2.Build
def execute_dotnet_build(project_path):
    cmd = ['dotnet','build']
    cwd = extract_path + f'/{project_path}/'
    print(f"\ncwd : {cwd}")
    try:
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE,cwd=cwd).communicate()[0]
    except Exception as error:
        error_type = type(error).__name__  # Get the name of the error type
        error_message = str(error)  # Get the error message
        # Print the error information
        print("Error Type:", error_type)
        print("Error Message:", error_message)
        return {"build" : False, "details" : 'Failed'}

    content = str(output).replace('b\'','').replace('\'','').replace('\\n','\n')
    # Save the build results to the given file
    write_results(content)
    print(f"\n\n{content}\n\n")
    if content and re.search('Build succeeded.',content):
        return {"build" : True, "details" : ""}
    
    details = get_error_details(content)
    return {"build" : False, "details" : details}

def get_error_details(build_output):

    error_pattern = r"([^/()]+\.cs)\((\d+),\d+\): error (CS\d+): (.+?) \[.+?\]"

    # Initialize error count and unique error messages
    error_count = 0
    unique_errors = set()
    error_details = []

    # Extract errors and update error count
    error_matches = re.findall(error_pattern, build_output)

    # Process error matches
    for match in error_matches:
        filename, line_number, error_code, error_message = match
        error = f"{filename} - {line_number} - {error_code} - {error_message}"
        if error not in unique_errors:
            error_details.append(
                f"\nFile: {filename}\nLine number: {line_number}\nMessage: {error_message}\nError Code: {error_code}\n\n"
            )
            unique_errors.add(error)
            error_count += 1

    # Check if "Build FAILED" line is present
    if "Build FAILED" in build_output:
        error_details.append("Build FAILED.\n")

    error_details.append(f"Total Errors: {error_count}\n")

    # Create a single multiline string
    detail_multiline_string = "".join(error_details)
    print(detail_multiline_string)
    return detail_multiline_string

#endregion

#region 3.Write Build Result
def write_results(content, file_name = 'result_file.txt'):
    # Save the build results to the given file
    with open(file_name, 'a') as file:
        file.write(content)

#endregion

#region 4.Database type & name

def is_appsettings_json_existed(project_path):
    appsettings_file_path = os.path.join(project_path, "appsettings.json")
    return os.path.isfile(appsettings_file_path)

def read_connection_string(appsettings_file):
    with open(appsettings_file, 'r') as file:
        appsettings = json.load(file)
        connection_strings = appsettings.get('ConnectionStrings', {})
        return connection_strings

def get_database(project_path):
    # os.chdir(project_path)
    # os.chdir(current_path)
    database = {'db_name' : '', 'db_type' : '' }
    settings_path = f"{extract_path}/{project_path}"
    is_file_existed = is_appsettings_json_existed(settings_path)
    if is_file_existed:
        connection_string = read_connection_string(f"{settings_path}/appsettings.json")
        for key, value in connection_string.items():
            # sqlite
            if isinstance(value, str) and '.sqlite' in value:
                database = { 
                                'db_name' : get_database_name(connection_string[key], r"Filename=(.*?)\.sqlite"),
                                'db_type' : 'Sqlite'
                            }
                
                # print(f" - {key}: {value}")
            # sqlserver
            else:
                database = { 
                                'db_name' : get_database_name(connection_string[key]),
                                'db_type' : 'SqlServer'
                            }
    return database
        


def get_database_name(connection_string, pattern = r"Database=(.*?);"):
    match = re.search(pattern, connection_string)
    if match:
        return match.group(1)
    else:
        return None

#endregion

#region 5.Dotnet Version 
def get_version(project_path):
    # Read and parse the .csproj file
    print(f"\nversion path : {project_path}/{project_path}.csproj")
    tree = ET.parse(f"{extract_path}/{project_path}/{project_path}.csproj")
    root = tree.getroot()
    dotnet_version = ''
    # Find the TargetFramework element
    target_framework_element = root.find("./PropertyGroup/TargetFramework")
    if target_framework_element is not None:
        # Extract the .NET version from the TargetFramework element
        dotnet_version = target_framework_element.text
        # print("The .NET version is:", dotnet_version)
    return dotnet_version

#endregion

#region 6.Apply Script

def apply_automate_script(zip_file):
    zip_file = f"{extract_path}/{zip_file}"
    delete_extracted_folders()
    folder_name = extract_zip(zip_file)
    return get_file_data(folder_name)

def get_file_data(folder_name):
    result = {}
    build_details = execute_dotnet_build(folder_name)
    database = get_database(folder_name)
    version = get_version(folder_name)
    result = { 
        "folder_name" : folder_name,
        "build" : build_details["build"],
        "error_details" : build_details["details"],
        "db_name" : database["db_name"],
        "db_type" : database["db_type"],
        "version" : version
    }
    print("\n******************************************\n")
    print(result,"\n\n")
    return result

#endregion

if __name__ == "__main__":
    os.chdir(extract_path)
    print()
    get_file_data('MovieList')
    #Sample
    # apply_automate_script('anusha.zip')

