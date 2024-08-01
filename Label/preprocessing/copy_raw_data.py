import shutil


def raw_pcd_processing(source_path, folder_name, target_path):
    try:
        extract_files(source_path, target_path)
        print(f"[PCD copy completed]")

    except FileExistsError:
        print(f"[PCD copy already completed]")
    return

def raw_image_processing(source_path, folder_name, target_path):
    try:
        for folder in os.listdir(source_path):
            if folder == 'ImageFC':
                CF_folder = os.path.join(target_path, f'{folder_name}/images/CAM_FRONT')
                extract_files(f'{source_path}/ImageFC_deid', CF_folder)
                renumbering_files(CF_folder, '.jpg')
            elif folder == 'ImageFL':
                CFL_folder = os.path.join(target_path, f'{folder_name}/images/CAM_FRONT_LEFT')
                extract_files(f'{source_path}/ImageFL_deid', CFL_folder)
                renumbering_files(CFL_folder, '.jpg')
            elif folder == 'ImageFR':
                CFR_folder = os.path.join(target_path, f'{folder_name}/images/CAM_FRONT_RIGHT')
                extract_files(f'{source_path}/ImageFR_deid', CFR_folder)
                renumbering_files(CFR_folder, '.jpg')
            else:
                pass
        print(f"[Image copy completed]")

    except FileExistsError:
        print(f"[Image copy already completed]")
    return


def extract_files(source_folder, target_folder):
    os.makedirs(target_folder, exist_ok=True)

    for filename in os.listdir(source_folder):
        file_number = ''.join(filter(str.isdigit, filename))

        if file_number.isdigit() and int(file_number) % 25 == 0:
            file_path = os.path.join(source_folder, filename)

            if os.path.isfile(file_path):
                shutil.copy(file_path, target_folder)