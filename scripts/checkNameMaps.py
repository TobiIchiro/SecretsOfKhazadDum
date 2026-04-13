import json

# Rutas fijas de los archivos JSON
archivo_a = r"F:\\RtoM\\SecretsOfKhazadDum\\json\\Moria\\Content\\Tech\\Data\\Building\\DT_Constructions.json"
archivo_b = r"C:\\Users\\israe\\AppData\\Local\\RtoMModTools\\TobisMod\\json_data\\Moria\\Content\\Tech\\Data\\Building\\DT_Constructions.json"

# Leer listas desde los archivos JSON (asumiendo que la raíz es una lista)
with open(archivo_a, "r", encoding="utf-8") as f:
    data_a = json.load(f)
with open(archivo_b, "r", encoding="utf-8") as f:
    data_b = json.load(f)

# Ordenar las listas alfabéticamente
lista_a_ordenada = sorted(data_a["NameMap"])
lista_b_ordenada = sorted(data_b["NameMap"])

# Elementos en A que no están en B
solo_en_a = sorted(set(lista_a_ordenada) - set(lista_b_ordenada))

# Elementos en B que no están en A
solo_en_b = sorted(set(lista_b_ordenada) - set(lista_a_ordenada))

# Escribir resultados en un archivo TXT
with open("diferencias.txt", "w", encoding="utf-8") as f:
    f.write("Elementos en A y no en B:\n")
    for item in solo_en_a:
        f.write(f"{item}\n")
    f.write("\nElementos en B y no en A:\n")
    for item in solo_en_b:
        f.write(f"{item}\n")

print("Archivo 'diferencias.txt' generado correctamente.")