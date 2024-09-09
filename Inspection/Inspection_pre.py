import shutil
import Label.preprocessing
import os
import reverse_process
from tqdm import tqdm

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


if __name__ == '__main__':

    step = "02_Inspection/"
    sensor = "01_IRIS_JX013/"
    space = "01_Highway/"

    EHD = "E:/HDC/"
    save_location = "C:/Users/pc/Desktop"
    os.chdir(save_location)
    print(os.getcwd())
    bucket_name = "coop-selectstar-7000527-241231/"

    # STEP 1: Set base file
    try:
        middle_folder_name = os.listdir(f'{EHD}/{bucket_name}/{step}/{sensor}/{space}/')[0]
    except:
        EHD = "D:/HDC/"
    finally:
        middle_folder_name = os.listdir(f'{EHD}/{bucket_name}/{step}/{sensor}/{space}/')[0]
        raw_data_path = os.path.join(f'{EHD}/{bucket_name}/{step}/{sensor}/{space}/', middle_folder_name)
        save_data_path = os.path.join(f'{save_location}/{bucket_name}/{step}/{sensor}/{space}/', middle_folder_name)
    print(raw_data_path)

    os.makedirs(save_data_path, exist_ok=True)

    LDR_Raw_PCD = os.path.join(raw_data_path, "LDR_RAW_PCD")
    LDR_RAW_Image = os.path.join(raw_data_path, "LDR_RAW_Image")
    LDR_GT_BOX = os.path.join(raw_data_path, "LDR_GT_BOX")

    # 폴더 별 데이터 파싱 진행
    for pcd_folder in os.listdir(f'{LDR_Raw_PCD}'):
        sequence_set = pcd_folder[12:]
        print(sequence_set)

        # 검수할 json 파일 annotations 폴더로 변환
        LDR_GT_BOX = os.path.join(raw_data_path, "LDR_GT_BOX")
        annotation_folder = os.path.join(save_data_path, f"{sequence_set}/annotations")
        os.makedirs(annotation_folder, exist_ok=True)
        parsing_num = reverse_process.reverse_parsing(LDR_GT_BOX, sequence_set, annotation_folder)

        file = open(os.path.join(save_data_path, f"{sequence_set}/parsing_num.txt"), 'w')
        w = file.write(f'{parsing_num[0]} ~ {parsing_num[-1]}')

        # STEP 2. Extract raw pcdbin
        raw_pcd_folder = os.path.join(LDR_Raw_PCD, pcd_folder)
        pointclouds_folder = os.path.join(save_data_path, f"{sequence_set}/pointclouds")
        Label.preprocessing.raw_pcd_processing(raw_pcd_folder, pointclouds_folder, target_file=parsing_num)

        # STEP 3. Extract raw image
        raw_image_set = f"LDR_Raw_Image-{sequence_set}"
        for image_folder in os.listdir(f'{LDR_RAW_Image}'):
            if image_folder == raw_image_set:
                raw_image_folder = os.path.join(LDR_RAW_Image, image_folder)
                Label.preprocessing.raw_image_processing(
                    raw_image_folder, sequence_set, os.path.join(save_data_path, sequence_set), target_file=parsing_num)

        # STEP 4. Parsing
        for pcdbin in tqdm(os.listdir(pointclouds_folder)):
            file_number = int(pcdbin.split('.')[0])

            if file_number in parsing_num:
                input_file = os.path.join(pointclouds_folder, pcdbin)
                output_file = os.path.join(pointclouds_folder, f"{os.path.splitext(pcdbin)[0]}.pcd")

                pre_processing_done_df = Label.preprocessing.pcdbin_parser(input_file)
                Label.preprocessing.pcdbin_to_pcd(pre_processing_done_df, output_file)

        # STEP 5. Remove pcdbin files and Rename PCD files
        Label.preprocessing.remove_files(pointclouds_folder, '.pcdbin')
        Label.preprocessing.renumbering_files(pointclouds_folder, '.pcd')

        # xlsx 파일 복사
        root = f'{EHD}/{bucket_name}/{step}/LDR_INSPECTION-.xlsx'
        target = os.path.join(save_data_path, f"{sequence_set}")
        shutil.copy(root,target)
        os.rename(os.path.join(target, "LDR_INSPECTION-.xlsx"), os.path.join(target, f"LDR_INSPECTION-{sequence_set}.xlsx"))

        # STEP 7. mk zip
        shutil.make_archive(f"{save_data_path}/{sequence_set}", 'zip',
                            f"{save_data_path}/{sequence_set}")
