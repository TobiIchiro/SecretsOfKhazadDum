"""
spawn_wall_instances.py
-----------------------
Unreal Engine Python Script (UE 4.27)

Lee Suburbs_Wall_Thin_3x3m.json, aplica el offset de coordenadas,
filtra instancias inválidas y genera actores idénticos copiando la clase 
y configuración del actor base existente en el nivel.
"""

import unreal
import json
import math

# ─── CONFIGURACIÓN ────────────────────────────────────────────────────────────

JSON_PATH = "F:/RtoM/SecretsOfKhazadDum/bubbleData/TelcharForge/NonDest_Wall_3M_A.json"

# Offsets que se restan a cada instancia
OFFSET_X = 6300.0
OFFSET_Y = 200.0

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def find_base_actor(base_mesh_name):
    """
    Busca en el nivel un actor cuyo label contenga base_mesh_name.
    Devuelve el primer actor encontrado o None.
    """
    all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
    for actor in all_actors:
        label = actor.get_actor_label()
        if base_mesh_name in label:
            unreal.log(f"[WallSpawner] Actor base encontrado: '{label}'")
            return actor

    unreal.log_warning(
        f"[WallSpawner] No se encontró ningún actor con '{base_mesh_name}' en el nivel."
    )
    return None


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    # 1. Leer JSON
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    base_mesh_name = data.get("BaseMesh", "")
    instances      = data.get("Instances", [])

    unreal.log(
        f"[WallSpawner] BaseMesh: '{base_mesh_name}'  |  "
        f"Instancias en JSON: {len(instances)}"
    )

    # 2. Localizar el actor base en el nivel
    base_actor = find_base_actor(base_mesh_name)
    if base_actor is None:
        unreal.log_error("[WallSpawner] Abortando: actor base no encontrado en el nivel.")
        return

    # Obtener metadatos clave del actor original para replicarlos
    actor_class = base_actor.get_class()
    
    # Extraer el Static Mesh original si es un StaticMeshActor estándar
    source_mesh = None
    if isinstance(base_actor, unreal.StaticMeshActor):
        source_mesh = base_actor.static_mesh_component.static_mesh

    placed  = 0
    skipped = 0

    with unreal.ScopedEditorTransaction("Spawn Wall Instances (Native)"):
        for inst in instances:
            t  = inst["Transform"]
            tr = t["Translation"]
            rot = t["Rotation"]
            sc  = t["Scale3D"]

            # 3. Aplicar offset
            new_x = tr["X"] - OFFSET_X
            new_y = tr["Y"] - OFFSET_Y
            new_z = tr["Z"]

            # 4. Filtrar coordenadas negativas
            if new_x < 0 or new_y < 0:
                unreal.log_warning(
                    f"[WallSpawner] Ignorada '{inst['Name']}' "
                    f"→ X={new_x:.1f}, Y={new_y:.1f}"
                )
                skipped += 1
                continue

            # 5. Convertir cuaternión → Rotator (redondeado al grado más cercano)
            quat = unreal.Quat(rot["X"], rot["Y"], rot["Z"], rot["W"])
            r = quat.rotator()
            rotator = unreal.Rotator(round(r.roll), round(r.pitch), round(r.yaw))
            location = unreal.Vector(new_x, new_y, new_z)
            scale    = unreal.Vector(sc["X"], sc["Y"], sc["Z"])

            # 6. MÉTODO NATIVO DE GENERACIÓN PARA UE 4.27
            # Spawnea un actor limpio de la misma clase directamente en el nivel activo
            new_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
                actor_class, 
                location, 
                rotator
            )

            if not new_actor:
                unreal.log_error(
                    f"[WallSpawner] Fallo al spawnear actor para '{inst['Name']}'"
                )
                continue

            # 7. Replicar propiedades críticas (Visuales y de escala)
            new_actor.set_actor_scale3d(scale)
            
            # Si el actor base tenía un malla asignada, la copiamos al nuevo componente
            if source_mesh and hasattr(new_actor, 'static_mesh_component'):
                new_actor.static_mesh_component.set_static_mesh(source_mesh)
                
                # Copiar materiales aplicados elemento por elemento si existen overrides
                material_count = base_actor.static_mesh_component.get_num_materials()
                for i in range(material_count):
                    mat = base_actor.static_mesh_component.get_material(i)
                    if mat:
                        new_actor.static_mesh_component.set_material(i, mat)

            # Cambiar nombre en el Outliner
            new_actor.set_actor_label(f"{base_mesh_name}_Instance_{placed}")
            placed += 1

    unreal.log(
        f"[WallSpawner] ¡Listo! Revisa tu Viewport. "
        f"Colocados: {placed}  |  Ignorados: {skipped}  |  Total: {len(instances)}"
    )


if __name__ == "__main__":
    main()