import os
import shutil
import pandas as pd
from tqdm import tqdm
import struct
import Pre_04_rename_files as rename_files

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

    s3_path = 'S3_hyundai'
    step_path = 'step1'

    given_data_path = '0.given_data'
    div_remove_path = '1.div&remove'
    parsing_done_path = '2.parsing_done'

    space = "01_Hightway"
    dataset = "HKMC-N2202209-240208"

    os.chdir('../../../')
    base_path = os.path.join(f"{os.getcwd()}/{s3_path}/{step_path}/")

    for sequence_set in os.listdir(f"{base_path}/{div_remove_path}/{space}/{dataset}/"):
        annotation_folder = f"{base_path}/{div_remove_path}/{space}/{dataset}/{sequence_set}/annotations/"

        if not os.path.exists(annotation_folder):
            PCDBIN_folder = f"{base_path}/{div_remove_path}/{space}/{dataset}/{sequence_set}/pcd bin/"
            pointclouds_folder = f"{base_path}/{div_remove_path}/{space}/{dataset}/{sequence_set}/pointclouds/"

            for PCDBIN_file in tqdm(os.listdir(PCDBIN_folder)):
                input_file = os.path.join(PCDBIN_folder, PCDBIN_file)
                output_file = os.path.join(pointclouds_folder, os.path.splitext(PCDBIN_file)[0] + ".pcd")

                pre_processing_done_df = pcdbin_parser(input_file)
                pcdbin_to_pcd(pre_processing_done_df, pointclouds_folder, output_file)

            os.makedirs(annotation_folder)

            print(f" Success [작업 가능 폴더 생성 완료]", sequence_set)

        else:
            print(f"Error [이미 폴더 생성 완료]", sequence_set)

    for i, sequence_set in enumerate(os.listdir(f"{base_path}/{div_remove_path}/{space}/{dataset}")):
        PCDBIN_folder = f"{base_path}/{div_remove_path}/{space}/{dataset}/{sequence_set}/pcd bin"
        pointclouds_folder = f"{base_path}/{div_remove_path}/{space}/{dataset}/{sequence_set}/pointclouds"

        rename_files.rename_files(pointclouds_folder)

        if os.path.exists(PCDBIN_folder):
            shutil.rmtree(PCDBIN_folder)

        shutil.make_archive(f"{base_path}/{div_remove_path}/{space}/{dataset}/{sequence_set}",
                            'zip', root_dir=f"{base_path}/{parsing_done_path}/{space}/{dataset}/{sequence_set}")
