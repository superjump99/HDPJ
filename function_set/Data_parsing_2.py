import os
import pandas as pd
import struct
import numpy as np
from tqdm import tqdm

# TODO 데이터 파싱
def pcdbin_parser(input_file_path):
    field = ["x_veh", "y_veh", "z_veh",
             "range_veh", "azi_veh", "ele_veh",
             "x", "y", "z",
             "range", "azi", "ele",
             "x_yaw_only", "y_yaw_only", "azi_yaw_only",
             "intensity", "layer", "echo",
             "firing_idx", "timestamp", "sensor"]

    # 파일 전체 크기를 얻어옵니다.
    file_size = os.path.getsize(input_file_path)

    # 미리 고정된 크기만큼 파일을 읽어 들입니다.
    record_size = 16 * 4 + 2 * 2 + 3 * 4  # float 16개, uint16 2개, uint32 3개
    num_records = file_size // record_size

    data = []

    with open(input_file_path, 'rb') as INPUT_FILE:
        for _ in tqdm(range(num_records), desc="Parsing binary file"):
            record = INPUT_FILE.read(record_size)
            parsed_record = struct.unpack("16f 2H 3L", record)
            data.append(parsed_record)

    parsing_df = pd.DataFrame(data, columns=field)
    pre_processing_done_df = pre_process(parsing_df)
    return pre_processing_done_df

# TODO Preprocessing
def pre_process(df):
    # ROI 관련 범위 종방향 0 < x < 120m, 횡방향 -50 < y < 50m
    # 잔상으로 판별되는 layer 값 56~63 제거
    df = df[(df['x_veh'] < 130) & (df['y_veh'] < 60) & (df['y_veh'] > -60)]
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

    with open(output_file_path, 'w') as output_file:
        output_file.write('\n'.join(header_lines) + '\n')

    # numpy를 사용하여 더 빠르게 파일에 쓰기
    np.savetxt(output_file_path, table.values, fmt='%f', delimiter=' ', header='', comments='', newline='\n', append=True)

# 테스트
if __name__ == "__main__":
    input_file = "path/to/your/input/file.pcd"
    output_file = "path/to/your/output/file.pcd"
    parsed_df = pcdbin_parser(input_file)
    pcdbin_to_pcd(parsed_df, output_file)