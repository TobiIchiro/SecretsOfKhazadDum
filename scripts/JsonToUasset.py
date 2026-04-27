import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

UASSETGUI_PATH = "F:/RtoM/UAssetGUI/UAssetGUI.exe"
ENGINE_VERSION = "VER_UE4_27"
ROOT_JSON = "f:/RtoM/SecretsOfKhazadDum/json"
DEST_ROOT = "f:/RtoM/SecretsOfKhazadDum/uasset"
ERROR_LOG = "conversion_errors.txt"

MAX_WORKERS = 6  # ajusta según pruebas

def convert_file(source, dest):
    cmd = [UASSETGUI_PATH, "fromjson", source, dest, ENGINE_VERSION]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        return {
            "success": False,
            "source": source,
            "error": result.stderr
        }

    return {
        "success": True,
        "source": source,
        "error": None
    }

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

errors = []

# Ejecutar en paralelo
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = [executor.submit(convert_file, src, dst) for src, dst in tasks]

    for future in as_completed(futures):
        result = future.result()

        if result["success"]:
            print(f"✔ Converted: {result['source']}")
        else:
            print(f"✖ Error: {result['source']}")
            errors.append(result)

# Guardar errores en archivo
if errors:
    with open(ERROR_LOG, "w", encoding="utf-8") as f:
        for err in errors:
            f.write(f"FILE: {err['source']}\n")
            f.write("ERROR:\n")
            f.write(err["error"] or "No error message")
            f.write("\n" + "-"*50 + "\n")

    print(f"\nSe encontraron {len(errors)} errores. Revisa: {ERROR_LOG}")
else:
    print("\nAll files have been converted successfully")