import shutil
import os

def copy_property(target_path):
    HDC_dir = os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
    os.chdir(HDC_dir)
    etc_dir = os.path.join(HDC_dir, 'etc')
    print(etc_dir)

    files_to_copy = [f for f in os.listdir(etc_dir) if f.endswith('.xlsx') or f.endswith('.txt')]

    # # 파일을 복사합니다.
    for file_name in files_to_copy:
        src_file = os.path.join(etc_dir, file_name)
        dst_file = os.path.join(target_path, file_name)

        try:
            shutil.copy(src_file, dst_file)
            print(f"{file_name} has been copied to {target_path}")
        except Exception as e:
            print(f"Failed to copy {file_name}: {e}")

if __name__ == '__main__':
    pass