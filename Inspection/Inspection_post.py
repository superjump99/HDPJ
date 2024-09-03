import os
import pandas as pd
import Label
import shutil
import re

# G:\내 드라이브\PM2팀\#김한솔\23-DS-041_현대자동차\3. 데이터\2. 작업 데이터\02_Inspection\01_IRIS_JX013\03_Urban\HKMC-N2202209-240207

def copy_and_rename_images(sequence_path, save_path, sequence):
    for value in os.listdir(sequence_path):
        value_path = os.path.join(sequence_path, value)

        if os.path.isdir(value_path) and value.startswith('LDR'):
            dest_path = os.path.join(save_path, value)
            shutil.copytree(value_path, dest_path)


            # Rename jpg files in the copied directory
            for image in os.listdir(dest_path):
                if image.endswith('.jpg'):
                    new_image_name = image.replace('-', '_')
                    new_image_name = f'LDR_INSPECTION-{sequence}_{new_image_name}'
                    os.rename(os.path.join(dest_path, image), os.path.join(dest_path, new_image_name))

            return len(os.listdir(dest_path)) - 1
def process_excel_files(sequence_path, save_path):
    for value in os.listdir(sequence_path):
        if value.endswith('.xlsx'):
            value_path = os.path.join(sequence_path, value)

            df = pd.read_excel(value_path)

            # Extract Frame Number and Selected Point Number
            df['Frame Number'] = df['Frame Index'].str.extract(r'(\d+)').astype(int)
            df['Selected Point Number'] = df['Selected Points Class/Object'].str.extract(r'\[(-?\d+)\]')

            # Group by Frame Number
            start_value = df['Frame Number'].min() - 50
            df['annotations'] = ((df['Frame Number'] - start_value) // 50).astype(int) - 1

            df_to_dict = df.groupby('annotations')['Selected Point Number'].apply(list).to_dict()

            # List all JSON files in the annotations directory
            annotation_json_path = os.path.join(sequence_path, "annotations")
            annotation_json = sorted(f for f in os.listdir(annotation_json_path) if f.endswith('.json'))

            necessary_vertex = []
            df_miss_gt = pd.DataFrame()

            for annotation in annotation_json:
                filenum = int(annotation.split('.json')[0])

                if filenum in df_to_dict:
                    json_file = Label.postprocessing.TRUNCATION.load_json_annotations(
                        os.path.join(annotation_json_path, annotation)
                    )
                    df_miss_gt = pd.concat([df_miss_gt, json_file[json_file['category'] == 'Miss_GT']],
                                           ignore_index=True)

                    _, box_vertices_list = Label.postprocessing.TRUNCATION.truncation(json_file)
                    _, miss_gt_box_vertices = Label.postprocessing.TRUNCATION.truncation(df_miss_gt)

                    for id_str in df_to_dict[filenum]:
                        id_int = int(id_str)
                        if id_int > 0:
                            necessary_vertex.append(box_vertices_list[id_int].tolist())
                        else:
                            necessary_vertex.append(miss_gt_box_vertices[-id_int - 1].tolist())

            df['ROI 8 points'] = necessary_vertex

            # Remove unnecessary columns
            df.drop(['Frame Number', 'Selected Point Number', 'annotations'], axis=1, inplace=True)

            # Modify rows with Miss GT Issue
            df.loc[df['Issue'] == 'Miss GT Issue', 'Selected Points Class/Object'] = "[-1] th object ['UNLABELED']"

            name = f"{value.split('.xlsx')[0]}.csv"
            df.to_csv(os.path.join(save_path, name), index=False)
            print(f'{name} Done')

            return df.shape[0]
def process_sequence(data_path, sequence, save_path):
    sequence_path = os.path.join(data_path, sequence)

    cnt_image_error = copy_and_rename_images(sequence_path, save_path, sequence)
    cnt_csv_error = process_excel_files(sequence_path, save_path)
    print(f"이미지 : {cnt_image_error}\n"
          f"csv : {cnt_csv_error}")

    raise Exception("에러 개수 불일치") if cnt_image_error != cnt_csv_error else print("에러 개수 일치")





# def check_result(inspection_dir):
#     for value in os.listdir(inspection_dir):
#         if value.endswith('.csv'):
#             df = pd.read_csv(os.path.join(inspection_dir, value))
#             df['Combined'] = df['Frame Index'].str.replace('.pcd', '').astype(str) + '_' + df[
#                 'Inspection Index'].astype(str)
#             error_list = df['Combined'].tolist()
#             normalized_list1 = [re.sub(r'^0+', '', item) for item in error_list]
#             for dir in os.listdir(inspection_dir):
#                 if dir == value.split('.csv')[0]:
#                     print(value.split('.csv')[0])
#                     images_dir = os.path.join(inspection_dir, dir)
#                     images_dir_list = os.listdir(images_dir)
#                     normalized_list2 = [re.sub(r'\.jpg$', '', re.sub(r'^0+', '', item)) for item in images_dir_list if
#                                         not item.endswith('.ini')]
#
#             sorted_list1 = sorted(normalized_list1, key=lambda x: (int(x.split('_')[0]), int(x.split('_')[1])))
#             sorted_list2 = sorted(normalized_list2, key=lambda x: (int(x.split('_')[0]), int(x.split('_')[1])))
#             print(len(sorted_list1), sorted_list1)
#             print(len(sorted_list2), sorted_list2)


if __name__ == '__main__':
    bucket_name = "coop-selectstar-7000527-241231/"
    step = "02_Inspection/"
    sensor = "01_IRIS_JX013/"
    space = "03_Urban/"

    print(step, sensor, space)

    drive = "G:/내 드라이브/PM2팀/#김한솔/23-DS-041_현대자동차/3. 데이터/2. 작업 데이터"

    # STEP 1: Set base file
    try:
        middle_folder_name = os.listdir(f'{drive}/{bucket_name}/{step}/{sensor}/{space}/')[0]
        data_path = os.path.join(f'{drive}/{bucket_name}/{step}/{sensor}/{space}/', middle_folder_name, '검수 완료 파일 업로드')
        inspection_dir = os.path.join(f'{drive}/{bucket_name}/{step}/{sensor}/{space}/', middle_folder_name,
                                      'LDR_GT_Inspection')

    except:
        middle_folder_name = os.listdir(f'{drive}/{step}/{sensor}/{space}/')[0]
        data_path = os.path.join(f'{drive}/{step}/{sensor}/{space}/', middle_folder_name, '검수 완료 파일 업로드')
        inspection_dir = os.path.join(f'{drive}/{step}/{sensor}/{space}/', middle_folder_name, 'LDR_GT_Inspection')

    # STEP 2: Process each sequence in the data path
    for sequence in os.listdir(data_path):

        if sequence.endswith('.ini'):
            continue
        
        print(sequence)
        sequence_path = os.path.join(data_path, sequence)
        save_path = os.path.join(inspection_dir)

        # Ensure the save path exists
        os.makedirs(save_path, exist_ok=True)

        # Process the sequence
        process_sequence(data_path, sequence, save_path)

