import os
import shutil
from tqdm import tqdm

from function_set.remove_unnecessary_file import remove_files, rename_files
from function_set.Data_parsing_2 import pcdbin_parser, pcdbin_to_pcd

from function_set.copy_raw_data import * # step 2 copy raw pcd and images

if __name__ == '__main__':
    drive = 'C:/Users/pc/Desktop'
    os.chdir(drive)
    print(os.getcwd())
    bucket_name = '1-coop-selectstar-7000527-241231/'
    ''' :parameter
        step
            :param  
            '01_Label/'
            '02_Inspection/'
        sensor
            :param
            '01_IRIS_JX013/'
            '02_PANDAR_MV/'
        space
            :param
            '01_Highway/'
            '02_ParkingLot/'
            '03_Urban/'
    '''

    step = '01_Label/'
    sensor = '02_PANDAR_MV/'
    space = "01_Highway/"
    middle_folder_name = 'HKMC-N2310382-240411'

    # STEP 1: Set base file
    base_path = os.path.join(f'{os.getcwd()}/{bucket_name}/{step}/{sensor}/{space}/')
    print(base_path)

    if not os.path.exists(base_path): os.makedirs(base_path)
    if os.listdir(base_path): middle_folder_name = os.listdir(base_path)[0]

    middle_folder = os.path.join(f'{base_path}/{middle_folder_name}')
    print(middle_folder)

    if not os.path.exists(f'{middle_folder}'): os.makedirs(middle_folder)
    if not os.path.exists(f'{middle_folder}/LDR_GT_Point/'): os.makedirs(f'{middle_folder}/LDR_GT_Point/')
    if not os.path.exists(f'{middle_folder}/LDR_GT_Property/'): os.makedirs(f'{middle_folder}/LDR_GT_Property/')
    if not os.path.exists(f'{middle_folder}/LDR_RAW_Image/'): os.makedirs(f'{middle_folder}/LDR_RAW_Image/')
    if not os.path.exists(f'{middle_folder}/LDR_RAW_PCD/'): os.makedirs(f'{middle_folder}/LDR_RAW_PCD/')
    if not os.path.exists(f'{middle_folder}/DATA/'): os.makedirs(f'{middle_folder}/DATA/')

    RAW_PCD_path = os.path.join(middle_folder, 'LDR_RAW_PCD')
    RAW_Image_path = os.path.join(middle_folder, 'LDR_RAW_Image')
    DATA_path = os.path.join(middle_folder, 'DATA')

    # STEP 2. Copy Raw Data
    print("== Step 2. Copy Raw Data ")
    # STEP 2-1: Copy Raw PCD
    print("=== Step 2-1. Copy Raw PCD")
    for i, sequence_set in enumerate(os.listdir(RAW_PCD_path)):
        try:
            sequence_pcd_path = os.path.join(DATA_path, f'{sequence_set[12:]}/pcdbin')
            if not os.path.exists(os.path.join(DATA_path, f'{sequence_set[12:]}/pointclouds/')):
                source_folder = f"{RAW_PCD_path}/{sequence_set}/"
                target_folder = f"{sequence_pcd_path}/"
                shutil.copytree(source_folder, target_folder)
                print(f"{i} [PCD copy completed]", sequence_set[12:])

        except FileExistsError:
            print(f"{i} [PCD copy already completed]", sequence_set[12:])

    # STEP 2-2: Copy Raw Images
    print("=== Step 2-2. Copy Raw Image")
    for i, sequence_set in enumerate(os.listdir(RAW_Image_path)):
        try:
            sequence_image_path = os.path.join(DATA_path, f'{sequence_set[14:]}/images')
            if not os.path.exists(sequence_image_path):
                source_folder = f"{RAW_Image_path}/{sequence_set}/ImageFC"
                target_folder = f"{sequence_image_path}/CAM_FRONT/"
                shutil.copytree(source_folder, target_folder)

                source_folder = f"{RAW_Image_path}/{sequence_set}/ImageFL"
                target_folder = f"{sequence_image_path}/CAM_FRONT_LEFT/"
                shutil.copytree(source_folder, target_folder)

                source_folder = f"{RAW_Image_path}/{sequence_set}/ImageFR"
                target_folder = f"{sequence_image_path}/CAM_FRONT_RIGHT/"
                shutil.copytree(source_folder, target_folder)
                print(f"{i} [Image copy completed]", sequence_set[14:])

        except FileExistsError:
            print(f"{i} [Image copy already completed]", sequence_set[14:])

    # STEP 3. Preprocessing
    print("== STEP 3. Preprocessing ")
    for i, sequence_set in enumerate(os.listdir(f"{DATA_path}")):
        print(i, sequence_set)
        data_sequence_path = os.path.join(f'{DATA_path}', sequence_set)

        if not os.path.exists(os.path.join(DATA_path, f'{sequence_set}/annotations')):
            os.makedirs(os.path.join(DATA_path, f'{sequence_set}/annotations'))

        # STEP 3-1: Check older data: Remove and rename Images files
        print(f"=== STEP 3-1: Check Image data: Remove and rename Images files")
        # TODO : image 처리가 잘못된게 있다면 에러 발생하게
        if os.path.exists(os.path.join(DATA_path, f'{sequence_set}/images')):
            if not os.listdir(os.path.join(DATA_path, f'{sequence_set}/images/CAM_FRONT'))[0] == '000000.jpg':
                remove_files(os.path.join(data_sequence_path, 'images/CAM_FRONT/'))
                rename_files(os.path.join(data_sequence_path, 'images/CAM_FRONT/'))

                remove_files(os.path.join(data_sequence_path, 'images/CAM_FRONT_LEFT/'))
                rename_files(os.path.join(data_sequence_path, 'images/CAM_FRONT_LEFT/'))

                remove_files(os.path.join(data_sequence_path, 'images/CAM_FRONT_RIGHT/'))
                rename_files(os.path.join(data_sequence_path, 'images/CAM_FRONT_RIGHT/'))
            else:
                pass

        # STEP 3-2: Check older data: Remove and rename PCD files
        print(f"=== STEP 3-2: Check PCD data: Remove and rename PCD files ")
        # TODO : PCD 처리가 잘못된게 있다면 에러 발생하게
        if os.path.exists(os.path.join(DATA_path, f'{sequence_set}/pointclouds')):
            if not os.listdir(os.path.join(DATA_path, f'{sequence_set}/pointclouds'))[0] == '000000.pcd':
                remove_files(os.path.join(data_sequence_path, 'pointclouds'))
                rename_files(os.path.join(data_sequence_path, 'pointclouds'))
            else:
                if os.path.exists(os.path.join(DATA_path, f'{sequence_set}/pcdbin')):
                    shutil.rmtree(os.path.join(DATA_path, f'{sequence_set}/pcdbin'))
            continue

        # STEP 3-3. Parsing data
        print(f"=== STEP 3-3: Parsing data")
        for pcdbin in tqdm(os.listdir(os.path.join(DATA_path, f"{sequence_set}/pcdbin"))):
            file_number = int(pcdbin.split('.')[0])
            if file_number % 25 == 0:
                input_file = os.path.join(DATA_path, f'{sequence_set}/pcdbin/{pcdbin}')
                output_file = os.path.join(DATA_path, f'{sequence_set}/pointclouds/{os.path.splitext(pcdbin)[0]}.pcd')
                if not os.path.exists(os.path.join(DATA_path, f'{sequence_set}/pointclouds')):
                    os.makedirs(os.path.join(DATA_path, f'{sequence_set}/pointclouds'))

                pre_processing_done_df = pcdbin_parser(input_file)
                pcdbin_to_pcd(pre_processing_done_df, output_file)

        # STEP 3-4: Remove and Rename current data PCD files
        data_sequence_path = os.path.join(f'{DATA_path}', sequence_set)

        remove_files(os.path.join(data_sequence_path, 'pointclouds'))
        rename_files(os.path.join(data_sequence_path, 'pointclouds'))


        # STEP 3-5: Remove pcdbin folder
        if os.path.exists(os.path.join(DATA_path, f'{sequence_set}/pcdbin')):
            shutil.rmtree(os.path.join(DATA_path, f'{sequence_set}/pcdbin'))

        # TODO: QA 진행하는 코드 추가 작성
        # STEP 5. mk zip
        # shutil.make_archive(f"{DATA_path}/{sequence_set}",
        #                     'zip', root_dir=f"{DATA_path}/{sequence_set}")
