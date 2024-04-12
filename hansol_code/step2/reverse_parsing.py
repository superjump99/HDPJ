import json
import os


if __name__ == '__main__':
    LDR_GT_Box = 'LDR_GT_BOX'
    file_name = ''

    version = '4.1.3'
    s3_path = 'S3_hyundai'
    step_path = 'step2'
    # step_path = 'step1'
    given_data_path = '0.given_data'
    parsing_done_path = '1.reverse_parsing_done'
    working_done_path = '3.working_done'
    out_path = '4.out'

    space = "03_Urban"
    dataset = "HKMC-N2202209-240220"

    os.chdir('../../')
    base_path = os.path.join(f"{os.getcwd()}/{s3_path}/{step_path}/")
    dataset_list = os.listdir(f"{base_path}/{given_data_path}/{space}/{dataset}/")
    for sequence_set in dataset_list:
        print(sequence_set)
        box_json = os.listdir(f"{base_path}/{given_data_path}/{space}/{dataset}/{sequence_set}/LDR_GT_Box/")
        json_file = os.path.join(f"{base_path}/{given_data_path}/{space}/{dataset}/{sequence_set}/LDR_GT_Box/"
                                 + box_json[0])
        print(box_json)
        print(json_file)
        if not os.path.exists(f"{base_path}/{parsing_done_path}/{space}/{dataset}/{sequence_set}"):
            print(f"{base_path}/{parsing_done_path}/{space}/{dataset}/{sequence_set}")

            with open(json_file, 'r') as f:
                data = json.load(f)

            for i in range(len(data["FRAME_LIST"])):
                output = {
                    "name": f"{i:06d}",
                    "timestamp": 0,
                    "index": i,
                    "labels": []
                }
                input_objs = [sublist for sublist in data["FRAME_LIST"][i]['OBJECT_LIST']]
                for idx, item in enumerate(input_objs):
                    label = {
                        "id": idx,
                        "category": item["CLASS"],
                        "occlusion": str(item["OCCLUSION"]),
                        "box3d": {
                            "dimension": {
                                "width": item["DIMENSION"][1],
                                "length": item["DIMENSION"][0],
                                "height": item["DIMENSION"][2]
                            },
                            "location": {
                                "x": item["LOCATION"][0],
                                "y": item["LOCATION"][1],
                                "z": -item["LOCATION"][2]  # Assuming this needs to be positive
                            },
                            "orientation": {
                                "rotationYaw": item["HEADING"],
                                "rotationPitch": 0,
                                "rotationRoll": 0
                            }
                        }
                    }
                    output["labels"].append(label)
                print(output)
                output_file = os.path.join(f"{base_path}/{out_path}/{space}/{dataset}/annotations", dfasd)
                os.makedirs(f"{base_path}/{out_path}/{space}/{dataset}/{today}-LDR_GT_BOX")
                with open(output_file, 'w') as f:
                    json.dump(output_json, f, indent=2)
    #     exit()
    # # for json in box_json:
    # #     print(folder)
    # exit()
    # # if os.path.exists(f"{base_path}/{parsing_done_path}/{space}/{dataset}):