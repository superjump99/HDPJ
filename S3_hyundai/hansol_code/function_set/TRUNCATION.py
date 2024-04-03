import os
import json
import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon

def load_json_annotations(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    converted_data = [
        {
            "category": label['category'],
            "x": label["box3d"]["location"]["x"],
            "y": label["box3d"]["location"]["y"],
            "width": label["box3d"]["dimension"]["width"],
            "length": label["box3d"]["dimension"]["length"],
            "rotationYaw": label["box3d"]["orientation"]["rotationYaw"]
        }
        for label in data["labels"]
    ]
    return pd.DataFrame(converted_data)

def calculate_box_vertices(center_x, center_y, width, length, rotationYaw):
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

def plot_field_and_boxes(field, df):
    plt.figure(figsize=(10, 8))
    plt.plot(field[:, 0], field[:, 1], '-o', label='Field Boundary')
    field_polygon = Polygon(field)
    for idx, row in df.iterrows():
        box_vertices = np.array(calculate_box_vertices(row['x'], row['y'], row['length'], row['width'], row['rotationYaw']))
        box_polygon = Polygon(box_vertices)

        plt.plot(box_vertices[:, 0], box_vertices[:, 1], '-s', label=f'Box {idx}')
        if not field_polygon.contains(box_polygon):
            # 박스와 필드의 차집합 영역 계산
            difference_area = box_polygon.difference(field_polygon).area
            rating = difference_area / box_polygon.area
        else:
            rating = 0
        print(f'Box {idx}', rating)
    plt.title('Field with Box')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.show()

def process_annotations(annotations_path, field_data):
    field = np.array(field_data)
    json_files = [f for f in os.listdir(annotations_path) if f.endswith('.json')]
    for json_file in json_files:
        df = load_json_annotations(os.path.join(annotations_path, json_file))
        plot_field_and_boxes(field, df)
        print('----------------------------------------')

if __name__ == '__main__':
    field_data = [(-1, 0), (20, 50), (120, 50), (120, -50), (20, -50), (-1, 0)]
    annotations_path = "C:/Users/pc/hyundai/input/HYUNDAI/CUBOID_TEST/annotations"
    process_annotations(annotations_path, field_data)

#     field = np.array(field_data)
#     field_polygon = Polygon(field_data)
# print(field_polygon)
#
#
# json_files = [f for f in os.listdir(f"{cuboid_test}/annotations") if f.endswith('.json')]
#
# for idx, json_file in enumerate(json_files):
#     pcdfilenum = int(json_file[:6])
#
#     # 각 JSON 파일을 읽어오기
#     with open(os.path.join(f"{cuboid_test}/annotations", json_file), 'r') as f:
#         data = json.load(f)
#     # print(len(data['labels']))
#     converted_data = [
#         {
#             "category": label['category'],
#             "x": label["box3d"]["location"]["x"],
#             "y": label["box3d"]["location"]["y"],
#             "width": label["box3d"]["dimension"]["width"],
#             "length": label["box3d"]["dimension"]["length"],
#             "rotationYaw": label["box3d"]["orientation"]["rotationYaw"]
#         }
#         for i, label in enumerate(data["labels"])
#     ]
#     df = pd.DataFrame(converted_data)
#     # print(df)
#     plt.figure(figsize=(10, 8))
#     plt.plot(field[:, 0], field[:, 1], '-o', label='Field Boundary')
#     for idx in range(len(df)):
#         print(df.iloc[idx].tolist()[1:])
#         boxpoint = df.iloc[idx].tolist()[1:]
#
#         box_vertices = np.array(calculate_box_vertices(boxpoint[0], boxpoint[1], boxpoint[2], boxpoint[3], boxpoint[4]))
#         box_polygon = Polygon(calculate_box_vertices(boxpoint[0], boxpoint[1], boxpoint[2], boxpoint[3], boxpoint[4]))
#
#         # print(box_polygon)
#         plt.plot(box_vertices[:, 0], box_vertices[:, 1], '-s', label=f'Box {idx}')
#         # plt.fill(box_vertices[:, 0], box_vertices[:, 1], 'b', alpha=0.1, label=f'Box {idx} ')
#         if not field_polygon.contains(box_polygon):
#             # print(field_polygon.contains(box_polygon))
#             # 박스와 필드의 차집합 영역 계산
#             difference_area = box_polygon.difference(field_polygon).area
#             rating = difference_area / box_polygon.area
#             # print(rating,field_polygon.area, difference_area, box_polygon.area)
#         else:
#             difference_area = 0
#
#
#     plt.title('Field with Box')
#     plt.xlabel('X')
#     plt.ylabel('Y')
#     plt.legend()
#     plt.grid(True)
#     plt.axis('equal')
#     plt.show()
