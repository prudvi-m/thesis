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

#region 1.Zip Handlng
def extract_zip():
    extension = ".zip"

    # *****
    # os.chdir(extract_path) # change directory from working dir to dir with files
    # **** 
    
    for item in os.listdir(extract_path): # loop through items in dir
        if item.endswith(extension): # check for ".zip" extension
            file_name = os.path.abspath(item) # get full path of files

            # Check if the corresponding extracted folder already exists
            extracted_folder = os.path.splitext(file_name)[0]
            if os.path.exists(os.path.join(os.getcwd(), extracted_folder)):
                print(f"Skipping {item} as the folder already exists.\n")
                continue
            
            zip_ref = zipfile.ZipFile(file_name) # create zipfile object
            zip_ref.extractall(extract_path) # extract file to dir
            zip_ref.close() # close file
            # os.remove(file_name) # delete zipped file
    # os.chdir(current_path)

    for entry in os.listdir(extract_path):
        folder_path = os.path.join(extract_path, entry)
        if os.path.isdir(folder_path) and entry == "__MACOSX":
            print("Deleting folder:", '__MACOSX')
            # Use shutil.rmtree() to delete the entire folder and its contents
            shutil.rmtree(folder_path)

def delete_extracted_folders():
    # os.chdir(extract_path)
    c_path = os.getcwd()
    for item in os.listdir(c_path):
        item_path = os.path.join(c_path, item)
        # Check if the item is a folder and its name matches any zip file name
        if os.path.isdir(item_path) and item + ".zip" in os.listdir(c_path):
            print("Folder to be deleted:", item)
            # Delete the folder
            shutil.rmtree(item_path)
    # os.chdir(current_path)


#endregion

#region 2.Build

def execute_dotnet_build(project_path):
    cmd = ['dotnet','build']
    cwd = os.getcwd() + f'/{project_path}/'
    try:
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE,cwd=cwd).communicate()[0]
    except Exception as error:
        error_type = type(error).__name__  # Get the name of the error type
        error_message = str(error)  # Get the error message
        # Print the error information
        print("Error Type:", error_type)
        print("Error Message:", error_message)
        return

    content = str(output).replace('b\'','').replace('\'','').replace('\\n','\n')
    # Save the build results to the given file
    write_results(content)
    if content:
        if re.search('Build succeeded.',content):
            return True
    return False

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
    tree = ET.parse(f"{project_path}/{project_path}.csproj")
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

#region 6.Loop zip files
def loop_zip_data():
    results = []
    worked = []
    # os.chdir(extract_path)
    ls_list = os.listdir()
    folders = [entry for entry in ls_list if os.path.isdir(os.path.join(extract_path, entry))]
    for i,ls_name in enumerate(folders):
        try :
            if not '.' in ls_name:
                
                build = execute_dotnet_build(ls_name)
                if build:
                    worked.append(ls_name);
                database = get_database(ls_name)
                version = get_version(ls_name)
                results.append({"build" : build, "db" : database, "version" : version})

                print(f"{ls_name}:\n")
                print(f" Build:    {'Build succeeded.' if build else 'failed.'}\n")
                print(f" DB Type:  {database['db_type']}\n")
                print(f" DB Name:  {database['db_name']}\n")
                # print(f" Database Name: {database["database_name"] or ''}")
                print(f" Version:  {version}\n");
                print("\n******************************************\n")
                return results

        except Exception as e:
            print(e)
        finally:
            continue
            # if i == len(folders) - 1:
                # os.chdir(current_path)
    
    print("worked Projects: " ,worked,'\n')
    print(results)
    return results,worked
#endregion

def delete_extracted_and_run():
    os.chdir(extract_path)
    delete_extracted_folders()
    extract_zip()
    return loop_zip_data()

if __name__ == "__main__":
    os.chdir(extract_path)
    print()
    delete_extracted_folders()
    # extract_zip()
    # loop_zip_data()
