import os

def find_files_with_remainder_zero(folder_path):

    for filename in os.listdir(folder_path):
        if filename.endswith('.pcdbin'):
            file_number = int(filename.split('.')[0])
            if file_number % 25 != 0:
                os.remove(os.path.join(folder_path, filename))

        if filename.endswith('.jpg'):
            file_number = int(filename.split('.')[0])
            if file_number % 25 != 0:
                os.remove(os.path.join(folder_path, filename))
    return

def rename_files(folder):
    # 입력 폴더에서 파일 목록 가져오기
    file_list = os.listdir(folder)

    # 출력 폴더가 없으면 생성
    if not os.path.exists(folder):
        os.makedirs(folder)

    # 파일 이름 변경 및 저장
    for i, old_name in enumerate(file_list):
        # 새로운 파일 이름 생성
        if old_name.endswith('.pcd'):
            new_name = f"{i:06d}.pcd"

            # 입력 폴더의 파일 경로와 출력 폴더의 파일 경로 생성
            old_path = os.path.join(folder, old_name)
            new_path = os.path.join(folder, new_name)
            # 파일 이름 변경
            os.rename(old_path, new_path)

        elif old_name.endswith('jpg'):
            new_name = f"{i + 1:06d}.jpg"

            # 입력 폴더의 파일 경로와 출력 폴더의 파일 경로 생성
            old_path = os.path.join(folder, old_name)
            new_path = os.path.join(folder, new_name)
            # 파일 이름 변경
            os.rename(old_path, new_path)


if __name__ == '__main__':

    high_path = '/'
    given_path = 'S3_hyundai/0.given_data'
    step1_path = 'S3_hyundai/1.div&remove'
    space = "00_sample"
    dataset = "HKMC-N2202209-240111"

    for i, sequence_set in enumerate(os.listdir(f"{high_path}/{step1_path}/{space}/{dataset}")):
        pcdbin_folder = f"{high_path}/{step1_path}/{space}/{dataset}/{sequence_set}/pcdbin"
        imageFC_folder = f"{high_path}/{step1_path}/{space}/{dataset}/{sequence_set}/images/CAM_FRONT"
        imageFR_folder = f"{high_path}/{step1_path}/{space}/{dataset}/{sequence_set}/images/CAM_FRONT_RIGHT"
        imageFL_folder = f"{high_path}/{step1_path}/{space}/{dataset}/{sequence_set}/images/CAM_FRONT_LEFT"
        find_files_with_remainder_zero(pcdbin_folder)
        # rename_files(pcdbin_folder)

        find_files_with_remainder_zero(imageFC_folder)
        rename_files(imageFC_folder)

        find_files_with_remainder_zero(imageFR_folder)
        rename_files(imageFR_folder)

        find_files_with_remainder_zero(imageFL_folder)
        rename_files(imageFL_folder)

