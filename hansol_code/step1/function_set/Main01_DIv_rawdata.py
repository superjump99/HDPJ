import os
import shutil


if __name__ == '__main__':

    s3_path = 'S3_hyundai'
    step_path = 'step1'

    given_data_path = '0.given_data'
    div_remove_path = '1.div&remove'

    space = "01_Hightway"
    dataset = "HKMC-N2202209-240208"

    os.chdir('../../../')
    base_path = os.path.join(f"{os.getcwd()}/{s3_path}/{step_path}/")
    # print(base_path)
    # exit()
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