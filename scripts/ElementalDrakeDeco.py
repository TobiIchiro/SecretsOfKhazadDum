import os

BASE_PATH = r"F:\RtoM\SecretsOfKhazadDum\json\Moria\Content\Mods\HuntersLodgePack\Constructions"

ELEMENTS = ["Poison", "Shadow", "Fire"]
ORIGINAL = "Frost"

OLD_PATH = "/Game/CharacterArt/Creatures/Drake/"
NEW_PATH = "/Game/Mods/HuntersLodgePack/Creatures/Drakes/Materials/"

def process_files():
    for file in os.listdir(BASE_PATH):
        if not file.endswith(".json"):
            continue
        
        if f"_{ORIGINAL}_" not in file:
            continue

        original_path = os.path.join(BASE_PATH, file)

        with open(original_path, "r", encoding="utf-8") as f:
            content = f.read()

        for element in ELEMENTS:
            # Nuevo nombre de archivo
            new_filename = file.replace(ORIGINAL, element)
            new_path = os.path.join(BASE_PATH, new_filename)

            # Modificar contenido
            new_content = content

            # 1. Frost -> Elemento
            new_content = new_content.replace(ORIGINAL, element)

            # 2. Ruta
            new_content = new_content.replace(OLD_PATH, NEW_PATH)

            # 3. Material específico
            new_content = new_content.replace(
                "MI_Drake_Chest",
                f"MI_{element}_Drake_Chest"
            )

            new_content = new_content.replace(
                "MI_Drake_Head",
                f"MI_{element}_Drake_Head"
            )

            new_content = new_content.replace(
                "MI_Drake_Tail",
                f"MI_{element}_Drake_Tail"
            )

            # Guardar nuevo archivo
            with open(new_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            print(f"Creado: {new_filename}")

if __name__ == "__main__":
    process_files()