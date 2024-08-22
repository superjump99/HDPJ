import os
import json
import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon

def  load_json_annotations(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    converted_data = [
        {
            "category": label['category'],
            "id": label['id'],
            "x": label["box3d"]["location"]["x"],
            "y": label["box3d"]["location"]["y"],
            "z": label["box3d"]["location"]["z"],
            "OCCLUSION": label['occlusion'],
            "width": label["box3d"]["dimension"]["width"],
            "length": label["box3d"]["dimension"]["length"],
            "height": label["box3d"]["dimension"]["height"],
            "rotationYaw": label["box3d"]["orientation"]["rotationYaw"]
        }
        for label in data["labels"]
    ]
    return pd.DataFrame(converted_data)

def calculate_box_vertices(center_x, center_y, center_z ,width, length, height, rotationYaw):
    # 반 가로와 반 세로 길이
    half_width = width / 2.0
    half_length = length / 2.0
    half_height = height / 2.0

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

    # 3D 공간에서 각 꼭지점을 계산 (z 좌표 포함)
    vertices = []
    for x, y in corners_rotated:
        # 상단 꼭지점 (높이가 더해진 경우)
        # x,y = f"{x:.2f}", f"{y:.2f}"
        vertices.append((x, y, center_z + half_height))
        # 하단 꼭지점 (높이가 뺀 경우)
        vertices.append((x, y, center_z - half_height))

    return vertices

def truncation(df):
    field = np.array([(-1, 0), (20, 50), (120, 50), (120, -50), (20, -50), (-1, 0)])

    plt.figure(figsize=(10, 8))
    plt.plot(field[:, 0], field[:, 1], '-o', label='Field Boundary')
    field_polygon = Polygon(field)
    truncation_list = []
    box_vertices_list = []
    for idx, row in df.iterrows():
        box_vertices = np.array(calculate_box_vertices(row['x'], row['y'], row['z'], row['length'], row['width'], row['height'], row['rotationYaw']))
        box_vertices_list.append(box_vertices)
        box_polygon = Polygon(box_vertices)

        plt.plot(box_vertices[:, 0], box_vertices[:, 1], '-s', label=f'Box {idx}')
        if not field_polygon.contains(box_polygon):
            # 박스와 필드의 차집합 영역 계산
            difference_area = box_polygon.difference(field_polygon).area
            # try:
            rating = difference_area / box_polygon.area
            # except:
            #     rating = 0
        else:
            rating = 0
        truncation_list.append(rating)
        plt.close()

    df['truncation'] = truncation_list
    return df, box_vertices_list


if __name__ == '__main__':
    field_data = [(-1, 0), (20, 50), (120, 50), (120, -50), (20, -50), (-1, 0)]
    field = np.array(field_data)
    annotations_path = "C:/Users/pc/hyundai/input/HYUNDAI/CUBOID_TEST/annotations"

    json_files = [f for f in os.listdir(annotations_path) if f.endswith('.json')]
    for json_file in json_files:
        df = load_json_annotations(os.path.join(annotations_path, json_file))
        truncation_df = truncation(field, df)
        print(truncation_df)

