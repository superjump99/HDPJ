import os

def remove_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.pcdbin'):
            try:
                file_number = int(filename.split('.')[0])
                if file_number == 0:
                    return
                if file_number % 25 != 0:
                    os.remove(os.path.join(folder_path, filename))
            except ValueError:
                continue    # file names that can't be converted to numbers are ignored
        if filename.endswith('.jpg'):
            try:
                file_number = int(filename.split('.')[0])
                if file_number % 25 != 0:
                    os.remove(os.path.join(folder_path, filename))
            except ValueError:
                continue  # file names that can't be converted to numbers are ignored
    return

def rename_files(folder_path):
    # 입력 폴더에서 파일 목록 가져오기
    file_list = os.listdir(folder_path)

    # 출력 폴더가 없으면 생성
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 파일 이름 변경 및 저장
    num = 0
    for i, old_name in enumerate(file_list):
        if old_name == 0:
            return
        # 새로운 파일 이름 생성
        if old_name.endswith('.pcdbin'):
            new_name = f"{i:06d}.pcd"

            # 입력 폴더의 파일 경로와 출력 폴더의 파일 경로 생성
            old_path = os.path.join(folder_path, old_name)
            new_path = os.path.join(folder_path, new_name)
            # 파일 이름 변경
            os.rename(old_path, new_path)

        elif old_name.endswith('jpg'):
            # num += 0.5
            new_name = f"{i:06d}.jpg"

            # 입력 폴더의 파일 경로와 출력 폴더의 파일 경로 생성
            old_path = os.path.join(folder_path, old_name)
            new_path = os.path.join(folder_path, new_name)
            # 파일 이름 변경
            os.rename(old_path, new_path)

if __name__ == '__main__':

    s3_path = 'S3_hyundai'
    step_path = 'step1'

    given_data_path = '0.given_data'
    div_remove_path = '1.div&remove'

    space = "01_Hightway"
    dataset = "HKMC-N2202209-240208"

    os.chdir('../')
    base_path = os.path.join(f"{os.getcwd()}/{s3_path}/{step_path}/")

    for i, sequence_set in enumerate(os.listdir(f"{base_path}/{div_remove_path}/{space}/{dataset}")):
        div_folder = f"{base_path}/{div_remove_path}/{space}/{dataset}/{sequence_set}"
        PCDBIN_folder = f"{div_folder}/pcd bin"
        imageFC_folder = f"{div_folder}/images/CAM_FRONT"
        imageFR_folder = f"{div_folder}/images/CAM_FRONT_RIGHT"
        imageFL_folder = f"{div_folder}/images/CAM_FRONT_LEFT"
        remove_files(PCDBIN_folder)
        # rename_files(PCDBIN_folder)

        remove_files(imageFC_folder)
        rename_files.rename_files(imageFC_folder)

        remove_files(imageFR_folder)
        rename_files.rename_files(imageFR_folder)

        remove_files(imageFL_folder)
        rename_files.rename_files(imageFL_folder)
