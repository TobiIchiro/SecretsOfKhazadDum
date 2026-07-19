from pathlib import Path

# ==========================
# CONFIGURACIÓN
# ==========================
DIR_A = r"F:\RtoM\Moria Replication Project\Moria-Replication\project\Content\Mods"
DIR_B = r"F:\RtoM\Unreal Engine Projects\Moria\Content\Mods"

# Cambiar a False si quieres distinguir mayúsculas/minúsculas
IGNORE_CASE = True

# ==========================

def obtener_archivos(base):
    base = Path(base)
    archivos = set()

    for archivo in base.rglob("*"):
        if archivo.is_file():
            ruta = archivo.relative_to(base).as_posix()

            if IGNORE_CASE:
                ruta = ruta.lower()

            archivos.add(ruta)

    return archivos

archivos_a = obtener_archivos(DIR_A)
archivos_b = obtener_archivos(DIR_B)

solo_a = sorted(archivos_a - archivos_b)
solo_b = sorted(archivos_b - archivos_a)

print("=" * 60)
print("Archivos presentes en Replication pero NO en UE Project")
print("=" * 60)

if solo_a:
    for archivo in solo_a:
        print(archivo)
else:
    print("Ninguno")

print()
print("=" * 60)
print("Archivos presentes en UE Project pero NO en Replication")
print("=" * 60)

if solo_b:
    for archivo in solo_b:
        print(archivo)
else:
    print("Ninguno")

print()
print("=" * 60)
print(f"Solo en A: {len(solo_a)}")
print(f"Solo en B: {len(solo_b)}")