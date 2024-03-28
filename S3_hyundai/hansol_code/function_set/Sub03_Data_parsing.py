import os
import shutil

from tqdm import tqdm
import struct
import pandas as pd

# TODO 데이터 파싱
def pcdbin_parser(input_file_path):
    field = ["x_veh", "y_veh", "z_veh",
             "range_veh", "azi_veh", "ele_veh",
             "x", "y", "z",
             "range", "azi", "ele",
             "x_yaw_only", "y_yaw_only", "azi_yaw_only",
             "intensity", "layer", "echo",
             "firing_idx", "timestamp", "sensor"]

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

                elif len(output_list) < 18:
                    line = input_file.read(2)
                    output_list.append(struct.unpack("H", line)[0])

                else:
                    line = input_file.read(4)
                    output_list.append(struct.unpack_from("L", line)[0])
            else:
                df_list.append(output_list)
                output_list = []
        parsing_df = pd.DataFrame(df_list, columns=field)
        pre_processing_done_df = pre_process(parsing_df)
        return pre_processing_done_df
# TODO Preprocessing
def pre_process(df):
    # ROI 관련 범위 종방향 0 < x < 120m, 횡방향 -50 < y < 50m
    df = df[df['x_veh'] < 130]
    df = df[df['y_veh'] < 60]
    df = df[df['z_veh'] > -60]

    # 잔상으로 판별되는 layer 값 56~63 제거
    df = df[df['layer'] < 56]
    df.reset_index(drop=True, inplace=True)
    return df

def pcdbin_to_pcd(pre_processing_done_df, pointclouds_folder, output_file_path):
    header_lines = [
            "VERSION .7",
            "FIELDS x y z intensity",
            "SIZE 4 4 4 4",
            "TYPE F F F F",
            "COUNT 1 1 1 1",
            f"WIDTH {len(pre_processing_done_df)}",
            "HEIGHT 1",
            "VIEWPOINT 0 0 0 1 0 0 0",
            f"POINTS {len(pre_processing_done_df)}",
            "DATA ascii"]

    #  TODO 0:x_veh, 1:y_veh, 2:z_veh, 14:intensity
    table = pre_processing_done_df.iloc[:, [0, 1, 2, 15]]
    if not os.path.exists(pointclouds_folder):
        os.makedirs(pointclouds_folder)
    with open(output_file_path, 'w+') as output_file:
        output_file.write('\n'.join(header_lines) + '\n')

    for i in range(len(pre_processing_done_df)):
        table_row = table.iloc[i].tolist()
        write_line = [f"{table_row[0]} {table_row[1]} {table_row[2]} {table_row[3]}"]

        with open(output_file_path, 'a') as output_file:
            output_file.write('\n'.join(write_line) + '\n')


if __name__ == '__main__':

    high_path = 'C:/Users/pc/SS-233/hyundai_code'
    step1_path = 'S3_hyundai/1.div&remove'
    step2_path = 'S3_hyundai/2.parsing_done'
    space = "03_Urban"
    dataset = "HKMC-N2202209-240220"

    for sequence_set in os.listdir(f"{high_path}/{step1_path}/{space}/{dataset}/"):
        annotation_folder = f"{high_path}/{step1_path}/{space}/{dataset}/{sequence_set}/annotations/"

        if not os.path.exists(annotation_folder):
            pcdbin_folder = f"{high_path}/{step1_path}/{space}/{dataset}/{sequence_set}/pcdbin/"
            pointclouds_folder = f"{high_path}/{step1_path}/{space}/{dataset}/{sequence_set}/pointclouds/"

            for pcdbin_file in tqdm(os.listdir(pcdbin_folder)):
                input_file = os.path.join(pcdbin_folder, pcdbin_file)
                output_file = os.path.join(pointclouds_folder, os.path.splitext(pcdbin_file)[0] + ".pcd")

                pre_processing_done_df = pcdbin_parser(input_file)
                pcdbin_to_pcd(pre_processing_done_df, pointclouds_folder, output_file)

            os.makedirs(annotation_folder)

            print(f" Success [작업 가능 폴더 생성 완료]", sequence_set)

        else:
            print(f"Error [이미 폴더 생성 완료]", sequence_set)
    # if not os.path.exists(f"{high_path}/{step2_path}/"):
    #     os.makedirs(f"{high_path}/{step2_path}/")

    # shutil.move(f"{high_path}/{step1_path}/{space}/",f"{high_path}/{step2_path}/{space}/")