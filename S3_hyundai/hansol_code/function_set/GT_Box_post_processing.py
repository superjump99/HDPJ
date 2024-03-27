import os
import json
import datetime

stage_list = ['0.NotAnnotated','1.AutomaticallyAnnotated','2.ManuallyRefined','3.VerifiedByAnnotator','4.VerifiedByEngineer']
"""
parameter
"""

stage = stage_list[0]
# print(stage)
inspction_step = 0

def change_frame_metadata(num,pcdnum,start_time):
    # TODO: FRAME_LIST 수정 필요
    # print(start_time)
    # print(type(start_time))
    year = int(start_time[:4])
    month = int(start_time[4:6])
    day = int(start_time[6:8])
    hour = int(start_time[8:10])
    minute = int(start_time[10:12])
    second = int(start_time[12:])
    start_time = datetime.datetime(year,month,day,hour,minute,second)
    # print(datetime.timedelta(seconds = num*0.1))
    # print(start_time)

    # print(str(start_time + datetime.timedelta(seconds = num*0.1)))
    # print(start_time)
    # timestamp = start_time + datetime.timedelta(seconds=num * 0.1)
    frame_metadata = {
                    # TODO Fix NUMBER value
                    "NUMBER": num*50,
                    # TODO Fix TIMESTAMP value
                    "TIMESTAMP": str(start_time + datetime.timedelta(seconds=0.5) + datetime.timedelta(seconds=pcdnum*0.5)),
                    "STAGE": stage,
                    "INSPECTION_STEP": inspction_step
                }
    return frame_metadata

def change_object_list(input_json):
    object_list = []
    try:
        for i in range(len(input_json['labels'])):
            label = {
                "CLASS": input_json["labels"][i]['category'],
                "OCCLUSION": str(input_json["labels"][i]['occlusion']),
                # TODO Fix TRUNCATION value
                "TRUNCATION": 0 , #1 / (input_json["labels"][i]["box3d"]["dimension"]["width"]*input_json["labels"][i]["box3d"]["dimension"]["length"]),
                "LOCATION": [
                    round(input_json["labels"][i]["box3d"]["location"]["x"], 2),
                    round(input_json["labels"][i]["box3d"]["location"]["y"], 2),
                    round(input_json["labels"][i]["box3d"]["location"]["z"], 2)
                ],
                "DIMENSION": [
                    round(input_json["labels"][i]["box3d"]["dimension"]["length"], 2),
                    round(input_json["labels"][i]["box3d"]["dimension"]["width"], 2),
                    round(input_json["labels"][i]["box3d"]["dimension"]["height"], 2)
                ],
                "HEADING": round(input_json["labels"][i]["box3d"]["orientation"]["rotationYaw"], 4),
            }
            object_list.append(label)
    except KeyError:
        pass
    return object_list

def frames(object_list,frame_metadata):

    FRAME_list = {
                "FRAME_METADATA": frame_metadata,
                "OBJECT_LIST": object_list
            }
    return FRAME_list

if __name__ == "__main__":
    pass