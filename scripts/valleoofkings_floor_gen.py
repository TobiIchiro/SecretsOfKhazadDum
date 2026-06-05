import json
import copy

PATH_FILE = "F:/RtoM/SecretsOfKhazadDum/json/Moria/Content/Tech/Data/Bubbles/GameWorldCatalog/BD_BB_Chapter3_ValleyOfKings.json"


FLOOR_TEMPLATE = {
    "$type": "UAssetAPI.PropertyTypes.Structs.StructPropertyData, UAssetAPI",
    "StructType": "GlobalLevelMeshInstance",
    "SerializeNone": True,
    "StructGUID": "{00000000-0000-0000-0000-000000000000}",
    "SerializationControl": "NoExtension",
    "Operation": "None",
    "Name": "Instances",
    "ArrayIndex": 0,
    "IsZero": False,
    "PropertyTagFlags": "None",
    "PropertyTagExtensions": "NoExtension",
    "Value": [
        {
            "$type": "UAssetAPI.PropertyTypes.Objects.NamePropertyData, UAssetAPI",
            "Name": "Name",
            "ArrayIndex": 0,
            "IsZero": False,
            "PropertyTagFlags": "None",
            "PropertyTagExtensions": "NoExtension",
            "Value": "Suburbs_Gate_A_Pillar_Shaft1",
        },
        {
            "$type": "UAssetAPI.PropertyTypes.Structs.StructPropertyData, UAssetAPI",
            "StructType": "Transform",
            "SerializeNone": True,
            "StructGUID": "{00000000-0000-0000-0000-000000000000}",
            "SerializationControl": "NoExtension",
            "Operation": "None",
            "Name": "Transform",
            "ArrayIndex": 0,
            "IsZero": False,
            "PropertyTagFlags": "None",
            "PropertyTagExtensions": "NoExtension",
            "Value": [
                {
                    "$type": "UAssetAPI.PropertyTypes.Structs.StructPropertyData, UAssetAPI",
                    "StructType": "Quat",
                    "SerializeNone": True,
                    "StructGUID": "{00000000-0000-0000-0000-000000000000}",
                    "SerializationControl": "NoExtension",
                    "Operation": "None",
                    "Name": "Rotation",
                    "ArrayIndex": 0,
                    "IsZero": False,
                    "PropertyTagFlags": "None",
                    "PropertyTagExtensions": "NoExtension",
                    "Value": [
                        {
                            "$type": "UAssetAPI.PropertyTypes.Structs.QuatPropertyData, UAssetAPI",
                            "Name": "Rotation",
                            "ArrayIndex": 0,
                            "IsZero": False,
                            "PropertyTagFlags": "None",
                            "PropertyTagExtensions": "NoExtension",
                            "Value": {
                                "$type": "UAssetAPI.UnrealTypes.FQuat, UAssetAPI",
                                "X": "+0",
                                "Y": "+0",
                                "Z": "+0",
                                "W": 1.0,
                            },
                        }
                    ],
                },
                {
                    "$type": "UAssetAPI.PropertyTypes.Structs.StructPropertyData, UAssetAPI",
                    "StructType": "Vector",
                    "SerializeNone": True,
                    "StructGUID": "{00000000-0000-0000-0000-000000000000}",
                    "SerializationControl": "NoExtension",
                    "Operation": "None",
                    "Name": "Translation",
                    "ArrayIndex": 0,
                    "IsZero": False,
                    "PropertyTagFlags": "None",
                    "PropertyTagExtensions": "NoExtension",
                    "Value": [
                        {
                            "$type": "UAssetAPI.PropertyTypes.Structs.VectorPropertyData, UAssetAPI",
                            "Name": "Translation",
                            "ArrayIndex": 0,
                            "IsZero": False,
                            "PropertyTagFlags": "None",
                            "PropertyTagExtensions": "NoExtension",
                            "Value": {
                                "$type": "UAssetAPI.UnrealTypes.FVector, UAssetAPI",
                                "X": 1750.0,
                                "Y": 7450.0,
                                "Z": 800.0,
                            },
                        }
                    ],
                },
                {
                    "$type": "UAssetAPI.PropertyTypes.Structs.StructPropertyData, UAssetAPI",
                    "StructType": "Vector",
                    "SerializeNone": True,
                    "StructGUID": "{00000000-0000-0000-0000-000000000000}",
                    "SerializationControl": "NoExtension",
                    "Operation": "None",
                    "Name": "Scale3D",
                    "ArrayIndex": 0,
                    "IsZero": False,
                    "PropertyTagFlags": "None",
                    "PropertyTagExtensions": "NoExtension",
                    "Value": [
                        {
                            "$type": "UAssetAPI.PropertyTypes.Structs.VectorPropertyData, UAssetAPI",
                            "Name": "Scale3D",
                            "ArrayIndex": 0,
                            "IsZero": False,
                            "PropertyTagFlags": "None",
                            "PropertyTagExtensions": "NoExtension",
                            "Value": {
                                "$type": "UAssetAPI.UnrealTypes.FVector, UAssetAPI",
                                "X": 1.0,
                                "Y": 1.0,
                                "Z": 1.0,
                            },
                        }
                    ],
                },
            ],
        },
    ],
}
FLOOR_TEMPLATE_2 = {
    "$type": "UAssetAPI.PropertyTypes.Structs.StructPropertyData, UAssetAPI",
    "StructType": "GlobalLevelMeshInstance",
    "SerializeNone": True,
    "StructGUID": "{00000000-0000-0000-0000-000000000000}",
    "SerializationControl": "NoExtension",
    "Operation": "None",
    "Name": "Instances",
    "ArrayIndex": 0,
    "IsZero": False,
    "PropertyTagFlags": "None",
    "PropertyTagExtensions": "NoExtension",
    "Value": [
        {
            "$type": "UAssetAPI.PropertyTypes.Objects.NamePropertyData, UAssetAPI",
            "Name": "Name",
            "ArrayIndex": 0,
            "IsZero": False,
            "PropertyTagFlags": "None",
            "PropertyTagExtensions": "NoExtension",
            "Value": "Suburbs_Gate_A_Pillar_Shaft1",
        },
        {
            "$type": "UAssetAPI.PropertyTypes.Structs.StructPropertyData, UAssetAPI",
            "StructType": "Transform",
            "SerializeNone": True,
            "StructGUID": "{00000000-0000-0000-0000-000000000000}",
            "SerializationControl": "NoExtension",
            "Operation": "None",
            "Name": "Transform",
            "ArrayIndex": 0,
            "IsZero": False,
            "PropertyTagFlags": "None",
            "PropertyTagExtensions": "NoExtension",
            "Value": [
                {
                    "$type": "UAssetAPI.PropertyTypes.Structs.StructPropertyData, UAssetAPI",
                    "StructType": "Quat",
                    "SerializeNone": True,
                    "StructGUID": "{00000000-0000-0000-0000-000000000000}",
                    "SerializationControl": "NoExtension",
                    "Operation": "None",
                    "Name": "Rotation",
                    "ArrayIndex": 0,
                    "IsZero": False,
                    "PropertyTagFlags": "None",
                    "PropertyTagExtensions": "NoExtension",
                    "Value": [
                        {
                            "$type": "UAssetAPI.PropertyTypes.Structs.QuatPropertyData, UAssetAPI",
                            "Name": "Rotation",
                            "ArrayIndex": 0,
                            "IsZero": False,
                            "PropertyTagFlags": "None",
                            "PropertyTagExtensions": "NoExtension",
                            "Value": {
                                "$type": "UAssetAPI.UnrealTypes.FQuat, UAssetAPI",
                                "X": "+0",
                                "Y": "+0",
                                "Z": 1.0,
                                "W": 0.0,
                            },
                        }
                    ],
                },
                {
                    "$type": "UAssetAPI.PropertyTypes.Structs.StructPropertyData, UAssetAPI",
                    "StructType": "Vector",
                    "SerializeNone": True,
                    "StructGUID": "{00000000-0000-0000-0000-000000000000}",
                    "SerializationControl": "NoExtension",
                    "Operation": "None",
                    "Name": "Translation",
                    "ArrayIndex": 0,
                    "IsZero": False,
                    "PropertyTagFlags": "None",
                    "PropertyTagExtensions": "NoExtension",
                    "Value": [
                        {
                            "$type": "UAssetAPI.PropertyTypes.Structs.VectorPropertyData, UAssetAPI",
                            "Name": "Translation",
                            "ArrayIndex": 0,
                            "IsZero": False,
                            "PropertyTagFlags": "None",
                            "PropertyTagExtensions": "NoExtension",
                            "Value": {
                                "$type": "UAssetAPI.UnrealTypes.FVector, UAssetAPI",
                                "X": 1750.0,
                                "Y": 7450.0,
                                "Z": 800.0,
                            },
                        }
                    ],
                },
                {
                    "$type": "UAssetAPI.PropertyTypes.Structs.StructPropertyData, UAssetAPI",
                    "StructType": "Vector",
                    "SerializeNone": True,
                    "StructGUID": "{00000000-0000-0000-0000-000000000000}",
                    "SerializationControl": "NoExtension",
                    "Operation": "None",
                    "Name": "Scale3D",
                    "ArrayIndex": 0,
                    "IsZero": False,
                    "PropertyTagFlags": "None",
                    "PropertyTagExtensions": "NoExtension",
                    "Value": [
                        {
                            "$type": "UAssetAPI.PropertyTypes.Structs.VectorPropertyData, UAssetAPI",
                            "Name": "Scale3D",
                            "ArrayIndex": 0,
                            "IsZero": False,
                            "PropertyTagFlags": "None",
                            "PropertyTagExtensions": "NoExtension",
                            "Value": {
                                "$type": "UAssetAPI.UnrealTypes.FVector, UAssetAPI",
                                "X": 1.0,
                                "Y": 1.0,
                                "Z": 1.0,
                            },
                        }
                    ],
                },
            ],
        },
    ],
}

with open(PATH_FILE, "r", encoding="utf-8") as f:
    data_a = json.load(f)

floors = data_a["Exports"][0]["Data"][0]["Value"][0]["Value"][-32]["Value"][1]["Value"]
k = 0
z = 900.0 + 200 + 300 + 100
y = 8112.5 + 100
for i in range(0, 5):
    a = copy.deepcopy(FLOOR_TEMPLATE)
    a["Value"][0]["Value"] = f"SM_AR_Suburbs_BaseTrim_050x300x100_A{i+21}"
    x = 1450 - 300 * i


    a["Value"][1]["Value"][1]["Value"][0]["Value"]["X"] = x
    a["Value"][1]["Value"][1]["Value"][0]["Value"]["Y"] = y
    a["Value"][1]["Value"][1]["Value"][0]["Value"]["Z"] = z

    floors.append(a)

y = 7087.5 - 100
for i in range(0, 5):
    a = copy.deepcopy(FLOOR_TEMPLATE_2)
    a["Value"][0]["Value"] = f"SM_AR_Suburbs_BaseTrim_050x300x100_A{i+26}"
    x = 1450 - 300 * i


    a["Value"][1]["Value"][1]["Value"][0]["Value"]["X"] = x
    a["Value"][1]["Value"][1]["Value"][0]["Value"]["Y"] = y
    a["Value"][1]["Value"][1]["Value"][0]["Value"]["Z"] = z

    floors.append(a)

with open(PATH_FILE, "w", encoding="utf-8") as f:
    json.dump(data_a, f, indent=2, ensure_ascii=False)
