import json

FILE_PATH = "F:/RtoM/SecretsOfKhazadDum/json/Moria/Content/Tech/Data/Building/DT_Constructions.json"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    data_a = json.load(f)


for i in range (-1647, -2293, -2):
    data_a["Exports"][0]["SerializationBeforeCreateDependencies"].append(i)

with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data_a, f, indent=2, ensure_ascii=False)