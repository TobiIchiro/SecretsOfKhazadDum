import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

UASSETGUI_PATH = "F:/RtoM/UAssetGUI/UAssetGUI.exe"
ENGINE_VERSION = "VER_UE4_27"
ROOT_JSON = "f:/RtoM/SecretsOfKhazadDum/json"
DEST_ROOT = "f:/RtoM/SecretsOfKhazadDum/uasset"

MAX_WORKERS = 4  # o prueba con 4, 8, etc.

def convert_file(source, dest):
    cmd = [UASSETGUI_PATH, "fromjson", source, dest, ENGINE_VERSION]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        return (False, source, result.stderr)
    return (True, source, None)

tasks = []

# Recolectar tareas
for dirpath, _, filenames in os.walk(ROOT_JSON):
    for file in filenames:
        if not file.lower().endswith(".json"):
            continue

        source = os.path.join(dirpath, file)
        rel_path = os.path.relpath(dirpath, ROOT_JSON)
        dest_dir = os.path.join(DEST_ROOT, rel_path)
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, os.path.splitext(file)[0] + ".uasset")

        tasks.append((source, dest))

# Ejecutar en paralelo
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = [executor.submit(convert_file, src, dst) for src, dst in tasks]

    for future in as_completed(futures):
        success, source, error = future.result()
        
        if success:
            print(f"✔ Converted: {source}")
        else:
            print(f"✖ Error: {source}")
            print(error)