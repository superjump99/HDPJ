import os

def remove_files(folder_path, file_type):
    for filename in os.listdir(folder_path):
        if filename.endswith(file_type):
            try:
                os.remove(os.path.join(folder_path, filename))
            except ValueError:
                continue
    return

def renumbering_files(folder_path, file_type):
    file_list = os.listdir(folder_path)

    for i, old_name in enumerate(file_list):
        if old_name == 0:
            return

        if old_name.endswith(file_type):
            new_name = f"{i:06d}{file_type}"

            old_path = os.path.join(folder_path, old_name)
            new_path = os.path.join(folder_path, new_name)

            os.rename(old_path, new_path)
    return