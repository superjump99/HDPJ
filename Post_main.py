import numpy as np
import json
import pandas as pd
import os
from datetime import date
from function_set import Post_BOX as BOX, Post_TRUNCATION as TRUNCATION
from function_set import Post_PROPERTY as PROPERTY

if __name__ == '__main__':
    HDC_path = os.getcwd()
    version = '4.1.3'
    bucket_name = 'coop-selectstar-7000527-241231/'
    step = '01_Label/'

    ''' :parameter
        step
            :param  
            '01_Label/'
            '02_Inspection/'
        sensor
            :param
            '01_IRIS_JX013/'
            '02_PANDAR_MV/'
        space
            :param
            '01_Highway/'
            '02_ParkingLot/'
            '03_Urban/'
    '''

    sensor = '01_IRIS_JX013'
    space = '01_Highway'

    # STEP 1: Set base file
    # middle_folder_name = os.listdir(f'{HDC_path}/{bucket_name}/{step}/{sensor}/{space}/')[0]
    # base_path = os.path.join(f'{HDC_path}/{bucket_name}/{step}/{sensor}/{space}/{middle_folder_name}')
    # DATA_path = os.path.join(base_path, 'DATA')
    tool_path = 'c:/Users/pc/hyundai/input/HYUNDAI/'
    os.chdir(tool_path)

    # 저장 경로 탐색
    for sequence_set in os.listdir(f"{tool_path}"):
        print(sequence_set)
        for file in os.listdir(f"{tool_path}/{sequence_set}"):
            if file.endswith('.txt'):
                print(file)
                sensor_space = file.split('_')[0]
                sensor = sensor_space.split('-')[0]
                space = sensor_space.split('-')[1]
                if sensor.lower() == 'iris':
                    sensor = '01_IRIS_JX013'
                else:
                    sensor = '02_PANDAR_MV'

                if space.lower() == 'highway':
                    space = '01_Highway'
                elif space.lower() == 'parkinglot':
                    space = '02_ParkingLot'
                else:
                    space = '03_Urban'
        middle_folder_name = os.listdir(f'{HDC_path}/{bucket_name}/{step}/{sensor}/{space}/')[0]
        base_path = os.path.join(f'{HDC_path}/{bucket_name}/{step}/{sensor}/{space}/{middle_folder_name}')

        result = sequence_set.split('-')
        log_start_time = "20" + result[2]

        property_json = f"LDR_GT_Property-{sequence_set}-{version}.json"
        box_json = f"LDR_GT_Box-{sequence_set}-{version}.json"

        # TODO Property
        # 생성된 폴더 확인 및 생성
        if not os.path.exists(f"{base_path}/LDR_GT_Property/{property_json}"):
            # STEP 1. ROAD PROPERTY DATA
            data = pd.read_excel(f"{tool_path}/{sequence_set}/property_data.xlsx")

            # STEP 2. Delete unnecessary index
            data.drop([0, 1], axis=0, inplace=True)
            data.reset_index(drop=True, inplace=True)

            # STEP 3. Data frame to json
            row = data.loc[0]
            seq_data = PROPERTY.sequence_metadata(row, version)
            scene_data = PROPERTY.scene_curation(row)
            output_json = PROPERTY.convert_to_new_format(seq_data, scene_data)

            # STEP 4. Save json file
            output_file_path = os.path.join(f"{base_path}/LDR_GT_Property/")
            if not os.path.exists(output_file_path): os.makedirs(output_file_path)

            save_path = os.path.join(output_file_path, property_json)
            # print(os.path.join(output_file_path, property_json))
            with open(save_path, 'w') as f:
                json.dump(output_json, f, indent=4)

            print(f"[{property_json}] 파일이 생성 되었습니다. ")
        else:
            print(f"[{property_json}] 파일이 이미 존재합니다. ")

        # TODO BOX
        # 생성된 폴더 확인 및 생성
        if not os.path.exists(f"{base_path}/LDR_GT_Point/{box_json}"):
            field = np.array([(-1, 0), (20, 50), (120, 50), (120, -50), (20, -50), (-1, 0)])

            # 입력 폴더 내의 모든 JSON 파일 목록 가져오기
            annotation_json = [f for f in os.listdir(f"{tool_path}/{sequence_set}/annotations")
                          if f.endswith('.json')]
            output_json = {"FRAME_LIST": []}
            n = 0
            for idx, annotation in enumerate(annotation_json):
                filenum = int(annotation[:6])
                if filenum % 2 == 1:
                    n += 1

                    df = TRUNCATION.load_json_annotations(
                        os.path.join(f"{tool_path}/{sequence_set}/annotations", annotation))
                    truncation_df = TRUNCATION.truncation(field, df)

                    # 후처리 함수
                    frame_metadata = BOX.change_frame_metadata(n, filenum, log_start_time)
                    object_list = BOX.change_object_list(truncation_df)
                    frame = BOX.frames(object_list, frame_metadata)
                    output_json['FRAME_LIST'].append(frame)

            # 파일명과 동일한 이름으로 변환된 JSON 파일 저장
            output_file_path = os.path.join(f"{base_path}/LDR_GT_Point/")
            if not os.path.exists(output_file_path): os.path.exists(output_file_path)
            save_path = os.path.join(output_file_path, box_json)

            with open(save_path, 'w') as f:
                json.dump(output_json, f, indent=2)

            print(f"[{box_json}] 파일이 생성 되었습니다.")

        else:
            print(f"[{box_json}] 파일이 이미 존재합니다. ")
    print(" 후처리 코드 종료 ")
