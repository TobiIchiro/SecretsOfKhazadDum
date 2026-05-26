import subprocess 

PATH_FILE = "F:/RtoM/SecretsOfKhazadDum/json/Moria/Content/Tech/Data/Bubbles/GameWorldCatalog/BD_BB_Chapter3_ValleyOfKings.json"
PATH_DST = "F:/RtoM/SecretsOfKhazadDum/uasset/Moria/Content/Tech/Data/Bubbles/GameWorldCatalog/BD_BB_Chapter3_ValleyOfKings.uasset"
UASSETGUI_PATH = "F:/RtoM/UAssetGUI/UAssetGUI.exe"
ENGINE_VERSION = "VER_UE4_27"

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


convert_file(PATH_FILE, PATH_DST)