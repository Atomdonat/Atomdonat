import os
import psutil
import multiprocessing
import re


def get_partitions() -> list:
    partitions = psutil.disk_partitions()
    partition_list = []
    for partition in partitions:
        partition_list.append(partition.device)

    return partition_list


def search_file(filename, directory) -> list:
    found_paths = []
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if re.findall(pattern=filename, string=file_name, flags=re.IGNORECASE):
                found_paths.append(os.path.join(root, file_name))

    print(f"Search in directory '{directory}' completed")
    return found_paths


def search_directory(directory_name, directory) -> list:
    found_paths = []
    for root, dirs, files in os.walk(directory):
        if directory_name in dirs:
            found_paths.append(os.path.join(root, directory_name))

    print(f"Search in directory '{directory}' completed")
    return found_paths


if __name__ == '__main__':
    multiprocessing.freeze_support()  # Add this line
    multiprocess = multiprocessing.Pool(processes=4)  # Your multiprocessing code here

    isFile = input('is File? (Y/n): ')

    # Search Directory
    if isFile == 'n':
        dir_name = str(input('Directory Name: '))
        pos_directory = str(input('parent Directory Path (leave empty if not known): '))
        print('')

        if not pos_directory:
            partition_list = get_partitions()
            possible_directories = []

            results = multiprocess.starmap(search_directory, zip([dir_name] * len(partition_list), partition_list))

            for result in results:
                if len(result) > 0:
                    for current_directory in result:
                        possible_directories.append(current_directory)

            if len(possible_directories) > 0:
                print('')
                print('The Search resulted in these paths:')
                for possible_directory in possible_directories:
                    print(f"\u2022 {possible_directory}")
            else:
                print('')
                print('The Search resulted in 0 matches')

        else:
            if not os.path.exists(pos_directory):
                raise ValueError(f'The Path {pos_directory} does not exist')

            else:
                print('found Directories:')
                search_directory(directory_name=dir_name, directory=pos_directory)

    # Search File
    else:
        fil_name = str(input('File Name: '))
        pos_directory = str(input('parent Directory Path (leave empty if not known): '))
        print('')

        if not pos_directory:
            partition_list = get_partitions()
            possible_directories = []

            results = multiprocess.starmap(search_file, zip([fil_name] * len(partition_list), partition_list))

            for result in results:
                if len(result) > 0:
                    for current_directory in result:
                        possible_directories.append(current_directory)

            if len(possible_directories) > 0:
                print('')
                print('The Search resulted in these paths:')
                for possible_directory in possible_directories:
                    print(f"\u2022 {possible_directory}")

            else:
                print('')
                print('The Search resulted in 0 matches')

        else:
            if not os.path.exists(pos_directory):
                raise ValueError(f'The Path {pos_directory} does not exist')

            else:
                print('found Files:')
                search_file(filename=fil_name, directory=pos_directory)
