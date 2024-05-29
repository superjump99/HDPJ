import numpy as np
import json
import pandas as pd
import os
from datetime import date
from function_set import Post_BOX as BOX, Post_TRUNCATION as TRUNCATION
from function_set import Post_PROPERTY as PROPERTY

if __name__ == '__main__':
    version = '4.1.3'

    road = ['01_Highway', '03_Urban']
    space = road[0]

    bucket_name = 'coop-selectstar-7000527-241231/'
    step_list = ['', '01_Label/', '02_Inspection/']
    sensor_list = ['', '01_IRIS_JX013/', '02_PANDAR_MV/']
    space_list = ['', '01_Highway/', '02_ParkingLot/', '03_Urban/']

    step = step_list[1]
    sensor = sensor_list[2]
    space = space_list[1]

    # STEP 1: Set base file
    middle_folder_name = os.listdir(f'{os.getcwd()}/{bucket_name}/{step}/{sensor}/{space}/')[0]
    base_path = os.path.join(f'{os.getcwd()}/{bucket_name}/{step}/{sensor}/{space}/{middle_folder_name}')
    DATA_path = os.path.join(base_path, 'DATA')

    for sequence_set in os.listdir(f"{DATA_path}"):
        result = sequence_set.split('-')
        log_start_time = "20" + result[2]

        property_json = f"{date.today()}-LDR_GT_Property-{sequence_set}-{version}.json"
        box_json = f"{date.today()}-LDR_GT_Box-{sequence_set}-{version}.json"

        # TODO Property
        # 생성된 폴더 확인 및 생성
        if not os.path.exists(f"{base_path}/LDR_GT_Property/{sequence_set}/{property_json}"):
            # STEP 1. ROAD PROPERTY DATA
            data = pd.read_excel(f"{DATA_path}/{sequence_set}/{sequence_set}.xlsx")

            # STEP 2. Delete unnecessary index
            data.drop([0, 1], axis=0, inplace=True)
            data.reset_index(drop=True, inplace=True)

            # STEP 3. Data frame to json
            row = data.loc[0]
            seq_data = PROPERTY.sequence_metadata(row, version)
            scene_data = PROPERTY.scene_curation(row)
            output_json = PROPERTY.convert_to_new_format(seq_data, scene_data)

            # STEP 4. Save json file
            output_file_path = os.path.join(f"{base_path}/LDR_GT_Property/{sequence_set}", property_json)
            with open(output_file_path, 'w') as f:
                json.dump(output_json, f, indent=2)

            print(f" [{sequence_set}--LDR_GT_Property] 폴더가 생성 되었습니다. ")
        else:
            print(f" [{sequence_set}--LDR_GT_Property] 폴더는 이미 생성 되었습니다. ")

        # TODO BOX
        # 생성된 폴더 확인 및 생성
        if not os.path.exists(f"{base_path}/LDR_GT_BOX/{sequence_set}/{box_json}"):
            field = np.array([(-1, 0), (20, 50), (120, 50), (120, -50), (20, -50), (-1, 0)])

            # 입력 폴더 내의 모든 JSON 파일 목록 가져오기
            annotation_json = [f for f in os.listdir(f"{DATA_path}/{sequence_set}/annotations")
                          if f.endswith('.json')]
            output_json = {"FRAME_LIST": []}
            n = 0
            for idx, annotation in enumerate(annotation_json):
                filenum = int(annotation[:6])
                if filenum % 2 == 1:
                    n += 1

                    df = TRUNCATION.load_json_annotations(
                        os.path.join(f"{DATA_path}/{sequence_set}/annotations", annotation))
                    truncation_df = TRUNCATION.truncation(field, df)

                    # 후처리 함수
                    frame_metadata = BOX.change_frame_metadata(n, filenum, log_start_time)
                    object_list = BOX.change_object_list(truncation_df)
                    frame = BOX.frames(object_list, frame_metadata)
                    output_json['FRAME_LIST'].append(frame)

            # 파일명과 동일한 이름으로 변환된 JSON 파일 저장
            output_file_path = os.path.join(f"{base_path}/LDR_GT_BOX/{sequence_set}", box_json)
            # os.makedirs(f"{base_path}/{working_done_path}/{space}/{dataset}/{folder_name}/LDR_GT_BOX")
            with open(output_file_path, 'w') as f:
                json.dump(output_json, f, indent=2)

            print(f" [{sequence_set}-LDR_GT_BOX] 폴더가 생성 되었습니다.")

        else:
            print(f" [{sequence_set}-LDR_GT_BOX] 폴더는 이미 생성 되었습니다. ")
    print(" 후처리 코드 종료 ")
