import os
import pandas as pd
import Label
import shutil
import re

# G:\내 드라이브\PM2팀\#김한솔\23-DS-041_현대자동차\3. 데이터\2. 작업 데이터\02_Inspection\01_IRIS_JX013\03_Urban\HKMC-N2202209-240207
def process_sequence(data_path, sequence):
    sequence_path = os.path.join(data_path, sequence)
    save_path = f'{data_path}/LDR_GT_Inspection/'
    # print(save_path)
    for value in os.listdir(sequence_path):
        if value.startswith('LDR') and os.path.isdir(os.path.join(sequence_path, value)):
            images_dir = os.path.join(sequence_path, value)
            print(f"Count Image = {len(os.listdir(images_dir)) - 1}")

            shutil.copytree(images_dir, f"{save_path}/{value}", dirs_exist_ok=True)

        elif value.endswith('.xlsx'):
            df = pd.read_excel(os.path.join(sequence_path, value))

            # Frame Number 및 Selected Point Number 추출
            df['Frame Number'] = df['Frame Index'].str.extract(r'(\d+)').astype(int)
            df['Selected Point Number'] = df['Selected Points Class/Object'].str.extract(r'\[(-?\d+)\]')

            # Frame Number를 기준으로 그룹화
            start_value = df['Frame Number'].min() - 50
            df['annotations'] = ((df['Frame Number'] - start_value) // 50).astype(int) - 1

            df_to_dict = df.groupby('annotations')['Selected Point Number'].apply(list).to_dict()

            # 입력 폴더 내의 모든 JSON 파일 목록 가져오기
            annotation_json = sorted(
                f for f in os.listdir(f"{sequence_path}/annotations") if f.endswith('.json')
            )

            necessary_vertex = []
            df_miss_gt = pd.DataFrame()

            for idx, annotation in enumerate(annotation_json):
                filenum = int(annotation.split('.json')[0])

                if filenum in df_to_dict.keys():
                    # print(filenum)
                    json_file = Label.postprocessing.TRUNCATION.load_json_annotations(
                        os.path.join(sequence_path, "annotations", annotation))
                    df_miss_gt = pd.concat([df_miss_gt, json_file[json_file['category'] == 'Miss_GT']], ignore_index=True)

                    _, box_vertices_list = Label.postprocessing.TRUNCATION.truncation(json_file)
                    _, miss_gt_box_vertices = Label.postprocessing.TRUNCATION.truncation(df_miss_gt)

                    for id in df_to_dict[filenum]:
                        id_int = int(id)
                        if id_int > 0:
                            necessary_vertex.append(box_vertices_list[id_int].tolist())
                        else:
                            necessary_vertex.append(miss_gt_box_vertices[-id_int - 1].tolist())

            df['ROI 8 points'] = necessary_vertex


            # 불필요한 열 삭제
            df.drop(['Frame Number', 'Selected Point Number', 'annotations'], axis=1, inplace=True)

            # Miss GT Issue에 해당하는 행을 찾아 Selected Points Class/Object 값을 수정
            df.loc[df['Issue'] == 'Miss GT Issue', 'Selected Points Class/Object'] = "[-1] th object ['UNLABELED']"
            print(f"Count Error = {len(df)}")

            name = f"{value.split('.xlsx')[0]}.csv"
            df.to_csv(os.path.join(save_path, name), index=False)


def check_result(inspection_dir):
    for value in os.listdir(inspection_dir):
        if value.endswith('.csv'):
            df = pd.read_csv(os.path.join(inspection_dir, value))
            df['Combined'] = df['Frame Index'].str.replace('.pcd', '').astype(str) + '_' + df[
                'Inspection Index'].astype(str)
            error_list = df['Combined'].tolist()
            normalized_list1 = [re.sub(r'^0+', '', item) for item in error_list]
            for dir in os.listdir(inspection_dir):
                if dir == value.split('.csv')[0]:
                    print(value.split('.csv')[0])
                    images_dir = os.path.join(inspection_dir, dir)
                    images_dir_list = os.listdir(images_dir)
                    normalized_list2 = [re.sub(r'\.jpg$', '', re.sub(r'^0+', '', item)) for item in images_dir_list if
                                        not item.endswith('.ini')]

            sorted_list1 = sorted(normalized_list1, key=lambda x: (int(x.split('_')[0]), int(x.split('_')[1])))
            sorted_list2 = sorted(normalized_list2, key=lambda x: (int(x.split('_')[0]), int(x.split('_')[1])))
            print(len(sorted_list1), sorted_list1)
            print(len(sorted_list2), sorted_list2)

if __name__ == '__main__':

    bucket_name = "coop-selectstar-7000527-241231/"
    step = "02_Inspection/"
    sensor = "01_IRIS_JX013/"
    space = "03_Urban/"

    drive = "G:/내 드라이브/PM2팀/#김한솔/23-DS-041_현대자동차/3. 데이터/2. 작업 데이터"

    # STEP 1: Set base file
    try:
        middle_folder_name = os.listdir(f'{drive}/{bucket_name}/{step}/{sensor}/{space}/')[0]

    except:
        middle_folder_name = os.listdir(f'{drive}/{step}/{sensor}/{space}/')[0]
        data_path = os.path.join(f'{drive}/{step}/{sensor}/{space}/', middle_folder_name)
        inspection_dir = os.path.join(data_path, 'LDR_GT_Inspection/')

    for i, sequence in enumerate(os.listdir(data_path)):
        if sequence.startswith('HKMC'):
            process_sequence(data_path, sequence)
            check_result(inspection_dir)

