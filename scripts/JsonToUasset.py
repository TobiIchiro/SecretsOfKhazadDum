import os
import subprocess

UASSETGUI_PATH = "F:/RtoM/UAssetGUI/UAssetGUI.exe"
ENGINE_VERSION = "VER_UE4_27"
ROOT_JSON = "f:/RtoM/SecretsOfKhazadDum/json"
DEST_ROOT = "f:/RtoM/SecretsOfKhazadDum/uasset"

for dirpath, _, filenames in os.walk(ROOT_JSON):
    for file in filenames:
        if not file.lower().endswith(".json"):
            continue

        source = os.path.join(dirpath, file)
        rel_path = os.path.relpath(dirpath, ROOT_JSON)
        dest_dir = os.path.join(DEST_ROOT, rel_path)
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, os.path.splitext(file)[0] + ".uasset")

        print(f"Converting: {source} -> {dest}")
        cmd = [UASSETGUI_PATH, "fromjson", source, dest, ENGINE_VERSION]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Error converting {file}")
            print(result.stderr)