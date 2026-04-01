import os
import subprocess

UNREALPAK_PATH = "F:/Programas/UE_4.27/Engine/Binaries/Win64/UnrealPak.exe"
INPUT_PATH = "F:/RtoM/SecretsOfKhazadDum/uasset"
DESTINATION_PATH = "F:/RtoM/SecretsOfKhazadDum/Pack"
PACK_LIST_PATH = "F:/RtoM/SecretsOfKhazadDum/scripts/Paklist.txt"
RETOC_PATH = "F:/RtoM/retoc-x86_64-pc-windows-msvc/retoc.exe"

UE_VERSION = "UE4_27"

# Create SecratsOfKhazadDum_LocTags.pak
locTagPath = os.path.join(DESTINATION_PATH,"SecratsOfKhazadDum_LocTags_P.pak")
cmd = [UNREALPAK_PATH, locTagPath, f"-create{PACK_LIST_PATH}"]
result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode != 0:
            print("Error converting")
            print(result.stderr)

# Create SecratsOfKhazadDum.pak, SecratsOfKhazadDum.ucas, SecratsOfKhazadDum.utoc
modPath = os.path.join(DESTINATION_PATH, "SecratsOfKhazadDum_P.utoc")
cmd = [RETOC_PATH, "to-zen", "--version", UE_VERSION, INPUT_PATH, modPath]
result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode != 0:
            print("Error converting")
            print(result.stderr)