import os
import Pre_04_rename_files as rename_files


def find_files_with_remainder_zero(folder_path):  # 25로 나눠지는 파일만 가져가기

    for filename in os.listdir(folder_path):
        if filename.endswith('.pcdbin'):
            file_number = int(filename.split('.')[0])
            if file_number % 25 != 0:
                os.remove(os.path.join(folder_path, filename))

        if filename.endswith('.jpg'):
            file_number = int(filename.split('.')[0])
            if file_number % 25 != 0:
                os.remove(os.path.join(folder_path, filename))
    return


if __name__ == '__main__':

    s3_path = 'S3_hyundai'
    step_path = 'step1'

    given_data_path = '0.given_data'
    div_remove_path = '1.div&remove'

    space = "01_Hightway"
    dataset = "HKMC-N2202209-240208"

    os.chdir('../../../')
    base_path = os.path.join(f"{os.getcwd()}/{s3_path}/{step_path}/")

    for i, sequence_set in enumerate(os.listdir(f"{base_path}/{div_remove_path}/{space}/{dataset}")):
        div_folder = f"{base_path}/{div_remove_path}/{space}/{dataset}/{sequence_set}"
        PCDBIN_folder = f"{div_folder}/pcd bin"
        imageFC_folder = f"{div_folder}/images/CAM_FRONT"
        imageFR_folder = f"{div_folder}/images/CAM_FRONT_RIGHT"
        imageFL_folder = f"{div_folder}/images/CAM_FRONT_LEFT"
        find_files_with_remainder_zero(PCDBIN_folder)
        # rename_files(PCDBIN_folder)

        find_files_with_remainder_zero(imageFC_folder)
        rename_files.rename_files(imageFC_folder)

        find_files_with_remainder_zero(imageFR_folder)
        rename_files.rename_files(imageFR_folder)

        find_files_with_remainder_zero(imageFL_folder)
        rename_files.rename_files(imageFL_folder)
