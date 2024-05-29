import os
import shutil
import pandas as pd
from tqdm import tqdm
import struct

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
    with open(input_file_path, 'rb') as INPUT_FILE:
        while True:
            if len(output_list) < 21:
                if len(output_list) < 16:
                    line = INPUT_FILE.read(4)
                    if not line:
                        break
                    output_list.append(struct.unpack("f", line)[0])

                elif len(output_list) < 18:
                    line = INPUT_FILE.read(2)
                    output_list.append(struct.unpack("H", line)[0])

                else:
                    line = INPUT_FILE.read(4)
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
    # 잔상으로 판별되는 layer 값 56~63 제거
    # df = df[(df['x_veh'] < 130) % (df[df['y_veh'] < 60]) & df[df['y_veh'] > -60] & (df['layer'] < 56)]
    df = df[df['y_veh'] < 60]
    df = df[df['z_veh'] > -60]
    df = df[df['layer'] < 56]
    df.reset_index(drop=True, inplace=True)
    return df


def pcdbin_to_pcd(pre_processing_done_df, output_file_path):
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

    # if the point cloud folder does not exist, make it
    # os.makedirs(pointclouds_folder, exist_ok=True)

    with open(output_file_path, 'w+') as output_file:
        output_file.write('\n'.join(header_lines) + '\n')

    for i in range(len(pre_processing_done_df)):
        table_row = table.iloc[i].tolist()
        write_line = [f"{table_row[0]} {table_row[1]} {table_row[2]} {table_row[3]}"]

        with open(output_file_path, 'a') as output_file:
            output_file.write('\n'.join(write_line) + '\n')
