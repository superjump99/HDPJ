import os
import Pre_02_Remove_unnecessary_file

def rename_files(folder):
    # 입력 폴더에서 파일 목록 가져오기
    file_list = os.listdir(folder)

    # 출력 폴더가 없으면 생성
    if not os.path.exists(folder):
        os.makedirs(folder)

    # 파일 이름 변경 및 저장
    num = 0
    for i, old_name in enumerate(file_list):
        # 새로운 파일 이름 생성
        if old_name.endswith('.pcdbin'):
            new_name = f"{i:06d}.pcd"

            # 입력 폴더의 파일 경로와 출력 폴더의 파일 경로 생성
            old_path = os.path.join(folder, old_name)
            new_path = os.path.join(folder, new_name)
            # 파일 이름 변경
            os.rename(old_path, new_path)

        elif old_name.endswith('jpg'):
            num += 0.5
            new_name = f"{num}.jpg"

            # 입력 폴더의 파일 경로와 출력 폴더의 파일 경로 생성
            old_path = os.path.join(folder, old_name)
            new_path = os.path.join(folder, new_name)
            # 파일 이름 변경
            os.rename(old_path, new_path)


if __name__ == '__main__':
    os.chdir('../../../')
    print(os.getcwd())
    image_path = os.path.join(os.getcwd(), 'S3_hyundai/step1/1.div&remove/01_Hightway/HKMC-N2202209-240208/HKMC-N2202209-240208102748-RFFR_LDL-0.0.0.1.0-RFFR_LDR-1')
    print(image_path)
    # exit()
    # for i, sequence_set in enumerate(os.listdir(f"{base_path}/{div_remove_path}/{space}/{dataset}")):

        # div_folder = f"{base_path}/{div_remove_path}/{space}/{dataset}/{sequence_set}"
    PCDBIN_folder = f"{image_path}/pcdbin"
    imageFC_folder = f"{image_path}/images/CAM_FRONT"
    imageFR_folder = f"{image_path}/images/CAM_FRONT_RIGHT"
    imageFL_folder = f"{image_path}/images/CAM_FRONT_LEFT"
    print(PCDBIN_folder)
    Pre_02_Remove_unnecessary_file.remove_files(PCDBIN_folder)
    # rename_files(PCDBIN_folder)

    Pre_02_Remove_unnecessary_file.remove_files(imageFC_folder)
    rename_files(imageFC_folder)

    PCDBIN_folder = f"{image_path}/pcdbin"
    pointclouds_folder = f"{image_path}/pointclouds"

    rename_files(pointclouds_folder)