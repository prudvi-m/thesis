import os
import subprocess
import zipfile
import re
import json5
import shutil
import xml.etree.ElementTree as ET

#region Global Varaibles
c_path = os.getcwd()
e_path = f"{c_path}/{'media'}"
#endregion


def extract_zip(zip_file):
    extracted_folder = None
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        first_item = zip_ref.infolist()[0]
        extracted_folder = os.path.dirname(first_item.filename)
        zip_ref.extractall(e_path)
    delete_mac_extract_folders()
    return extracted_folder

def delete_mac_extract_folders():
    for entry in os.listdir(e_path):
        folder_path = os.path.join(e_path, entry)
        if os.path.isdir(folder_path) and entry == "__MACOSX":
            shutil.rmtree(folder_path)


def delete_extracted_folders():
    print(f"\n* e_path : {e_path}")
    for item in os.listdir(e_path):
        item_path = os.path.join(e_path, item)
        
        if os.path.isdir(item_path) and item + ".zip" in os.listdir(e_path):
            print("Folder to be deleted:", item)
            shutil.rmtree(item_path)



def execute_dotnet_build(project_path):
    cmd = ['dotnet','build']
    cwd = e_path + f'/{project_path}/'
    print(f"\ncwd : {cwd}")
    try:
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE,cwd=cwd).communicate()[0]
    except Exception as err:
        err_type = type(err).__name__
        err_message = str(err)
        print("err Type:", err_type)
        print("err Message:", err_message)
        return {"build" : False, "details" : 'Failed'}

    content = str(output).replace('b\'','').replace('\'','').replace('\\n','\n')
    write_results(content)
    print(f"\n\n{content}\n\n")
    if content and re.search('Build succeeded.',content):
        return {"build" : True, "details" : ""}
    
    details = get_err_details(content)
    return {"build" : False, "details" : details}

def get_err_details(build_output):

    err_pattern = r"([^/()]+\.cs)\((\d+),\d+\): error (CS\d+): (.+?) \[.+?\]"

    err_count = 0
    unique_errors = set()
    err_details = []


    err_matches = re.findall(err_pattern, build_output)


    for match in err_matches:
        filename, line_number, err_code, err_message = match
        error = f"{filename} - {line_number} - {err_code} - {err_message}"
        if error not in unique_errors:
            err_details.append(
                f"\nFile: {filename}\nLine number: {line_number}\nMessage: {err_message}\nError Code: {err_code}\n\n"
            )
            unique_errors.add(error)
            err_count += 1


    if "Build FAILED" in build_output:
        err_details.append("Build FAILED.\n")

    err_details.append(f"Total Errors: {err_count}\n")


    detail_multiline_string = "".join(err_details)
    print(detail_multiline_string)
    return detail_multiline_string




def write_results(content, file_name = 'result_file.txt'):

    with open(file_name, 'a') as file:
        file.write(content)





def is_appsettings_json_existed(project_path):
    appsettings_file_path = os.path.join(project_path, "appsettings.json")
    return os.path.isfile(appsettings_file_path)

def read_connection_string(appsettings_file):
    try:
        with open(appsettings_file, 'r') as file:
            appsettings = json5.load(file)
            connection_strings = appsettings.get('ConnectionStrings', {})
            return connection_strings
    except FileNotFoundError:
        print(f"Error: File '{appsettings_file}' not found.")
    except json5.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON file '{appsettings_file}': {e}")
    except Exception as e:
        print(f"Error: {e}")
    return None


def get_database(project_path):
    database = {'db_name' : '', 'db_type' : '' }
    settings_path = f"{e_path}/{project_path}"
    is_file_existed = is_appsettings_json_existed(settings_path)
    if is_file_existed:
        connection_string = read_connection_string(f"{settings_path}/appsettings.json")
        if connection_string:
            for key, value in connection_string.items():

                if isinstance(value, str) and '.sqlite' in value:
                    database = { 
                                    'db_name' : get_database_name(connection_string[key], r"Filename=(.*?)\.sqlite"),
                                    'db_type' : 'Sqlite'
                                }
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


def get_version(project_path):
    csproj_files = []
    for root, dirs, files in os.walk(f"{e_path}/{project_path}"):
        for file in files:
            if file.endswith(".csproj"):
                csproj_files.append(os.path.join(root, file))

    dt_version = ''
    for csproj_file in csproj_files:

        tree = ET.parse(csproj_file)
        root = tree.getroot()

        # Find the TargetFramework element
        target_el = root.find("./PropertyGroup/TargetFramework")
        if target_el is not None:
            dt_version = target_el.text
            print("The .NET version is:", dt_version)
            break

    return dt_version

def apply_automate_script(zip_file):
    zip_file = f"{e_path}/{zip_file}"
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



if __name__ == "__main__":
    os.chdir(e_path)
    print()
    # get_file_data('MovieList')
    # apply_automate_script('bond_2.zip')

