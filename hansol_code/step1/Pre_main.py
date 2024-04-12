import os
import shutil

from tqdm import tqdm

from hansol_code.step1.function_set.Pre_02_Remove_unnecessary_file import find_files_with_remainder_zero
from hansol_code.step1.function_set.Pre_03_Data_parsing import pcdbin_parser, pcdbin_to_pcd
from hansol_code.step1.function_set.Pre_04_rename_files import rename_files

if __name__ == '__main__':
    s3_path = 'S3_hyundai'
    step_path = 'step1'

    given_data_path = '0.given_data'
    div_remove_path = '1.div&remove'
    parsing_done_path = '2.parsing_done'

    space = "01_Hightway"
    dataset = "HKMC-N2202209-240208"

    os.chdir('../../')
    # print(os.getcwd())
    base_path = os.path.join(f"{os.getcwd()}/{s3_path}/{step_path}/")
    for i, sequence_set in enumerate(os.listdir(f"{base_path}/{given_data_path}/{space}/{dataset}/LDR_Raw_PCD/")):
        # print(sequence_set)
        try:
            if not os.path.exists(f"{base_path}/{given_data_path}/{space}/{dataset}/{sequence_set[12:]}"):
                given_folder = f"{base_path}/{given_data_path}/{space}/{dataset}"
                div_folder = f"{base_path}/{div_remove_path}/{space}/{dataset}"

                source_folder = f"{given_folder}/LDR_Raw_PCD/LDR_Raw_PCD-{sequence_set[12:]}/"
                target_folder = f"{div_folder}/{sequence_set[12:]}/pcd bin/"
                shutil.copytree(source_folder, target_folder)

                source_folder = f"{given_folder}/LDR_Raw_Image/LDR_Raw_Image-{sequence_set[12:]}/ImageFC"
                target_folder = f"{div_folder}/{sequence_set[12:]}/images/CAM_FRONT"
                shutil.copytree(source_folder, target_folder)

                source_folder = f"{given_folder}/LDR_Raw_Image/LDR_Raw_Image-{sequence_set[12:]}/ImageFL"
                target_folder = f"{div_folder}/{sequence_set[12:]}/images/CAM_FRONT_LEFT"
                shutil.copytree(source_folder, target_folder)

                source_folder = f"{given_folder}/LDR_Raw_Image/LDR_Raw_Image-{sequence_set[12:]}/ImageFR"
                target_folder = f"{div_folder}/{dataset}/images/CAM_FRONT_RIGHT"
                shutil.copytree(source_folder, target_folder)
                print(f"{i+1} [원천 데이터 분리 완료]", sequence_set[12:])
        except FileExistsError:
            print(f"{i+1} [폴더 이미 존재]", sequence_set[12:])

    for i, sequence_set in enumerate(os.listdir(f"{base_path}/{div_remove_path}/{space}/{dataset}")):

        div_folder = f"{base_path}/{div_remove_path}/{space}/{dataset}/{sequence_set}"
        PCDBIN_folder = f"{div_folder}/pcd bin"
        imageFC_folder = f"{div_folder}/images/CAM_FRONT"
        imageFR_folder = f"{div_folder}/images/CAM_FRONT_RIGHT"
        imageFL_folder = f"{div_folder}/images/CAM_FRONT_LEFT"
        find_files_with_remainder_zero(PCDBIN_folder)
        # rename_files(PCDBIN_folder)

        find_files_with_remainder_zero(imageFC_folder)
        rename_files.rename_files(imageFC_folder)

        find_files_with_remainder_zero(imageFR_folder)
        rename_files.rename_files(imageFR_folder)

        find_files_with_remainder_zero(imageFL_folder)
        rename_files.rename_files(imageFL_folder)

    for sequence_set in os.listdir(f"{base_path}/{div_remove_path}/{space}/{dataset}/"):
        annotation_folder = f"{base_path}/{div_remove_path}/{space}/{dataset}/{sequence_set}/annotations/"

        if not os.path.exists(annotation_folder):
            PCDBIN_folder = f"{base_path}/{div_remove_path}/{space}/{dataset}/{sequence_set}/pcd bin/"
            pointclouds_folder = f"{base_path}/{div_remove_path}/{space}/{dataset}/{sequence_set}/pointclouds/"

            for PCDBIN_file in tqdm(os.listdir(PCDBIN_folder)):
                input_file = os.path.join(PCDBIN_folder, PCDBIN_file)
                output_file = os.path.join(pointclouds_folder, os.path.splitext(PCDBIN_file)[0] + ".pcd")

                pre_processing_done_df = pcdbin_parser(input_file)
                pcdbin_to_pcd(pre_processing_done_df, pointclouds_folder, output_file)

            os.makedirs(annotation_folder)

            print(f" Success [작업 가능 폴더 생성 완료]", sequence_set)

        else:
            print(f"Error [이미 폴더 생성 완료]", sequence_set)

    for i, sequence_set in enumerate(os.listdir(f"{base_path}/{div_remove_path}/{space}/{dataset}")):
        PCDBIN_folder = f"{base_path}/{div_remove_path}/{space}/{dataset}/{sequence_set}/pcd bin"
        pointclouds_folder = f"{base_path}/{div_remove_path}/{space}/{dataset}/{sequence_set}/pointclouds"

        rename_files.rename_files(pointclouds_folder)

        if os.path.exists(PCDBIN_folder):
            shutil.rmtree(PCDBIN_folder)

        shutil.make_archive(f"{base_path}/{div_remove_path}/{space}/{dataset}/{sequence_set}",
                            'zip', root_dir=f"{base_path}/{parsing_done_path}/{space}/{dataset}/{sequence_set}")