import os
import shutil

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
    high_path = '/'
    given_path = 'S3_hyundai/0.given_data'
    step1_path = 'S3_hyundai/1.div&remove'
    space = "03_Urban"
    dataset = "HKMC-N2202209-240220"

    for i, sequence_set in enumerate(os.listdir(f"{high_path}/{step1_path}/{space}/{dataset}")):

        pointclouds_folder = f"{high_path}/{step1_path}/{space}/{dataset}/{sequence_set}/pointclouds"
        pcdbin_folder = f"{high_path}/{step1_path}/{space}/{dataset}/{sequence_set}/pcdbin"

        rename_files(pointclouds_folder)

        if os.path.exists(pcdbin_folder):
            shutil.rmtree(pcdbin_folder)

        shutil.make_archive(f"{high_path}/{step1_path}/{space}/{dataset}/{sequence_set}",
                            'zip', root_dir=f"{high_path}/{step1_path}/{space}/{dataset}/{sequence_set}")
