import pytest
import pathlib
import os
import shutil
import filecmp

def copy_file(source_file, destination_directory):
    shutil.copy2(source_file, destination_directory)


def collect_file_info(directory_path):
    file_info = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            file_info.append((file, file_size))
    return file_info


def write_file_info(file_info, output_file):
    with open(output_file, 'w') as f:
        for file, size in file_info:
            f.write(f"{file}\t{size} bytes\n")


idea_options_info_filename = 'idea_options_txt'
before_files_directory = 'C:\\Users\\janina\\work\\files_before'
after_files_directory = 'C:\\Users\\janina\\work\\files_after'
options_directory = 'C:\\Users\\janina\\AppData\\Roaming\\JetBrains\\IntelliJIdea2023.1\\options'

laf_file_path = '%s\\laf.xml' % options_directory
projects_file_path = '%s\\recentProjects.xml' % options_directory
before_vm_options_path = 'C:\\Users\\janina\\AppData\\Local\\JetBrains\\Toolbox\\apps\\IDEA-U\\ch-0\\231.9011.34.vmoptions'
after_vm_options = 'C:\\Users\\janina\\AppData\\Roaming\\JetBrains\\IntelliJIdea2023.1\\idea64.exe.vmoptions'


def test_dump_files_info_before():
    idea_options_file_info = collect_file_info(options_directory)
    write_file_info(idea_options_file_info, before_files_directory + '\\' + idea_options_info_filename)
    copy_file(laf_file_path, before_files_directory + '\\' + 'laf.xml')
    copy_file(projects_file_path, before_files_directory + '\\' + 'recentProjects.xml')
    copy_file(before_vm_options_path, before_files_directory + '\\' + '231.9011.34.vmoptions')


def test_dump_files_info_after():
    idea_options_file_info = collect_file_info(options_directory)
    write_file_info(idea_options_file_info, after_files_directory + '\\' + idea_options_info_filename)
    copy_file(laf_file_path, after_files_directory + '\\' + 'laf.xml')
    copy_file(projects_file_path, after_files_directory + '\\' + 'recentProjects.xml')
    copy_file(after_vm_options, after_files_directory + '\\' + '231.9011.34.vmoptions')


def compare_settings_files(file1_path, file2_path):
    with open(file1_path, 'r') as file1:
        content1 = file1.read()

    with open(file2_path, 'r') as file2:
        content2 = file2.read()
    return content1 == content2


def test_compare_directories():
    old_directory = 'C:\\Users\\janina\\work\\files_before'
    new_directory = 'C:\\Users\janina\\work\\files_after'
    differing_files = []

    for dirpath, dirnames, filenames in os.walk(old_directory):
        for filename in filenames:
            old_file = os.path.join(dirpath, filename)
            new_file = os.path.join(new_directory, os.path.relpath(old_file, old_directory))

            if os.path.isfile(new_file) and not filecmp.cmp(old_file, new_file, shallow=False):
                differing_files.append(filename)

    return differing_files


