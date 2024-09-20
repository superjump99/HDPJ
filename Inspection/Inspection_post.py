import os
import pandas as pd
import Label
import shutil
import re

# G:/내 드라이브/PM2팀/#김한솔/23-DS-041_현대자동차/3. 데이터/2. 작업 데이터/02_Inspection/01_IRIS_JX013/03_Urban\HKMC-N2202209-240207

def process_sequence(data_path, sequence, save_path):
    sequence_path = os.path.join(data_path, sequence)
    print(sequence_path)
    parsing_num_txt = 'parsing_num.txt'
    f = open(os.path.join(sequence_path,parsing_num_txt), 'r')
    lines = f.read()
    start_frame = int(lines.split('~')[0])

    csv_save_path = process_excel_files(sequence_path, save_path,start_frame)
    cel = csv_error_list(path= csv_save_path)

    iel = copy_and_rename_images(sequence_path, save_path, sequence)
    sorted_iel = sorted(iel, key=lambda x: (int(x.split('_')[0]), int(x.split('_')[1])))

    error_show = compare_lists(sorted_iel, cel)
    print(error_show)
    if error_show:
        raise Exception(f"에러 개수 불일치 {error_show}")
    else:
        print("에러 개수 일치")




def compare_lists(iel, cel):
    if len(iel) != len(cel):
        if len(iel) > len(cel):
            long, short = iel, cel
            print(f'image 폴더에 오류가 더 많음')
        else:
            long, short = cel, iel
            print(f'csv 파일에 오류가 더 많음')
        for i in range(len(short)):
            if short[i] in long:
                long.remove(short[i])
        return long



def image_error_list(iel):
    result = []
    for i in iel:
        if i.endswith('.ini'):
            continue
        val = i.split('LDR-1_')[1][:-4]
        result.append(val)
    return result

def transform(row):
    frame_number = int(row['Frame Index'].replace('.pcd', '').lstrip('0'))  # 앞의 0 제거하고 숫자만 남김
    inspection_index = row['Inspection Index']
    return f"{frame_number}_{inspection_index}"
def csv_error_list(path):
    result = []
    df = pd.read_csv(path)
    df['el'] = df.apply(transform, axis=1)
    result = df['el'].tolist()
    return result

def copy_and_rename_images(sequence_path, save_path, sequence):
    for value in os.listdir(sequence_path):
        value_path = os.path.join(sequence_path, value)
        if os.path.isdir(value_path) and value.startswith('LDR'):
            dest_path = os.path.join(save_path, value)
            if not os.path.exists(dest_path):
                shutil.copytree(value_path, dest_path)
                for image in os.listdir(dest_path):
                    if image.endswith('.jpg') or image.endswith('.JPG'):
                        if image.endswith('.JPG'):
                            image.replace('.JPG', '.jpg')
                        new_image_name = image.replace('-', '_')
                        if '_' not in new_image_name:
                            new_image_name = image.replace('.', '_1.')
                        parts = new_image_name.split('_')
                        number_part = parts[-2].zfill(6)
                        index_part = parts[-1]
                        new_image_name = f'LDR_INSPECTION-{sequence}_' + '_'.join(
                            parts[:-2]) + f'{number_part}_{index_part}'
                        os.rename(os.path.join(dest_path, image), os.path.join(dest_path, new_image_name))
            else:
                pass
            iel = image_error_list(os.listdir(dest_path))
            return iel
def process_excel_files(sequence_path, save_path, start_frame):
    for value in os.listdir(sequence_path):
        if value.endswith('.xlsx'):
            value_path = os.path.join(sequence_path, value)

            df = pd.read_excel(value_path)

            # Extract Frame Number and Selected Point Number
            df['Frame Number'] = df['Frame Index'].str.extract(r'(\d+)').astype(int)
            df['Selected Point Number'] = df['Selected Points Class/Object'].str.extract(r'\[(-?\d+)\]')

            # Group by Frame Number
            start_value = start_frame
            print(start_value)
            df['annotations'] = ((df['Frame Number'] - start_value) // 50).astype(int)

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
                        print(id_str)
                        try:
                            id_int = int(id_str)
                            print(annotation, id_int)
                            if id_int >= 0:
                                necessary_vertex.append(box_vertices_list[id_int].tolist())
                            else:
                                print(miss_gt_box_vertices)
                                print(miss_gt_box_vertices[-id_int - 1].tolist())
                                necessary_vertex.append(miss_gt_box_vertices[-id_int - 1].tolist())
                        except:
                            necessary_vertex.append('')
                            continue

            df['ROI 8 points'] = necessary_vertex

            # Remove unnecessary columns
            df.drop(['Frame Number', 'Selected Point Number', 'annotations'], axis=1, inplace=True)

            # Modify rows with Miss GT Issue
            df.loc[df['Issue'] == 'Miss GT Issue', 'Selected Points Class/Object'] = "[-1] th object ['UNLABELED']"

            name = f"{value.split('.xlsx')[0]}.csv"
            df.to_csv(os.path.join(save_path, name), index=False)
            print(f'{name} Done')

            return os.path.join(save_path, name)

if __name__ == '__main__':
    bucket_name = "coop-selectstar-7000527-241231/"
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
    step = "02_Inspection/"
    sensor = "01_IRIS_JX013/"
    space = "01_Highway/"

    date = '240906'
    print(step, sensor, space)

    drive = "C:/Users/pc/SS-233/HDC/"

    # STEP 1: Set base file
    try:
        middle_folder_name = os.listdir(f'{drive}/{bucket_name}/{step}/{sensor}/{space}/')[0]
        data_path = os.path.join(f'{drive}/{bucket_name}/{step}/{sensor}/{space}/', middle_folder_name, date)
        inspection_dir = os.path.join(f'{drive}/{bucket_name}/{step}/{sensor}/{space}/', middle_folder_name,
                                      'LDR_GT_Inspection')

    except:
        middle_folder_name = os.listdir(f'{drive}/{step}/{sensor}/{space}/')[0]
        data_path = os.path.join(f'{drive}/{step}/{sensor}/{space}/', middle_folder_name, date)
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
        # process_sequence(data_path, sequence, save_path)

