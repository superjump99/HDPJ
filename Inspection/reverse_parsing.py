import json
import os


if __name__ == '__main__':
    LDR_GT_Box = 'LDR_GT_BOX'
    file_name = ''

    version = '4.1.3'
    s3_path = 'S3_hyundai'

    HDC_path = os.getcwd()
    version = '4.1.3'
    bucket_name = 'coop-selectstar-7000527-241231/'
    task = '02_Inspection/'

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

    space_dir = os.path.join(f"{os.getcwd()}/{bucket_name}/{task}/{space}")
    dataset_list = os.listdir(space_dir)
    print(dataset_list)
    # exit()
    # dataset_list = os.listdir(f"{base_path}/{given_data_path}/{space}/{dataset}/")
    for sequence_set in dataset_list:
        if sequence_set.endswith(".json"):
            print(sequence_set)
            # box_json = os.listdir(f"{space_dir}/{given_data_path}/{space}/{dataset}/{sequence_set}/LDR_GT_Box/")
            # json_file = os.path.join(f"{base_path}/{given_data_path}/{space}/{dataset}/{sequence_set}/LDR_GT_Box/"+ box_json[0])
            # print(box_json)
            json_file = os.path.join(space_dir, sequence_set)
            print(json_file)
            # print(json_file)
            # if not os.path.exists(f"{base_path}/{parsing_done_path}/{space}/{dataset}/{sequence_set}"):
                # print(f"{base_path}/{parsing_done_path}/{space}/{dataset}/{sequence_set}")

            with open(json_file, 'r') as f:
                data = json.load(f)

        # exit()
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
                    output_path = os.path.join(f"{space_dir}/{sequence_set[:-5]}/annotations/", f"{i:06d}.json")
                    os.makedirs(f"{space_dir}/{sequence_set[:-5]}/annotations/", exist_ok=True)
                    with open(output_path, 'w') as f:
                        json.dump(output, f, indent=2)
    #     exit()
    # # for json in box_json:
    # #     print(folder)
    # exit()
    # # if os.path.exists(f"{base_path}/{parsing_done_path}/{space}/{dataset}):