import os
import json
import pandas as pd

def sequence_metadata(data):
    seq_data = {
        "VERSION": "4.1.2",
        "NUM_OF_FRAMES": data["NUM_OF_FRAMES"],
        "FPS": data["FPS"],
        "START_TIME": str(data["START_TIME"]),
        "END_TIME": str(data["END_TIME"]),
        "STAGE": data["STAGE"],
    }
    return seq_data

def sence_curation(data):
    sence_data = {
        "COUNTRY": data["COUNTRY"],
        "WEATHER": data["WEATHER"],
        "ILLUMINATION": data["ILLUMINATION"],
        "ROAD": data["ROAD"],
        "ROAD_SURFACE": data["ROAD_SURFACE"],
    }
    return sence_data

def convert_to_new_format(seq_data,sence_data):
        output_json = {
            "SEQUENCE_METADATA": seq_data,
            "SCENE_CURATION": sence_data
        }
        return output_json

if __name__ == "__main__":
    folder_name = "HKMC-N2202209-240111"
    file_name = os.listdir(f"C:/Users/pc/SS-233/23-ds-041/S3_hyundai/0.given_data/{folder_name}/LDR_RAW_PCD/")[0][12:]

    property_input_folder = f"C:/Users/pc/SS-233/23-ds-041/S3_hyundai/2.working_done/{folder_name}/"
    property_output_folder = f"C:/Users/pc/SS-233/23-ds-041/S3_hyundai/3.out/{folder_name}/LDR_GT_Property/"

    property_filename = f"LDR_GT_Property-{file_name}-4.1.1.json"


    # 생성된 폴더 확인 및 생성
    if not os.path.exists(property_output_folder):
        os.makedirs(property_output_folder)

        # 후처리 할 데이터 불러오기
        data = pd.read_excel(property_input_folder +'property_data.xlsx')
        data.drop([0, 1], axis=0, inplace=True)
        data.reset_index(drop=True,inplace=True)

        if data["NAME"][0] == folder_name:
            # csv 파일에서 데이터
            for i in range(len(data)):
                row = data.loc[i]
                seq_data = sequence_metadata(row)
                sence_data = sence_curation(row)
                output_json = convert_to_new_format(seq_data,sence_data)
                # print(outout_json)

        # 파일명과 동일한 이름으로 변환된 JSON 파일 저장
        output_file = os.path.join(property_output_folder, property_filename)
        with open(output_file, 'w') as f:
            json.dump(output_json, f, indent=2)
            # print(f'Save {json_file}')