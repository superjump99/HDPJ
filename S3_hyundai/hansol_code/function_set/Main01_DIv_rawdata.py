import os
import shutil


if __name__ == '__main__':

    high_path = 'C:/Users/pc/SS-233/hyundai_code'
    given_path = 'S3_hyundai/0.raw_data'
    step1_path = 'S3_hyundai/1.div&remove'
    space = "01_Hightway"
    dataset = "HKMC-N2202209-240208"

    for i, sequence_set in enumerate(os.listdir(f"{high_path}/{given_path}/{space}/{dataset}/LDR_Raw_PCD/")):
        try:
            if not os.path.exists(f"{high_path}/{given_path}/{space}/{sequence_set[12:]}"):

                source_folder = f"{high_path}/{given_path}/{space}/{dataset}/LDR_Raw_PCD/LDR_Raw_PCD-{sequence_set[12:]}/"
                target_folder = f"{high_path}/{step1_path}/{space}/{dataset}/{sequence_set[12:]}/pcdbin/"
                shutil.copytree(source_folder, target_folder)

                source_folder = f"{high_path}/{given_path}/{space}/{dataset}/LDR_Raw_Image/LDR_Raw_Image-{sequence_set[12:]}/ImageFC"
                target_folder = f"{high_path}/{step1_path}/{space}/{dataset}/{sequence_set[12:]}/images/CAM_FRONT"
                shutil.copytree(source_folder, target_folder)

                source_folder = f"{high_path}/{given_path}/{space}/{dataset}/LDR_Raw_Image/LDR_Raw_Image-{sequence_set[12:]}/ImageFL"
                target_folder = f"{high_path}/{step1_path}/{space}/{dataset}/{sequence_set[12:]}/images/CAM_FRONT_LEFT"
                shutil.copytree(source_folder, target_folder)

                source_folder = f"{high_path}/{given_path}/{space}/{dataset}/LDR_Raw_Image/LDR_Raw_Image-{sequence_set[12:]}/ImageFR"
                target_folder = f"{high_path}/{step1_path}/{space}/{dataset}/{sequence_set[12:]}/images/CAM_FRONT_RIGHT"
                shutil.copytree(source_folder, target_folder)
                print(f"{i+1} [원천 데이터 분리 완료]", sequence_set[12:])
        except FileExistsError:
            print(f"{i+1} [폴더 이미 존재]", sequence_set[12:])