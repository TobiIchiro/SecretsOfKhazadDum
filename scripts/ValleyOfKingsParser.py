import json
import csv

FILE_PATH = r"F:/RtoM/GameExports/Exports/Moria/Content/Tech/Data/Bubbles/GameWorldCatalog/BD_BB_Chapter3_ValleyOfKings.json"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    MorBubbleData = json.load(f)


InstancedMeshCatalog = MorBubbleData[0]["Properties"]["InstancedMeshCatalog"]["Batches"]

catalogParsed = []
for instance in InstancedMeshCatalog:
    Mesh = instance["Definition"]["Mesh"]["ObjectName"].strip("'").split("'")[1]