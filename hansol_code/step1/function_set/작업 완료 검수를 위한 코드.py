import os
import json
import datetime
import math

# TODO 검수 후처리 코드
def change_object_list(input_json):
    object_list = []
    try:
        for i in range(len(input_json['labels'])):
            label = {
                "CLASS": input_json["labels"][i]['category'],
                "OCCLUSION": input_json["labels"][i]['occlusion'],
                # TODO Fix TRUNCATION value
                "TRUNCATION": 0 , #1 / (input_json["labels"][i]["box3d"]["dimension"]["width"]*input_json["labels"][i]["box3d"]["dimension"]["length"]),
                "LOCATION": [
                    round(input_json["labels"][i]["box3d"]["location"]["x"], 2),
                    round(input_json["labels"][i]["box3d"]["location"]["y"], 2),
                    round(input_json["labels"][i]["box3d"]["location"]["z"], 2)
                ],
                "DIMENSION": [
                    round(input_json["labels"][i]["box3d"]["dimension"]["width"], 2),
                    round(input_json["labels"][i]["box3d"]["dimension"]["length"], 2),
                    round(input_json["labels"][i]["box3d"]["dimension"]["height"], 2)
                ],
                "HEADING": round(input_json["labels"][i]["box3d"]["orientation"]["rotationYaw"], 4),
            }
            object_list.append(label)
    except KeyError:
        pass
    return object_list

def round_float(input_json,idx):
    if len(input_json["labels"]) != 0:
        print(len(input_json['labels']))
        for idx in range(len(input_json['labels'])):
            input_json["labels"][idx]["box3d"]["dimension"]["width"] = round(input_json["labels"][idx]["box3d"]["dimension"]["width"],2)
            input_json["labels"][idx]["box3d"]["dimension"]["length"] = round(input_json["labels"][idx]["box3d"]["dimension"]["length"],2)
            input_json["labels"][idx]["box3d"]["dimension"]["height"] = math.floor(input_json["labels"][idx]["box3d"]["dimension"]["height"]*100)/100
            input_json["labels"][idx]["box3d"]["location"]["x"] = round(input_json["labels"][idx]["box3d"]["location"]["x"],2)
            input_json["labels"][idx]["box3d"]["location"]["y"] = round(input_json["labels"][idx]["box3d"]["location"]["y"],2)
            input_json["labels"][idx]["box3d"]["location"]["z"] = round(input_json["labels"][idx]["box3d"]["location"]["z"],2)
            input_json["labels"][idx]["box3d"]["orientation"]["rotationYaw"] = round(input_json["labels"][idx]["box3d"]["orientation"]["rotationYaw"],4)
            input_json["labels"][idx]["box3d"]["orientation"]["rotationPitch"] = 0
            input_json["labels"][idx]["box3d"]["orientation"]["rotationPitch"] = 0

    return input_json

if __name__ == "__main__":

    high_path = '/'
    step1_path = 'S3_hyundai/1.div&remove'
    step2_path = 'S3_hyundai/2.parsing_done'
    step3_path = 'S3_hyundai/3.working_done'
    space = "00_sample"
    sequenceset = "HKMC-N2202209-240111"
    dataset = "CUBOID_TEST"
    xx = "C:/Users/pc/SS-233/hyundai_code/S3_hyundai/3.working_done/CUBOID_TEST/annotations"
    outfolder = "C:/Users/pc/SS-233/hyundai_code/S3_hyundai/3.working_done/CUBOID_TEST/annotations_검수/annotations"


    json_files = [f for f in os.listdir(xx) if f.endswith('.json')]

    for idx, json_file in enumerate(json_files):

        with open(os.path.join(xx, json_file), 'r') as f:
            data = json.load(f)

        output_json = round_float(data,idx)
        output_file = os.path.join(outfolder, json_file)

        if not os.path.exists(outfolder):
            os.makedirs(outfolder)
        with open(output_file, 'w') as f:
            json.dump(output_json, f, indent=2)




# for sequence_set in os.listdir(f"{high_path}/{step3_path}/{space}/{dataset}/"):
    #     file_name = os.listdir(f"{high_path}/{step3_path}/{space}/LDR_RAW_PCD/")[0][12:]
    #     annotation_folder = f"{high_path}/{step1_path}/{space}/{dataset}/{sequence_set}/annotations/"
    #
    #     # print(file_name)
    #     sequence_set_list = file_name.split('-')
    #     # company = result[0]
    #     # test_car_num = result[1]
    #     log_start_time = "20" + sequence_set_list[2]
    #     print(log_start_time)
    #
    #     json_files = [f for f in os.listdir(annotation_folder) if f.endswith('.json')]
    #
    #     for idx,box_file in enumerate(json_files):
    #         pcdfile_num = int(box_file[:6])
    #
    #         with open(os.path.join(annotation_folder, box_file), 'r') as f:
    #             data = json.load(f)
    #
    #
    #
    #
    #     property_input_folder = f"{high_path}/S3_hyundai/2.working_done/{folder_name}/"
    #     property_output_folder = f"{high_path}/S3_hyundai/3.out/{folder_name}/LDR_GT_Property/"
    #     property_filename = f"LDR_GT_Property-{file_name}-{version}.json"
    #
    #     box_input_folder = f"{path}/S3_hyundai/2.working_done/{folder_name}/annotations"
    #     box_output_folder = f"{path}/S3_hyundai/3.out/{folder_name}/LDR_GT_Box"
    #     box_filename = f"LDR_GT_Box-{file_name}-{version}.json"