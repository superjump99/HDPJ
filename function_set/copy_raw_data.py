import os
import shutil


def copy_raw_pcd(source_path, folder_name, target_path):
    save_path = os.path.join(target_path, f'{folder_name}/pcdbin')
    try:
        shutil.copytree(source_path, save_path)
        print(f"[PCD copy completed]")
    except FileExistsError:
        print(f"[PCD copy already completed]")
    finally:
        return save_path

def copy_raw_image(source_path, folder_name, target_path):
    try:
        for folder in os.listdir(source_path):
            if folder == 'ImageFC':
                target_fc = os.path.join(target_path, f'{folder_name}/images/CAM_FRONT')
                shutil.copytree(f'{source_path}/ImageFC_deid', target_fc)
            elif folder == 'ImageFL':
                target_fl = os.path.join(target_path, f'{folder_name}/images/CAM_FRONT_LEFT')
                shutil.copytree(f'{source_path}/ImageFL_deid', target_fl)
            elif folder == 'ImageFR':
                target_fr = os.path.join(target_path, f'{folder_name}/images/CAM_FRONT_RIGHT')
                shutil.copytree(f'{source_path}/ImageFR_deid', target_fr)
            else:
                pass
        return print(f"[Image copy completed]")

    except FileExistsError:
        return print(f"[Image copy already completed]")
