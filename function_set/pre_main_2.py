from tqdm import tqdm
from function_set.copy_raw_data import *
from function_set.Data_parsing_2 import *
from function_set.remove_unnecessary_file import *

if __name__ == '__main__':
    EHD = "E:/HDC/"

    save_location = "C:/Users/pc/Desktop"
    os.chdir(save_location)
    print(os.getcwd())
    bucket_name = "coop-selectstar-7000527-241231/"

    step = "01_Label/"
    sensor = "02_PANDAR_MV/"
    space = "02_ParkingLot"

    # STEP 1: Set base file
    middle_folder_name = os.listdir(f'{EHD}/{bucket_name}/{step}/{sensor}/{space}/')[0]
    raw_data_path = os.path.join(f'{EHD}/{bucket_name}/{step}/{sensor}/{space}/', middle_folder_name)
    save_data_path = os.path.join(f'{save_location}/{bucket_name}/{step}/{sensor}/{space}/', middle_folder_name)

    os.makedirs(save_data_path, exist_ok=True)

    LDR_Raw_PCD = os.path.join(raw_data_path, "LDR_RAW_PCD")
    LDR_RAW_Image = os.path.join(raw_data_path, "LDR_RAW_Image")

    for pcd_folder in os.listdir(f'{LDR_Raw_PCD}'):
        os.makedirs(os.path.join(save_data_path, f"{pcd_folder}/annotations"), exist_ok=True)
        sequence_set = pcd_folder[12:]
        print(sequence_set)

        # STEP 2. Extract raw pcdbin
        raw_pcd_folder = os.path.join(LDR_Raw_PCD, pcd_folder)
        pointclouds_folder = os.path.join(save_data_path, f"{sequence_set}/pointclouds")
        raw_pcd_processing(raw_pcd_folder, sequence_set, pointclouds_folder)

        # STEP 3. Extract raw image
        raw_image_set = f"LDR_Raw_Image-{sequence_set}"
        for image_folder in os.listdir(f'{LDR_RAW_Image}'):
            if image_folder == raw_image_set:
                raw_image_folder = os.path.join(LDR_RAW_Image, image_folder)
                raw_image_processing(raw_image_folder, sequence_set, save_data_path)

        # STEP 4. Parsing
        for pcdbin in tqdm(os.listdir(pointclouds_folder)):
            file_number = int(pcdbin.split('.')[0])

            if file_number % 25 == 0:
                input_file = os.path.join(pointclouds_folder, pcdbin)
                output_file = os.path.join(pointclouds_folder, f"{os.path.splitext(pcdbin)[0]}.pcd")

                pre_processing_done_df = pcdbin_parser(input_file)
                pcdbin_to_pcd(pre_processing_done_df, output_file)

        # STEP 5: Remove and Rename current data PCD files
        remove_files(pointclouds_folder, '.pcdbin')
        renumbering_files(pointclouds_folder, '.pcd')
