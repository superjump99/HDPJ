import os

def remove_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.pcdbin'):
            try:
                file_number = int(filename.split('.')[0])
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
    for i, old_name in enumerate(file_list):
        if old_name == 0:
            return

        if old_name.endswith('.pcdbin'):
            new_name = f"{i:06d}.pcd"

            old_path = os.path.join(folder_path, old_name)
            new_path = os.path.join(folder_path, new_name)

            os.rename(old_path, new_path)

        elif old_name.endswith('jpg'):
            new_name = f"{i:06d}.jpg"

            old_path = os.path.join(folder_path, old_name)
            new_path = os.path.join(folder_path, new_name)

            os.rename(old_path, new_path)
