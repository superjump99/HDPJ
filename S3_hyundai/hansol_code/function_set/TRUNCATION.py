import os
import json
import pandas as pd
import math
from shapely.geometry import Polygon

import matplotlib.pyplot as plt
import matplotlib.patches as patches
# from matplotlib.patches import Rectangle, Polygon
import numpy as np


def calculate_box_vertices(center_x, center_y, length, width, rotationYaw):
    # 반 가로와 반 세로 길이
    half_width = width / 2.0
    half_length = length / 2.0

    # 박스의 중심에서 각 꼭지점까지의 상대적 위치
    corners_relative = [
        (-half_length, -half_width),
        (-half_length, half_width),
        (half_length, half_width),
        (half_length, -half_width)
    ]

    # 회전 변환을 적용하여 각 꼭지점을 계산
    corners_rotated = [
        (
            center_x + x * math.cos(rotationYaw) - y * math.sin(rotationYaw),
            center_y + x * math.sin(rotationYaw) + y * math.cos(rotationYaw)
        ) for x, y in corners_relative
    ]

    return corners_rotated

field_data = [(-1, 0), (20, 50), (120, 50), (120, -50), (20, -50), (-1, 0)]
field = np.array(field_data)
field_polygon = Polygon(field_data)
print(field_polygon)

cuboid_test = "C:/Users/pc/hyundai/input/HYUNDAI/CUBOID_TEST/"

json_files = [f for f in os.listdir(f"{cuboid_test}/annotations") if f.endswith('.json')]

for idx, json_file in enumerate(json_files):
    pcdfilenum = int(json_file[:6])

    # 각 JSON 파일을 읽어오기
    with open(os.path.join(f"{cuboid_test}/annotations", json_file), 'r') as f:
        data = json.load(f)
    # print(len(data['labels']))
    converted_data = [
        {
            "category": label['category'],
            "x": label["box3d"]["location"]["x"],
            "y": label["box3d"]["location"]["y"],
            "width": label["box3d"]["dimension"]["width"],
            "length": label["box3d"]["dimension"]["length"],
            "rotationYaw": label["box3d"]["orientation"]["rotationYaw"]
        }
        for i, label in enumerate(data["labels"])
    ]
    df = pd.DataFrame(converted_data)
    # print(df)
    plt.figure(figsize=(10, 8))
    plt.plot(field[:, 0], field[:, 1], '-o', label='Field Boundary')
    for idx in range(len(df)):
        print(df.iloc[idx].tolist()[1:])
        boxpoint = df.iloc[idx].tolist()[1:]

        box_vertices = np.array(calculate_box_vertices(boxpoint[0], boxpoint[1], boxpoint[2], boxpoint[3], boxpoint[4]))
        box_polygon = Polygon(calculate_box_vertices(boxpoint[0], boxpoint[1], boxpoint[2], boxpoint[3], boxpoint[4]))

        # print(box_polygon)
        plt.plot(box_vertices[:, 0], box_vertices[:, 1], '-s', label=f'Box {idx}')
        # plt.fill(box_vertices[:, 0], box_vertices[:, 1], 'b', alpha=0.1, label=f'Box {idx} ')
        if not field_polygon.contains(box_polygon):
            # print(field_polygon.contains(box_polygon))
            # 박스와 필드의 차집합 영역 계산
            difference_area = box_polygon.difference(field_polygon).area
            rating = difference_area / box_polygon.area
            # print(rating,field_polygon.area, difference_area, box_polygon.area)
        else:
            difference_area = 0
        # else:
        #     difference_area = 0
        # print(difference_area)
    # print(box_vertices)
    # 그래프 설정

    # plt.plot(box_vertices[:, 0], box_vertices[:, 1], '-s', label='Box')
    #
    # # 필드와 박스가 겹치는 부분 강조
    #
    plt.title('Field with Box')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.show()

def gkatndlfma():

    return 결과값