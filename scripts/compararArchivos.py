from pathlib import Path

# ==========================
# CONFIGURACIÓN
# ==========================
DIR_A = r"F:\RtoM\SecretsOfKhazadDum\uasset\Moria\Content\Mods"
DIR_B = r"F:\RtoM\Moria Replication Project\Moria-Replication\project\Content\Mods"

# Cambiar a False si quieres distinguir mayúsculas/minúsculas
IGNORE_CASE = True

# ==========================

def obtener_archivos(base):
    base = Path(base)
    archivos = {}

    for archivo in base.rglob("*"):
        if archivo.is_file():
            ruta = archivo.relative_to(base).as_posix()

            clave = ruta.lower() if IGNORE_CASE else ruta
            archivos[clave] = ruta  # Conserva el nombre original

    return archivos

archivos_a = obtener_archivos(DIR_A)
archivos_b = obtener_archivos(DIR_B)

iguales = sorted(set(archivos_a.keys()) & set(archivos_b.keys()))

print("=" * 60)
print("Archivos presentes en ambos directorios")
print("=" * 60)

if iguales:
    for archivo in iguales:
        print(archivos_a[archivo])
else:
    print("No hay archivos en común.")

print()
print(f"Total de archivos iguales: {len(iguales)}")