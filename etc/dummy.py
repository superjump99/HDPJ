import os
import zipfile

# ZIP 파일이 있는 폴더 경로와 새로 생성할 폴더 경로를 지정합니다.
source_folder = 'C:/Users/pc/Desktop/coop-selectstar-7000527-241231/01_Label/02_PANDAR_MV/02_ParkingLot/HKMC-N2310382-240417'  # ZIP 파일이 있는 폴더
  # 여기에 기본 폴더 경로를 입력하세요

destination_folder = 'C:/Users/pc/Desktop/coop-selectstar-7000527-241231/01_Label/02_PANDAR_MV/02_ParkingLot/dum'  # 새로운 폴더를 생성할 위치
os.makedirs(destination_folder, exist_ok = True)
# 소스 폴더에서 모든 파일과 폴더 목록을 가져옵니다.
for item in os.listdir(source_folder):
    # 파일의 전체 경로를 만듭니다.
    file_path = os.path.join(source_folder, item)

    # ZIP 파일인지 확인합니다.
    if os.path.isfile(file_path) and item.lower().endswith('.zip'):
        # ZIP 파일의 이름을 추출하고 확장자를 제거합니다.
        folder_name = os.path.splitext(item)[0]

        # 새로운 폴더의 전체 경로를 만듭니다.
        new_folder_path = os.path.join(destination_folder, folder_name)

        # 새로운 폴더를 생성합니다 (이미 존재하는 경우 무시됨).
        os.makedirs(os.path.join(new_folder_path, '생산 annoations'), exist_ok=True)
        os.makedirs(os.path.join(new_folder_path, '검수 annoations'), exist_ok=True)
        print(f"폴더 '{new_folder_path}'가 생성되었습니다.")

print("모든 ZIP 파일에 대한 폴더 생성이 완료되었습니다.")