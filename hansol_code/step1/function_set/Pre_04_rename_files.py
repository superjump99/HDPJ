import os
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