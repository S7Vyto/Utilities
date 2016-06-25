import os
from enum import Enum


class Position(Enum):
    start = 1
    end = 2


class ProjectType(Enum):
    android = 1
    iOS = 2


def change_file_name(find_char, new_char, folder_name):
    dir_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "RegionXML", folder_name)

    if os.path.exists(dir_path):
        if os.path.isdir(dir_path):
            dir_files = [file for file in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, file))]
            for file_name in dir_files:
                if file_name == '.DS_Store':
                    continue

                clean_name = file_name
                clean_name = clean_name.replace(find_char, new_char)
                clean_name = clean_name.lower()

                if clean_name.startswith('-'):
                    clean_name = clean_name[1:]

                print(clean_name)
                os.rename(os.path.join(dir_path, file_name), os.path.join(dir_path, clean_name))


def change_file_extension(project, position, append_string, folder_name, exclude_names):
    dir_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "RegionXML", folder_name)

    if os.path.exists(dir_path):
        if os.path.isdir(dir_path):
            dir_files = [file for file in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, file))]
            for file_name in dir_files:
                if file_name == '.DS_Store' or file_name in exclude_names:
                    continue

                clean_name = file_name

                ## iOS Projects
                if project == ProjectType.iOS:
                    if '_ipad' in clean_name.lower():
                        clean_name = clean_name.replace('_ipad', '')
                    elif '_iphone' in clean_name.lower():
                        clean_name = clean_name.replace('_iphone', '')

                    if '@2x' in clean_name:
                        clean_name = clean_name.replace('@2x', append_string + '@2x')
                    elif '@3x' in clean_name:
                        clean_name = clean_name.replace('@3x', append_string + '@3x')
                    else:
                        clean_name = clean_name.replace('.', append_string + '.')
                ## Android Projects
                elif project == ProjectType.android:
                    if append_string not in clean_name:
                        if position == Position.start:
                            clean_name = append_string + clean_name
                        elif position == Position.end:
                            clean_name = clean_name.replace('.png', append_string)

                print(clean_name)
                os.rename(os.path.join(dir_path, file_name), os.path.join(dir_path, clean_name))

##change_file_name('-', '_', 'topics')
change_file_extension(ProjectType.iOS, Position.end, '_iPhone', 'buttons', [])

