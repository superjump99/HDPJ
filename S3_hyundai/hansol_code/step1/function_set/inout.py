# from function_set import preprocess
from tqdm import tqdm
import shutil
import os

if __name__ == '__main__':
    print("🤍🤍🤍 파싱 및 전처리 코드 실행 🤍🤍🤍")

    dataset = 'HKMC-N2202209-240220'
    given_pcd_folder = f"C:/Users/pc/SS-233/23-ds-041/S3_hyundai/0.given_data/{dataset}/LDR_Raw_PCD"
    given_image_folder = f"C:/Users/pc/SS-233/23-ds-041/S3_hyundai/0.given_data/{dataset}/LDR_Raw_Image"
    working_folder = f"C:/Users/pc/SS-233/23-ds-041/S3_hyundai/1.working/"

    # 파싱 및 전처리
    for folder in os.listdir(given_pcd_folder):
        print(folder)