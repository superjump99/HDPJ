from S3_hyundai.hansol_code.step1.function_set import preprocess
from tqdm import tqdm
import os

if __name__ == '__main__':

    print("🤍🤍🤍 파싱 및 전처리 코드 실행 🤍🤍🤍")
    path = "/"
    dataset = 'HKMC-N2202209-240220'
    given_pcd_folder = f"{path}/S3_hyundai/0.given_data/{dataset}/LDR_Raw_PCD"
    given_image_folder = f"{path}/S3_hyundai/0.given_data/{dataset}/LDR_Raw_Image"
    working_folder = f"{path}/S3_hyundai/1.working/"

    # 파싱 및 전처리
    for sequence in os.listdir(given_pcd_folder):
        pcdbin_folder = f"{given_pcd_folder}/{sequence}/"
        # print(pcdbin_folder)
        # 작업 툴 필요 폴더 생성
        annotation_folder = working_folder + f"{sequence[12:]}/annotations/"
        pcd_folder = working_folder +f"{sequence[12:]}/pointclouds/"
        # pcd_w_g_folder = working_folder+ f"{folder}/pointclouds_without_ground/"

        # pcd 폴더 생성 (폴더가 이미 만들 어져 있거나, 로우 데이터에 pcdbin 파일이 없으면 폴더 생성 하지 않음)
        if not os.path.exists(working_folder + sequence[12:]):
            os.makedirs(working_folder + sequence[12:])
            os.makedirs(pcd_folder)
            os.makedirs(annotation_folder)
            preprocess.create_image_folder(dataset, sequence[12:])
            # shutil.copy("C:/Users/pc/SS-233/23-ds-041/S3_hyundai/hansol_code/property_data.xlsx",working_folder + sequence[12:] + "/property_data.xlsx")

            # download 한 pcdbin 파일 개수 만큼 반복
            print(f"💿💿💿 '{sequence[12:]}' 데이터 파싱 및 전처리 중 💿💿💿")
            for pcdbin_file in tqdm(os.listdir(pcdbin_folder)):
                input_file_path = os.path.join(pcdbin_folder, pcdbin_file)
                output_file_path = os.path.join(pcd_folder, os.path.splitext(pcdbin_file)[0] + ".pcd")

                # pcdbin parsing
                parsing_result = preprocess.pcdbin_parser(input_file_path, sequence[12:])

                preprocess.data_preprocesser(parsing_result, output_file_path)
            print(f"✅✅ '{sequence[12:]}' 데이터 파싱 및 전처리 완료 ✅✅")


            # mk_json for recode bbox
            # TODO : 인준님이 자동 생성으로 만들어 주심
            # preprocess.create_json_files(pcd_folder, annotation_folder)
            print(f"🆕🆕🆕 '{sequence[12:]}' 폴더 생성 되었습니다. 🆕🆕🆕")
            break
        else:
            print(f"❗❗❗ '{sequence[12:]}' 폴더는 이미 생성 되었습니다. ❗❗❗")
print("🤍🤍🤍 파싱 및 전처리 코드 종료 🤍🤍🤍")
