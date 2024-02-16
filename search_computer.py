# Configuration section
logical_cpu_cores = 6  # max count of PC logical CPU Cores or number of Drive-Partitions

# Logic outline
# 1. Install imported packages if needed
# 2. run Script in Terminal or IDE
# 3. when prompted enter required Information
# 4. wait until results get printed

# Imports
import os
import psutil
import multiprocessing
import re


# Script logic
def get_partitions() -> list:
    partitions = psutil.disk_partitions()
    partition_list = []
    for partition in partitions:
        partition_list.append(partition.device)

    return partition_list


def search_for_file(filename, directory) -> list:
    found_paths = []
    for root, dirs, files in os.walk(directory):
        for current_filename in files:
            if re.findall(pattern=filename, string=current_filename, flags=re.IGNORECASE):
                found_paths.append(os.path.join(root, current_filename))

    print(f"Search in directory '{directory}' completed")
    return found_paths


def search_for_directory(directory_name, directory) -> list:
    found_paths = []
    for root, dirs, files in os.walk(directory):
        if directory_name in dirs:
            found_paths.append(os.path.join(root, directory_name))

    print(f"Search in directory '{directory}' completed")
    return found_paths


# Main function to execute the script
if __name__ == '__main__':
    multiprocessing.freeze_support()
    multiprocess = multiprocessing.Pool(processes=logical_cpu_cores)
    possible_parent_directories = []

    isFile = input('is File? (Y/n): ')  # yes -> File; not yes -> Directory
    parent_directory = str(input('parent Directory Path (leave empty if not known): '))

    # Search Directory
    if isFile == 'n':
        wanted_directory_name = str(input('Directory Name: '))
        print('')

        # search possible matches in every directory
        if not parent_directory:
            system_partition_list = get_partitions()

            results = multiprocess.starmap(search_for_directory, zip([wanted_directory_name] * len(system_partition_list), system_partition_list))

        # search possible match in parent directory
        else:
            if not os.path.exists(parent_directory):
                raise ValueError(f'The Path {parent_directory} does not exist')

            else:
                print('found Directories:')
                results = search_for_directory(directory_name=wanted_directory_name, directory=parent_directory)

    # Search File
    else:
        wanted_file_name = str(input('File Name: '))
        print('')

        # search possible matches in every directory
        if not parent_directory:
            system_partition_list = get_partitions()

            results = multiprocess.starmap(search_for_file, zip([wanted_file_name] * len(system_partition_list), system_partition_list))

        # search possible match in parent directory
        else:
            if not os.path.exists(parent_directory):
                raise ValueError(f'The Path {parent_directory} does not exist')

            else:
                print('found Files:')
                results = search_for_file(filename=wanted_file_name, directory=parent_directory)

    # add matches to List
    for result in results:
        if len(result) > 0:
            for current_directory in result:
                possible_parent_directories.append(current_directory)

    # print list as formatted itemize
    if len(possible_parent_directories) > 0:
        print('')
        print('The Search resulted in these paths:')
        for possible_directory in possible_parent_directories:
            print(f"\u2022 {possible_directory}")
    else:
        print('')
        print('The Search resulted in 0 matches')
