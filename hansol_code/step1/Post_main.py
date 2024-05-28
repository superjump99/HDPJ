import numpy as np
import json
import pandas as pd
import os
from datetime import datetime
from hansol_code.step1.function_set import Post_BOX as BOX, Post_PROPERTY as PROPERTY, Post_TRUNCATION as TRUNCATION

if __name__ == '__main__':
    version = '4.1.3'
    s3_path = 'S3_hyundai'
    step_path = 'step1'
    given_data_path = '0.given_data'
    div_remove_path = '1.div&remove'
    parsing_done_path = '2.parsing_done'
    working_done_path = '3.working_done'
    out_path = '4.out'

    road = ['01_Highway', '03_Urban']
    space = road[0]

    os.chdir('../../')
    base_path = os.path.join(f"{os.getcwd()}/{s3_path}/{step_path}/")

    dataset = os.listdir(f"{base_path}/{working_done_path}/{space}/")[0]


    today = (str(datetime.today().year)[2:] + str(datetime.today().month).zfill(2) +
             str(datetime.today().day).zfill(2))

    for folder_name in os.listdir(f"{base_path}/{working_done_path}/{space}/{dataset}"):
        result = folder_name.split('-')
        company = result[0]
        test_car_num = result[1]
        log_start_time = "20" + result[2]

        property_filename = f"LDR_GT_Property-{folder_name}-{version}.json"
        box_filename = f"LDR_GT_Box-{folder_name}-{version}.json"

        # TODO Property
        # 생성된 폴더 확인 및 생성
        if not os.path.exists(f"{base_path}/{working_done_path}/{space}/{dataset}/{folder_name}/LDR_GT_Property"):

            # 후처리 할 데이터 불러오기
            data = pd.read_excel(f"{base_path}/{working_done_path}/{space}/{dataset}/{folder_name}/property_data.xlsx")
            data.drop([0, 1], axis=0, inplace=True)
            data.reset_index(drop=True, inplace=True)

            # csv 파일에서 데이터
            row = data.loc[0]
            seq_data = PROPERTY.sequence_metadata(row, version)
            sence_data = PROPERTY.sence_curation(row)
            output_json = PROPERTY.convert_to_new_format(seq_data, sence_data)
            # print(output_json)
            # 파일명과 동일한 이름으로 변환된 JSON 파일 저장
            os.makedirs(f"{base_path}/{working_done_path}/{space}/{dataset}/{folder_name}/"
                        f"LDR_GT_Property")

            output_file = os.path.join(f"{base_path}/{working_done_path}/{space}/{dataset}/{folder_name}/"
                                       f"LDR_GT_Property", property_filename)

            with open(output_file, 'w') as f:
                json.dump(output_json, f, indent=2)
            print(f" [{folder_name}--LDR_GT_Property] 폴더가 생성 되었습니다. ")
        else:
            print(f" [{folder_name}--LDR_GT_Property] 폴더는 이미 생성 되었습니다. ")

        # TODO BOX
        # 생성된 폴더 확인 및 생성
        if not os.path.exists(f"{base_path}/{working_done_path}/{space}/{dataset}/{folder_name}/LDR_GT_BOX"):
            field = np.array([(-1, 0), (20, 50), (120, 50), (120, -50), (20, -50), (-1, 0)])

            # 입력 폴더 내의 모든 JSON 파일 목록 가져오기
            json_files = [f for f in os.listdir(f"{base_path}/{working_done_path}/{space}/{dataset}/{folder_name}/annotations")
                          if f.endswith('.json')]
            output_json = {"FRAME_LIST": []}
            n = 0
            for idx, json_file in enumerate(json_files):
                pcdfilenum = int(json_file[:6])
                if pcdfilenum % 2 ==1:
                    n += 1

                    df = TRUNCATION.load_json_annotations(
                        os.path.join(f"{base_path}/{working_done_path}/{space}/{dataset}/{folder_name}/annotations", json_file))
                    truncation_df = TRUNCATION.truncation(field, df)

                    # 후처리 함수
                    frame_metadata = BOX.change_frame_metadata(n, pcdfilenum, log_start_time)
                    object_list = BOX.change_object_list(truncation_df)
                    frame = BOX.frames(object_list, frame_metadata)
                    output_json['FRAME_LIST'].append(frame)
    #
            # 파일명과 동일한 이름으로 변환된 JSON 파일 저장
            output_file = os.path.join(f"{base_path}/{working_done_path}/{space}/{dataset}/{folder_name}/LDR_GT_BOX", box_filename)
            os.makedirs(f"{base_path}/{working_done_path}/{space}/{dataset}/{folder_name}/LDR_GT_BOX")
            with open(output_file, 'w') as f:
                json.dump(output_json, f, indent=2)
            print(f" [{folder_name}--{today}-LDR_GT_BOX] 폴더가 생성 되었습니다. ")

        else:
            print(f" [{folder_name}--LDR_GT_BOX] 폴더는 이미 생성 되었습니다. ")
    print(" 후처리 코드 종료 ")
