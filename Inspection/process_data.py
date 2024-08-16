import os
import json


def process_dataset(LDR_GT_BOX, sequence_set, save_path):
    parsing_num = []
    for boxjson in os.listdir(LDR_GT_BOX):
        if boxjson[11:-11] != sequence_set:
            continue
        else:
            json_file = os.path.join(LDR_GT_BOX, boxjson)

            with open(json_file, 'r') as f:
                data = json.load(f)
            for i in range(len(data["FRAME_LIST"])):
                parsing_num.append(data["FRAME_LIST"][i]["FRAME_METADATA"]["NUMBER"])
                output = {
                    "name": f"{i:06d}",
                    "timestamp": 0,
                    "index": i,
                    "labels": []
                }
                input_objs = [sublist for sublist in data["FRAME_LIST"][i]['OBJECT_LIST']]
                for idx, item in enumerate(input_objs):
                    if item["CLASS"] == "TUBULER_MARKER":
                        item["CLASS"] = "TUBULAR_MARKER"
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
                                "z": item["LOCATION"][2]  # Assuming this needs to be positive
                            },
                            "orientation": {
                                "rotationYaw": item["HEADING"],
                                "rotationPitch": 0,
                                "rotationRoll": 0
                            }
                        }
                    }
                    output["labels"].append(label)
                # print(output)
                output_path = os.path.join(f"{save_path}", f"{i:06d}.json")

                with open(output_path, 'w') as f:
                    json.dump(output, f, indent=2)
    return parsing_num