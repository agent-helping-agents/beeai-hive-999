import os
import json
import time

def map_drive(mount_point):
    structure = {}
    for root, dirs, files in os.walk(mount_point):
        structure[root] = {"dirs": dirs, "files": files}
    return structure

if __name__ == "__main__":
    mount_point = "/media/batman/2e5c0fde-0328-49e4-8d37-dd18be027734/"
    drive_map = map_drive(mount_point)
    with open("/home/batman/Documents/augment-projects/Baker-Street-Laboratory/research/drive_map.json", "w") as f:
        json.dump(drive_map, f, indent=4)
    print("Drive mapping completed and saved to research/drive_map.json")