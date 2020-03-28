import datetime
import os
import time

from pyunpack import Archive

from config import *


# read the directory
def treat_archive():
    for file_path, directories, files in os.walk(read_from_dir):
        for f in files:
            process_file(file_path, f)


# treat current file
def process_file(filepath, c_file):
    current_file_path = os.path.join(filepath, c_file)
    filename, file_extension = os.path.splitext(c_file)
    if file_extension in files_extensions:
        if c_file.endswith('.zip'):
            extract_to_path = zip_path
        elif c_file.endswith('.rar'):
            extract_to_path = rar_path
        try:
            print(f"Processing the file: {c_file}")
            if not os.path.exists(extract_to_path):
                try:
                    os.mkdir(extract_to_path)
                except OSError:
                    print(f"Creation of the directory {extract_to_path} failed")

            Archive(current_file_path).extractall(extract_to_path)
            print(f"\t\t...extracted successfully to {extract_to_path}")
            if delete_source_file and os.path.exists(current_file_path):
                print(f"\t\t...remove source file...")
                os.remove(current_file_path)
                print(f"\t\t... source file was removed: {current_file_path}.")
        except Exception:
            print(f"The file {c_file} was not extracted.")


if __name__ == '__main__':
    start = time.perf_counter()
    if os.path.exists(read_from_dir):
        treat_archive()
    else:
        print(f"Please check if the path: '{read_from_dir}' with archives exists.")
        print("- Create or update the 'read_from_dir' variable with correct path.")
    finish = time.perf_counter()
    time_exec = str(datetime.timedelta(finish - start))
    print(f'Finished in {time_exec}')
