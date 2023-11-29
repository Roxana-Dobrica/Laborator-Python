import os
import sys

#1. Create a Python script that does the following:
#Takes a directory path and a file extension as command line arguments (use sys.argv).
#Searches for all files with the given extension in the specified directory (use os module).
#For each file found, read its contents and print them.


def read_files_from_directory(directory_path, extension):
    try:
        if not os.path.isdir(directory_path) or not os.path.exists(directory_path):
            raise FileNotFoundError(f"Directory not found: {directory_path}")

        for file in os.listdir(directory_path):
            if file.endswith(extension):
                file_path = os.path.join(directory_path, file)
                try:
                    with open(file_path) as f:
                        print(f.read())
                except PermissionError:
                    print(f"Permission denied to read file: {file_path}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


#2. Write a script using the os module that renames all files in a specified directory to have a sequential number prefix.
# For example, file1.txt, file2.txt, etc. Include error handling for cases like the directory not existing or files that can't be renamed.


def rename_files(directory_path):
    try:
        if not os.path.isdir(directory_path) or not os.path.exists(directory_path):
            raise FileNotFoundError(f"Directory not found: {directory_path}")

        counter = 1
        for file in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file)

            if os.path.isfile(file_path):
                base_name = os.path.splitext(file)[0]
                file_extension = os.path.splitext(file)[1]
                new_name = os.path.join(directory_path, f"{base_name}{counter}{file_extension}")

                try:
                    os.rename(file_path, new_name)
                    counter += 1
                except PermissionError:
                    print(f"Permission denied to rename file: {file_path}")
                except FileNotFoundError:
                    print(f"File not found: {file_path}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


#3. Create a Python script that calculates the total size of all files in a directory provided as a command line argument. The script should:
# Use the sys module to read the directory path from the command line.
# Utilize the os module to iterate through all the files in the given directory and its subdirectories.
# Sum up the sizes of all files and display the total size in bytes.
# Implement exception handling for cases like the directory not existing, permission errors, or other file access issues.


def calculate_files_size(directory_path):
    try:
        if not os.path.isdir(directory_path) or not os.path.exists(directory_path):
            raise FileNotFoundError(f"Directory not found: {directory_path}")

        total_size = 0
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                total_size += os.path.getsize(file_path)
        print(f"Total size of all files in directory {directory_path} is {total_size} bytes.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except PermissionError as e:
        print(f"Error: Permission denied to access {e.filename}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


#4. Write a Python script that counts the number of files with each extension in a given directory. The script should:
# Accept a directory path as a command line argument (using sys.argv).
# Use the os module to list all files in the directory.
# Count the number of files for each extension (e.g., .txt, .py, .jpg) and print out the counts.
# Include error handling for scenarios such as the directory not being found, no read permissions, or the directory being empty.

def count_files_with_extension(directory_path):
    try:
        if not os.path.isdir(directory_path) or not os.path.exists(directory_path):
            raise FileNotFoundError(f"Directory not found: {directory_path}")

        files_with_extension = {}
        for file in os.listdir(directory_path):
            if os.path.isfile(os.path.join(directory_path, file)):
                file_extension = os.path.splitext(file)[1]
                if file_extension in files_with_extension:
                    files_with_extension[file_extension] += 1
                else:
                    files_with_extension[file_extension] = 1

        if not files_with_extension:
            print(f"No files found in the directory: {directory_path}")
        else:
            for extension, count in files_with_extension.items():
                print(f" {extension} - {count} ")

    except PermissionError as e:
        print(f"Error: Permission denied to access {e.filename}.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script_name.py <function_name> <directory_path> [additional_args]")
        sys.exit(1)

    function_name = sys.argv[1]
    directory_path = sys.argv[2]

    if function_name == "read_files_from_directory":
        if len(sys.argv) != 4:
            print("Usage: python script_name.py read_files_from_directory <directory_path> <file_extension>")
            sys.exit(1)
        file_extension = sys.argv[3]
        read_files_from_directory(directory_path, file_extension)

    elif function_name == "rename_files":
        rename_files(directory_path)

    elif function_name == "calculate_files_size":
        calculate_files_size(directory_path)

    elif function_name == "count_files_with_extension":
        count_files_with_extension(directory_path)

    else:
        print("Invalid function name.")
        sys.exit(1)


