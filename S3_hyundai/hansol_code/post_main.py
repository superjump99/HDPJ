from function_set import GT_Box_post_processing as GTB
from function_set import GT_Property_post_processing as GTP
import json
import pandas as pd
import os


if __name__ == '__main__':
    path = "C:/Users/pc/SS-233/hyundai_code"
    version = "4.1.3"
    print("💛💛💛 후처리 코드 실행 💛💛💛")
    for folder_name in os.listdir(f"{path}/S3_hyundai/2.working_done"):
        file_name = os.listdir(f"{path}/S3_hyundai/0.given_data/{folder_name}/LDR_RAW_PCD/")[0][12:]
        # print(file_name)
        result = file_name.split('-')
        company = result[0]
        test_car_num = result[1]
        log_start_time =  "20" + result[2]
        print(log_start_time)

        property_input_folder = f"{path}/S3_hyundai/2.working_done/{folder_name}/"
        property_output_folder = f"{path}/S3_hyundai/3.out/{folder_name}/LDR_GT_Property/"
        property_filename = f"LDR_GT_Property-{file_name}-{version}.json"

        box_input_folder = f"{path}/S3_hyundai/2.working_done/{folder_name}/annotations"
        box_output_folder = f"{path}/S3_hyundai/3.out/{folder_name}/LDR_GT_Box"
        box_filename = f"LDR_GT_Box-{file_name}-{version}.json"

        # TODO Property
        # 생성된 폴더 확인 및 생성
        if not os.path.exists(property_output_folder):

            # 후처리 할 데이터 불러오기
            data = pd.read_excel(property_input_folder + 'property_data.xlsx')
            data.drop([0, 1], axis=0, inplace=True)
            data.reset_index(drop=True,inplace=True)

            # csv 파일에서 데이터
            for i in range(len(data)):
                row = data.loc[i]
                seq_data = GTP.sequence_metadata(row)
                sence_data = GTP.sence_curation(row)
                output_json = GTP.convert_to_new_format(seq_data,sence_data)
            # else:
            #     print("error: data[NAME] not found in 'property_data.xlsx'")
            # 파일명과 동일한 이름으로 변환된 JSON 파일 저장
            os.makedirs(property_output_folder)
            output_file = os.path.join(property_output_folder, property_filename)
            with open(output_file, 'w') as f:
                json.dump(output_json, f, indent=2)
                # print(f'Save {json_file}')

        # TODO BOX
        # 생성된 폴더 확인 및 생성
        if not os.path.exists(box_output_folder):
            # 입력 폴더 내의 모든 JSON 파일 목록 가져오기
            json_files = [f for f in os.listdir(box_input_folder) if f.endswith('.json')]

            output_json = {"FRAME_LIST": []}
            for idx,json_file in enumerate(json_files):

                pcdfilenum = int(json_file[:6])

                # 각 JSON 파일을 읽어오기
                with open(os.path.join(box_input_folder, json_file), 'r') as f:
                    data = json.load(f)
                # 후처리 함수
                frame_metadata = GTB.change_frame_metadata(idx, pcdfilenum, log_start_time)
                object_list = GTB.change_object_list(data)
                frame = GTB.frames(object_list, frame_metadata)
                output_json['FRAME_LIST'].append(frame)

            # 파일명과 동일한 이름으로 변환된 JSON 파일 저장
            output_file = os.path.join(box_output_folder, box_filename)
            os.makedirs(box_output_folder)
            with open(output_file, 'w') as f:
                json.dump(output_json, f, indent=2)
            print(f"🆕🆕🆕 '{folder_name}' 폴더 생성 되었습니다. 🆕🆕🆕")

        else:
            print(f"❗❗❗ '{folder_name}' 폴더는 이미 생성 되었습니다. ❗❗❗")
    print("💛💛💛 후처리 코드 종료 💛💛💛")
