import numpy as np
from function_set import GT_Box_post_processing as GTB
from function_set import GT_Property_post_processing as GTP
from function_set import TRUNCATION
import json
import pandas as pd
import os

if __name__ == '__main__':
    high_path = 'C:/Users/pc/SS-233/hyundai_code'
    step1_path = 'S3_hyundai/1.div&remove'
    step2_path = 'S3_hyundai/2.parsing_done'
    step3_path = 'S3_hyundai/3.working_done'
    step4_path = 'S3_hyundai/4.out'
    space = "00_sample"
    sequence_set = "HKMC-N2202209-240111"
    dataset = "CUBOID_TEST"
    version = '4.1.3'

    cuboid_test = "C:/Users/pc/SS-233/hyundai_code/S3_hyundai/3.working_done/CUBOID_TEST/"


    print(" 후처리 코드 실행 ")
    for folder_name in os.listdir(f"{high_path}/{step3_path}/{space}/{sequence_set}"):
        # file_name = os.listdir(f"{high_path}/{step3_path}/{space}/{sequence_set}/{folder_name}")[0][12:]
        # print(folder_name)
        # print(file_name)
        result = folder_name.split('-')
        company = result[0]
        test_car_num = result[1]
        log_start_time = "20" + result[2]
        # print(log_start_time)

        property_input_folder = f"{high_path}/{step3_path}/{space}/{sequence_set}/{folder_name}/"
        property_output_folder = f"{high_path}/{step4_path}/{space}/{sequence_set}/{folder_name}/LDR_GT_Property/"
        # print(property_output_folder)

        property_filename = f"LDR_GT_Property-{folder_name}-{version}.json"

        box_input_folder = f"{high_path}/{step3_path}/{space}/{sequence_set}/{folder_name}/annotations"
        box_output_folder = f"{high_path}/{step4_path}/{space}/{sequence_set}/{folder_name}/LDR_GT_Box"
        box_filename = f"LDR_GT_Box-{folder_name}-{version}.json"

        # TODO Property
        # 생성된 폴더 확인 및 생성
        if not os.path.exists(f"{cuboid_test}/LDR_GT_Property"):

            # 후처리 할 데이터 불러오기
            data = pd.read_excel(f"{cuboid_test}/property_data.xlsx")
            data.drop([0, 1], axis=0, inplace=True)
            data.reset_index(drop=True,inplace=True)
            # print(data.loc[0])
            # csv 파일에서 데이터
            row = data.loc[0]
            seq_data = GTP.sequence_metadata(row, version)
            sence_data = GTP.sence_curation(row)
            output_json = GTP.convert_to_new_format(seq_data, sence_data)
            # else:
            #     print("error: data[NAME] not found in 'property_data.xlsx'")
            # 파일명과 동일한 이름으로 변환된 JSON 파일 저장
            os.makedirs(f"{cuboid_test}/LDR_GT_Property")
            output_file = os.path.join(f"{cuboid_test}/LDR_GT_Property", property_filename)
            with open(output_file, 'w') as f:
                json.dump(output_json, f, indent=2)
            print(f" '{folder_name}--LDR_GT_Property' 폴더가 생성 되었습니다. ")
        else:
            print(f" '{folder_name}--LDR_GT_Property' 폴더는 이미 생성 되었습니다. ")
        # TODO BOX
        # 생성된 폴더 확인 및 생성
        if not os.path.exists(f"{cuboid_test}/LDR_GT_BO1"):
            field = np.array([(-1, 0), (20, 50), (120, 50), (120, -50), (20, -50), (-1, 0)])

            # 입력 폴더 내의 모든 JSON 파일 목록 가져오기
            json_files = [f for f in os.listdir(f"{cuboid_test}/annotations") if f.endswith('.json')]

            output_json = {"FRAME_LIST": []}
            for idx,json_file in enumerate(json_files):

                pcdfilenum = int(json_file[:6])
                df = TRUNCATION.load_json_annotations(os.path.join(f"{cuboid_test}/annotations", json_file))
                truncation_df = TRUNCATION.truncation(field, df)
                # print(truncation_df)
                # 후처리 함수
                frame_metadata = GTB.change_frame_metadata(idx+1, pcdfilenum, log_start_time)
                # print(frame_metadata)
                object_list = GTB.change_object_list(truncation_df)
                # print(object_list)
                frame = GTB.frames(object_list, frame_metadata)
                output_json['FRAME_LIST'].append(frame)

            # 파일명과 동일한 이름으로 변환된 JSON 파일 저장
            output_file = os.path.join(f"{cuboid_test}/LDR_GT_BOX123", box_filename)
            os.makedirs(f"{cuboid_test}/LDR_GT_BOX123")
            with open(output_file, 'w') as f:
                json.dump(output_json, f, indent=2)
            print(f" '{folder_name}--LDR_GT_BOX' 폴더가 생성 되었습니다. ")

        else:
            print(f" '{folder_name}--LDR_GT_BOX' 폴더는 이미 생성 되었습니다. ")
    print(" 후처리 코드 종료 ")
