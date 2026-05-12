import json
import os

PATH_BASE = r"C:\Users\israe\AppData\Local\RtoMModTools\data\Tobis_json\DT_ItemRecipes"

archivo_a = r"F:\RtoM\SecretsOfKhazadDum\json\Moria\Content\Tech\Data\Items\DT_ItemRecipes.json"

START = 390
END = 466

with open(archivo_a, "r", encoding="utf-8") as f:
    data_a = json.load(f)

data = data_a["Exports"][0]["Table"]["Data"]

print(data[-33]["Name"])

for i in range(START, END):

    const = data[i]
    name = const["Name"]

    path_file = os.path.join(PATH_BASE, f"{name}.json")

    if not os.path.exists(path_file):
        print(f"No existe: {path_file}")
        continue

    with open(path_file, "r", encoding="utf-8") as f:
        ind_const = json.load(f)

    ind_const["Row"] = const

    with open(path_file, "w", encoding="utf-8") as f:
        json.dump(ind_const, f, indent=2, ensure_ascii=False)

    print(f"Actualizado: {name}")