import os
import shutil
from tqdm import tqdm
from function_set.copy_raw_data import *
from function_set.Data_parsing_2 import *
from function_set.remove_unnecessary_file import *

if __name__ == '__main__':
    EHD = 'E:/HDC/'

    save_location = 'C:/Users/pc/Desktop'
    os.chdir(save_location)
    print(os.getcwd())
    bucket_name = 'coop-selectstar-7000527-241231/'

    step = '01_Label/'
    sensor = '02_PANDAR_MV/'
    space = "02_ParkingLot"

    # STEP 1: Set base file
    middle_folder = os.listdir(f'{EHD}/{bucket_name}/{step}/{sensor}/{space}/')[0]
    raw_data_path = os.path.join(f'{EHD}/{bucket_name}/{step}/{sensor}/{space}/', middle_folder)
    save_data_path = os.path.join(f'{save_location}/{bucket_name}/{step}/{sensor}/{space}/', middle_folder)
    print(save_data_path)

    if not os.path.exists(save_data_path): os.makedirs(save_data_path)


    raw_pcd_folder = os.path.join(raw_data_path, 'LDR_RAW_PCD')
    raw_image_folder = os.path.join(raw_data_path, 'LDR_RAW_Image')

    for pcd_folder in os.listdir(f'{raw_pcd_folder}'):
        sequence_set = pcd_folder[12:]
        print(sequence_set)

        source_path = os.path.join(raw_pcd_folder, pcd_folder)
        pcdbin_folder = copy_raw_pcd(source_path, sequence_set, save_data_path)
        Raw_image_folder = f'LDR_Raw_Image-{sequence_set}'
        for image_folder in os.listdir(f'{raw_image_folder}'):
            if image_folder == Raw_image_folder:
                source_path = os.path.join(raw_image_folder, image_folder)
                copy_raw_image(source_path, sequence_set, save_data_path)

        print(pcdbin_folder)


        print(save_data_path)
        save_path = os.path.join(save_data_path, f'{sequence_set}/pointclouds')
        if not os.path.exists(save_path): os.makedirs(save_path)
        print(save_path)

        for pcdbin in tqdm(os.listdir(pcdbin_folder)):
            file_number = int(pcdbin.split('.')[0])

            if file_number % 25 == 0:
                input_file = os.path.join(pcdbin_folder, pcdbin)
                output_file = os.path.join(save_path, f'{os.path.splitext(pcdbin)[0]}.pcd')
                # print(output_file)
                # exit()
                pre_processing_done_df = pcdbin_parser(input_file)
                pcdbin_to_pcd(pre_processing_done_df, output_file)

        # STEP 3-4: Remove and Rename current data PCD files
        remove_files(save_path)
        rename_files(save_path)

        # STEP 3-5: Remove pcdbin folder
        if os.path.exists(pcdbin_folder):
            shutil.rmtree(pcdbin_folder)
        break
        # break
        # Raw_image_folder = f'LDR_Raw_Image-{raw_pcd_folder[12:]}'

        #     print(RIF)
        # break
        # copy_raw_image(Raw_image_folder, DATA_path)
        #
        # break