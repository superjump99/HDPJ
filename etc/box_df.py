import numpy as np
import os
import pandas as pd
from function_set import Post_TRUNCATION as TRUNCATION

def save_truncation_df_to_excel(truncation_df, xlsx_path, sheet_name):
    if not os.path.exists(xlsx_path):
        with pd.ExcelWriter(xlsx_path, mode='w', engine='openpyxl') as writer:
            truncation_df.to_excel(writer, sheet_name=sheet_name, index=False)
    else:
        with pd.ExcelWriter(xlsx_path, mode='a', engine='openpyxl') as writer:
            truncation_df.to_excel(writer, sheet_name=sheet_name, index=False)

def process_json_file(json_file, base_path, field, xlsx_path):
    df = TRUNCATION.load_json_annotations(os.path.join(base_path, json_file))
    truncation_df = TRUNCATION.truncation(field, df)
    truncation_df['OCCLUSION'] = truncation_df['OCCLUSION'].astype(int)
    truncation_df = truncation_df.round(decimals=2)
    truncation_df = truncation_df.sort_values(by=['category'])
    truncation_df = truncation_df.drop(columns=['x', 'y', 'z', 'rotationYaw', 'truncation'])
    save_truncation_df_to_excel(truncation_df, xlsx_path, json_file[:6])

def main():
    os.chdir("C:/Users/pc/hyundai/input/HYUNDAI")
    dataset = os.listdir(os.getcwd())[0]
    print(dataset)

    base_path = os.path.join(f"{os.getcwd()}/{dataset}/annotations")
    xlsx_path = os.path.join(f"{os.getcwd()}/{dataset}", f'{dataset}.xlsx')

    field = np.array([(-1, 0), (20, 50), (120, 50), (120, -50), (20, -50), (-1, 0)])

    # 입력 폴더 내의 모든 JSON 파일 목록 가져오기
    json_files = [f for f in os.listdir(base_path) if f.endswith('.json')]

    for idx, json_file in enumerate(json_files):
        pcdfile_num = int(json_file[:6])
        if pcdfile_num % 2 == 1:
            print(idx)
            process_json_file(json_file, base_path, field, xlsx_path)

if __name__ == '__main__':
    main()
