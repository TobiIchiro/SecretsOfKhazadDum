import unreal

def static_meshes_to_bubble_data(bubble_data_path: str, map_name: str):
    """
    Lee solo los StaticMeshActors dentro de la carpeta
    '{map_name}/BubbleData/staticMeshes' del World Outliner.
    """

    bubble_data = unreal.load_asset(bubble_data_path)
    if not bubble_data:
        unreal.log_error(f"No se pudo cargar: {bubble_data_path}")
        return

    # Carpeta objetivo en el Outliner
    target_folder = "BubbleData"

    all_actors = unreal.EditorLevelLibrary.get_all_level_actors()

    # Filtrar por tipo Y por carpeta del Outliner
    sma_list = [
        a for a in all_actors
        if isinstance(a, unreal.StaticMeshActor)
        and str(a.get_folder_path()) == target_folder
    ]

    if not sma_list:
        unreal.log_warning(
            f"No se encontraron StaticMeshActors en '{target_folder}'"
        )
        return

    unreal.log(f"Encontrados {len(sma_list)} actores en '{target_folder}'")

    # Agrupar por (mesh + materiales + collision)
    batches: dict = {}

    for actor in sma_list:
        smc = actor.static_mesh_component
        if not smc:
            continue

        mesh = smc.static_mesh
        if not mesh:
            continue

        num_mats = smc.get_num_materials()
        materials = [smc.get_material(i) for i in range(num_mats)]
        mat_paths = tuple(
            m.get_path_name() if m else "None" for m in materials
        )
        collision_profile = smc.get_collision_profile_name()

        key = (mesh.get_path_name(), mat_paths, str(collision_profile))

        if key not in batches:
            batches[key] = {
                "mesh": mesh,
                "materials": materials,
                "collision_profile": collision_profile,
                "smc_ref": smc,
                "actors": []
            }
        batches[key]["actors"].append(actor)

    # Construir Batches
    new_batches = []

    for key, data in batches.items():
        mesh      = data["mesh"]
        materials = data["materials"]
        actors    = data["actors"]
        smc_ref   = data["smc_ref"]

        definition = unreal.GlobalInstantiableMesh()
        definition.set_editor_property("Mesh", mesh)
        definition.set_editor_property("Materials", materials)
        definition.set_editor_property("CollisionProfile", data["collision_profile"])
        definition.set_editor_property("bAffectNavigation", False)
        definition.set_editor_property("bReceivesDecals", True)
        definition.set_editor_property("bBigCharactersBreak", False)
        definition.set_editor_property("NumCustomDataFloats", 0)
        definition.set_editor_property("LightingChannels", 
            unreal.LightingChannels(channel0=True, channel1=False, channel2=False))

        instances = []
        for actor in actors:
            inst           = unreal.GlobalLevelMeshInstance()
            inst.name      = unreal.Name(actor.get_actor_label())
            inst.transform = actor.get_actor_transform()
            instances.append(inst)

        batch            = unreal.GlobalLevelInstancedMeshBatch()
        batch.definition = definition
        batch.instances  = instances
        new_batches.append(batch)

        unreal.log(
            f"  Batch '{mesh.get_name()}' "
            f"[{len(materials)} mats | col={data['collision_profile']}] "
            f"→ {len(actors)} instancias"
        )

    # Guardar en el DataAsset
    bubble_data.instanced_mesh_catalog.batches = new_batches
    unreal.EditorAssetLibrary.save_asset(bubble_data_path)

    unreal.log(
        f"BubbleData actualizado: {len(new_batches)} batches, "
        f"{sum(len(b.instances) for b in new_batches)} instancias totales."
    )


# ── Uso ──────────────────────────────────────────────────────────────────────
static_meshes_to_bubble_data(
    bubble_data_path = "/Game/Tech/Data/Bubbles/GameWorldCatalog/BD_BB_TelcharForge",
    map_name         = "BB_TelcharForge_BD_Placement"
)