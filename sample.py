import re

build_output = """
MSBuild version 17.4.1+9a89d02ff for .NET
Determining projects to restore...
All projects are up-to-date for restore.
/Users/prudvi/Desktop/ui/media/MovieList/Controllers/MovieController.cs(35,18): error CS1002: ; expected [/Users/prudvi/Desktop/ui/media/MovieList/MovieList.csproj]
/Users/prudvi/Desktop/ui/media/MovieList/Controllers/HomeController.cs(10,9): error CS1585: Member modifier private must precede the member type and name [/Users/prudvi/Desktop/ui/media/MovieList/MovieList.csproj]

Build FAILED.

/Users/prudvi/Desktop/ui/media/MovieList/Controllers/MovieController.cs(35,18): error CS1002: ; expected [/Users/prudvi/Desktop/ui/media/MovieList/MovieList.csproj]
/Users/prudvi/Desktop/ui/media/MovieList/Controllers/HomeController.cs(10,9): error CS1585: Member modifier private must precede the member type and name [/Users/prudvi/Desktop/ui/media/MovieList/MovieList.csproj]
0 Warning(s)
2 Error(s)

Time Elapsed 00:00:01.64
"""

# Regular expression pattern
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
        print("Error:")
        print(f"File: {filename}")
        print(f"Line number: {line_number}")
        print(f"Error Message: {error_message}")
        print(f"Error Code: {error_code}")
        print()
        unique_errors.add(error)
        error_count += 1

# Check if "Build FAILED" line is present
if "Build FAILED" in build_output:
    print("Build FAILED.")

print(f"Total Errors: {error_count}")

