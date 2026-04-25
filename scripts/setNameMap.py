import json

def custom_sort_key(s: str):
    s_lower = s.lower()
    
    # Prioridad de caracteres:
    # "." primero, luego "_", luego letras normales
    s_priority = (
        s_lower
        .replace(".", " ")   # más prioritario
        .replace("_", "!")   # después del punto, pero antes de letras
    )
    
    return s_priority

# Rutas fijas de los archivos JSON
archivo_a = r"F:\\RtoM\\SecretsOfKhazadDum\\json\\Moria\\Content\\Tech\\Data\\Building\\DT_Constructions.json"
archivo_b = r"F:\\RtoM\\SecretsOfKhazadDum\\json\\Moria\\Content\\Tech\\Data\\Building\\DT_ConstructionRecipes.json"

# Leer listas desde los archivos JSON (asumiendo que la raíz es una lista)
with open(archivo_a, "r", encoding="utf-8") as f:
    data_a = json.load(f)

with open(archivo_b, "r", encoding="utf-8") as f:
    data_b = json.load(f)

# Ordenar NameMap alfabeticamente
data_a["NameMap"] = sorted(data_a["NameMap"], key=custom_sort_key)
data_b["NameMap"] = sorted(data_b["NameMap"], key=custom_sort_key)


with open(archivo_a, "w", encoding="utf-8") as f:
            json.dump(data_a, f, indent=2, ensure_ascii=False)
with open(archivo_b, "w", encoding="utf-8") as f:
            json.dump(data_b, f, indent=2, ensure_ascii=False)