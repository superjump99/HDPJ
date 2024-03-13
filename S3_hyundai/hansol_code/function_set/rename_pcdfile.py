import os


def rename_files(input_folder, output_folder):
    # 입력 폴더에서 파일 목록 가져오기
    file_list = os.listdir(input_folder)

    # 출력 폴더가 없으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 파일 이름 변경 및 저장
    for i, old_name in enumerate(file_list):
        # 새로운 파일 이름 생성
        if old_name.endswith('.pcd'):
            new_name = f"{i:06d}.pcd"

            # 입력 폴더의 파일 경로와 출력 폴더의 파일 경로 생성
            old_path = os.path.join(input_folder, old_name)
            new_path = os.path.join(output_folder, new_name)
            # 파일 이름 변경
            os.rename(old_path, new_path)

        elif old_name.endswith('jpg'):
            new_name = f"{i+1:06d}.jpg"

            # 입력 폴더의 파일 경로와 출력 폴더의 파일 경로 생성
            old_path = os.path.join(input_folder, old_name)
            new_path = os.path.join(output_folder, new_name)
            # 파일 이름 변경
            os.rename(old_path, new_path)
        # print(f"Renamed: {old_name} -> {new_name}")


def find_files_with_remainder_zero(folder_path):

    for filename in os.listdir(folder_path):
        if filename.endswith('.pcd'):
            file_number = int(filename.split('.')[0])
            if file_number % 25 != 0:
                os.remove(os.path.join(folder_path, filename))

        if filename.endswith('.jpg'):
            file_number = int(filename.split('.')[0])
            if file_number % 25 != 0:
                os.remove(os.path.join(folder_path, filename))
    return

# 사용 예시
if __name__ == '__main__':
    path = "C:/Users/pc/SS-233/hyundai_code"
    file_name = "HKMC-N2202209-240220110344-RFFR_LDL-0.0.0.1.0-RFFR_LDR-1"
    input_folder = f"{path}/S3_hyundai/1.working/{file_name}/pointclouds"
    output_folder = f"{path}/S3_hyundai/1.working/{file_name}/pointclouds"

    find_files_with_remainder_zero(input_folder)
    rename_files(input_folder, output_folder)

    imagef_input_folder = f"{path}/S3_hyundai/1.working/{file_name}/images/CAM_FRONT"
    imagefl_input_folder = f"{path}/S3_hyundai/1.working/{file_name}/images/CAM_FRONT_LEFT"
    imagefr_input_folder = f"{path}/S3_hyundai/1.working/{file_name}/images/CAM_FRONT_RIGHT"

    imagef_output_folder = f"{path}/S3_hyundai/1.working/{file_name}/images/CAM_FRONT"
    imagefl_output_folder = f"{path}/S3_hyundai/1.working/{file_name}/images/CAM_FRONT_LEFT"
    imagefr_output_folder = f"{path}/S3_hyundai/1.working/{file_name}/images/CAM_FRONT_RIGHT"

    find_files_with_remainder_zero(imagef_input_folder)
    find_files_with_remainder_zero(imagefl_input_folder)
    find_files_with_remainder_zero(imagefr_input_folder)
    rename_files(imagef_input_folder, imagef_output_folder)
    rename_files(imagefl_input_folder, imagefl_output_folder)
    rename_files(imagefr_input_folder, imagefr_output_folder)
