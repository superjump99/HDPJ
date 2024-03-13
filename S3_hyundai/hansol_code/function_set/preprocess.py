import os
import shutil
import struct
import pandas as pd
import json

def pcdbin_parser(input_file_path,seq):
    field = ["x_veh", "y_veh", "z_veh", "range_veh", "azi_veh", "ele_veh",
             "x", "y", "z", "range", "azi", "ele",
             "x_yaw_only", "y_yaw_only", "azi_yaw_only",
             "intensity", "layer", "echo",
             "firing_idx", "timestamp", "sensor"]
    field = ["x_veh", "y_veh", "z_veh",
             "x", "y", "z",
             "intensity", "lidar_idx", "row",
             "azi", "range", "echo"]

    df_list = []
    output_list = []
    with open(input_file_path, 'rb') as input_file:
        while True:
            if len(output_list) < 21:
                if len(output_list) < 16:
                    line = input_file.read(4)
                    if not line:
                        break
                    output_list.append(struct.unpack("f", line)[0])
                    # print(struct.unpack("f", line)[0])

                # elif len(output_list) < 18:
                #     line = input_file.read(2)
                #     output_list.append(struct.unpack("H", line)[0])
                #
                # else:
                #     line = input_file.read(4)
                #     output_list.append(struct.unpack_from("L", line)[0])
            else:
                df_list.append(output_list)
                output_list = []
        parsing_df = pd.DataFrame(df_list,columns=field)
        # print(parsing_df)
        # parsing_df.to_csv(f'{seq}.csv')

        # exit()
        # # parsing_df.to_csv('000061.csv')
        # # TODO ROI 관련 범위 종방향 0 < x < 120m, 횡방향 -50 < y < 50m
        parsing_df = parsing_df[parsing_df['x'] < 130]
        parsing_df = parsing_df[parsing_df['y'] < 60]
        parsing_df = parsing_df[parsing_df['y'] > -60]
        #
        #
        # # 잔상으로 판별되는 layer 값 56~63 제거
        # parsing_df = parsing_df[parsing_df['layer']<56]
        # parsing_df.reset_index(drop=True,inplace=True)
        # # parsing_df.to_csv('del_x_y.csv')

        # print("데이터 개수 : ", len(parsing_df))
    return parsing_df

def data_preprocesser(parsing_df, output_file_path):
    header_lines = [
            "VERSION .7",
            "FIELDS x y z intensity",
            "SIZE 4 4 4 4",
            "TYPE F F F F",
            "COUNT 1 1 1 1",
            f"WIDTH {len(parsing_df)}",
            "HEIGHT 1",
            "VIEWPOINT 0 0 0 1 0 0 0",
            f"POINTS {len(parsing_df)}",
            "DATA ascii"]

    # 6:x,7:y,8:z
    table = parsing_df.iloc[:, [3, 4, 5, 6]]
    print(table)
    with open(output_file_path, 'w+') as output_file:
        output_file.write('\n'.join(header_lines) + '\n')
    # table = parsing_df.iloc[:, [7, 6, 8, 15]]

    for i in range(len(parsing_df)):
        table_row = table.iloc[i].tolist()
        # print(table_row)
        # wirte_line = [f"{table_row[0]*-1} {table_row[1]} {table_row[2]} {table_row[3]}"]
        wirte_line = [f"{table_row[0]} {table_row[1]} {table_row[2]} {table_row[3]}"]

        with open(output_file_path, 'a') as output_file:
            output_file.write('\n'.join(wirte_line) + '\n')

def create_json_files(source_folder, target_folder):
    # 소스 폴더에서 파일 목록을 가져옴
    file_list = os.listdir(source_folder)

    # 타겟 폴더가 없다면 생성
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # 파일 개수만큼 반복하여 JSON 파일 생성
    for file_name in file_list:
        # JSON 파일 이름 생성
        json_file_name = os.path.join(target_folder, file_name.split(".")[0] + ".json")

        # JSON 파일에 저장할 데이터 생성 (예시로 파일 이름과 경로를 저장)
        data_to_save = {}

        # JSON 파일 생성 및 데이터 저장
        with open(json_file_name, 'w') as json_file:
            json.dump(data_to_save, json_file, indent=4)

def create_image_folder(folder, folder_name):
    print(f"🖼️ '{folder}' 데이터 이미지 복사 중 🖼️")
    source_folder = f"C:/Users/pc/SS-233/23-ds-041/S3_hyundai/0.given_data/{folder}/LDR_Raw_Image/LDR_Raw_Image-{folder_name}/ImageFC"
    target_folder = f"C:/Users/pc/SS-233/23-ds-041/S3_hyundai/1.working/{folder_name}/images/CAM_FRONT"
    shutil.copytree(source_folder, target_folder)
    source_folder = f"C:/Users/pc/SS-233/23-ds-041/S3_hyundai/0.given_data/{folder}/LDR_Raw_Image/LDR_Raw_Image-{folder_name}/ImageFL"
    target_folder = f"C:/Users/pc/SS-233/23-ds-041/S3_hyundai/1.working/{folder_name}/images/CAM_FRONT_LEFT"
    shutil.copytree(source_folder, target_folder)
    source_folder = f"C:/Users/pc/SS-233/23-ds-041/S3_hyundai/0.given_data/{folder}/LDR_Raw_Image/LDR_Raw_Image-{folder_name}/ImageFR"
    target_folder = f"C:/Users/pc/SS-233/23-ds-041/S3_hyundai/1.working/{folder_name}/images/CAM_FRONT_RIGHT"
    shutil.copytree(source_folder, target_folder)
    print(f"✅️ '{folder}' 데이터 이미지 복사 완료 ✅️")



if __name__ == "__main__":
    """
    0.given_data에 있는 현대차에서 제공한 raw 데이터 시퀀스 파일 말다 실행
    """
    for filename in os.listdir(f"C:/Users/pc/SS-233/23-ds-041/S3_hyundai/1.working"):
        input_folder = f"C:/Users/pc/SS-233/23-ds-041/S3_hyundai/0.given_data/{filename}/LDR_RAW_PCD/LDR_RAW_PCD-HKMC-N2202209-240111142349-RFFR_LDL-0.0.0.1.0-RFFR_LDR-1/"
        work_folder = f"C:/Users/pc/SS-233/23-ds-041/S3_hyundai/1.working/{filename}/pointclouds/"
        annotation_folder = f"C:/Users/pc/SS-233/23-ds-041/S3_hyundai/1.working/{filename}/annotations/"

        # pcd 폴더 생성 (이미 만들 어져 있으면 파일 생성하지 않음)
        if not os.path.exists(work_folder):
            os.mkdir(work_folder)

            # download 한 pcdbin 파일 개수 만큼 반복
            for filename in os.listdir(input_folder):
                if filename.endswith(".pcdbin"):
                    input_file_path = os.path.join(input_folder, filename)
                    output_file_path = os.path.join(work_folder, os.path.splitext(filename)[0] + ".pcd")

                # pcdbin parsing
                parsing_result = pcdbin_parser(input_file_path)
                # print(f'{filename} Parsing Done')

                # preprocessing after parsing
                data_preprocesser(parsing_result, output_file_path)
                # print(f'{filename} Pre_processing Done')

            source_folder_path = work_folder
            target_folder_path = annotation_folder
            create_json_files(source_folder_path, target_folder_path)
        # print(f'-------{filename=} Parsing & Preprocessing Done -----------------')