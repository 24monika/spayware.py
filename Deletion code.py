import os
import shutil
import time

def delete_folder_if_accessed(folder_path):
    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} does not exist.")
        return
    initial_access_time = os.path.getatime(folder_path)

    try:
        while True:
            current_access_time = os.path.getatime(folder_path)
            if current_access_time != initial_access_time:
                # Added os.path.realpath to fix the issue with symlinks
                shutil.rmtree(os.path.realpath(folder_path))
                break
            else:
                time.sleep(1)
    except FileNotFoundError:
        print("...")
    except KeyboardInterrupt:
        print("Program interrupted by user.")
    except Exception as e:
        print(f"Error: {e}")

if _name_ == "_main_":
    folder_to_monitor = r"#your folders path"
    delete_folder_if_accessed(folder_to_monitor)