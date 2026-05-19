# Porter Goat — Follow-up Design (Persistor + Proximity Menu)

Hi Tobi — this doc covers the two remaining items from the porter-goat priority list (5 and 6). Both require some authoring inside the UE4 editor because they touch a Blueprint class graph, which can't be safely authored from JSON alone. Below is the exact spec for each so you can do the editor work and then commit the resulting JSON through your usual `JsonToUasset.py` / `PackMod.py` pipeline.

I'm opening this PR as an **RFC / design proposal** — happy to adjust before any implementation. Nothing in here changes a `.uasset` yet.

---

## Branch and base

This PR is opened against `Goat-npc` (the active goat branch). Not `main`, which doesn't carry the goat content.

---

## Item 5 — `BP_PorterGoatPersistor`

### Why we need it

When the player saves and reloads, the porter goat's runtime state needs to persist (identity, last position, role, alive flag, etc.). Vanilla NPC actors that survive saves implement the `MorSaveGameObjectCallbacks` interface from `/Script/Moria`. `BP_NpcGoat` does not implement it as shipped, so a separate small actor — `BP_PorterGoatPersistor` — gets spawned alongside the goat at summon time and acts as the goat's save participant.

A separate actor (rather than modifying `BP_NpcGoat` directly) keeps the override on `BP_NpcGoat` minimal and avoids re-cooking the heavier goat BP when only the save schema changes.

### Asset to create

| Field          | Value                                                                  |
|----------------|------------------------------------------------------------------------|
| Path           | `/Game/Mods/PorterGoat/Persistor/BP_PorterGoatPersistor`               |
| Parent class   | `AActor` (vanilla, no custom parent)                                   |
| Implements     | `MorSaveGameObjectCallbacks` (from `/Script/Moria`)                    |
| Components     | None required (no mesh, no collision)                                  |
| Tick           | Disabled (`Actor Tick` → uncheck "Start with Tick Enabled")            |

### Member variables (all 7 marked "Save Game")

| Variable             | Type       | Purpose                                                  |
|----------------------|------------|----------------------------------------------------------|
| `GoatGuid`           | Guid       | Unique identity per goat instance; assigned on first spawn |
| `GoatName`           | Name       | Optional display name override                            |
| `GoatRole`           | Name       | DT_NPCRoles row name (`Porter`)                           |
| `LastKnownLocation`  | Vector     | World location at last save (for re-summon after reload)  |
| `LastKnownRotation`  | Rotator    | Facing direction at last save                             |
| `bIsAlive`           | Boolean    | Alive flag                                                |
| `SaveTimestamp`      | DateTime   | When this record was last written (for debugging)         |

For each variable in the Variable Details panel: scroll to the **Save Game** flag and check it. Variables not flagged `SaveGame` won't be serialized by the engine's default `USaveGame` machinery.

### Interface methods

Adding `MorSaveGameObjectCallbacks` will auto-create stub functions in the BP for each interface method. **Leave the function bodies empty for v1.** UE4's default property serialization handles the actual read/write when properties are flagged `SaveGame`; the interface hooks exist so the engine knows the actor opts into the save pipeline.

If the interface signature includes a version method (e.g. `GetSaveDataVersion`), return `1`.

### Editor steps

1. Content Browser → navigate to `/Game/Mods/PorterGoat/`
2. Create subfolder `Persistor/`
3. Right-click in the new folder → Blueprint Class → choose **Actor** → name `BP_PorterGoatPersistor`
4. Open the BP, then Class Settings → **Interfaces** → **Add** → `MorSaveGameObjectCallbacks`
5. Compile (interface stubs auto-add)
6. Variables tab → add the 7 variables above with the exact names and types listed
7. For each variable: in Details panel, check the **Save Game** flag
8. Class Defaults → **Actor Tick** → uncheck "Start with Tick Enabled"
9. Compile + Save
10. Run your usual tojson step on the cooked uasset → commit `json/Moria/Content/Mods/PorterGoat/Persistor/BP_PorterGoatPersistor.json`

### Runtime wiring (out of scope for this PR)

The persistor is spawned by UE4SS-side code at goat-summon time and attached to the goat. The runtime contract:

```
on_summon_goat():
    goat = SpawnActor(BP_NpcGoat_C, player_location)
    persistor = SpawnActor(BP_PorterGoatPersistor_C)
    persistor.GoatGuid = GenerateGuid()
    persistor.AttachToActor(goat)
    persistor.GoatRole = "Porter"
```

This is documented for future runtime work — not part of this PR.

---

## Item 6 — Goat Proximity Menu

### What we want

When the player walks up to the porter goat and presses the interact key, a small menu opens with options:

1. **Open Inventory** — show the goat's saddlebag grid (you already have `BP_SaddleBags_Goat` and `BP_ContainerItem_Goat_Slot_EpicPack` wired into inventory storage)
2. **Dismiss** — despawn the goat (the bell summon path can re-spawn it later)
3. *(optional flavor)* **Pet**

### Architecture finding

I traced how Moria does proximity menus by looking at `BP_NpcGoat.json` on `Goat-npc`. It uses these `/Script/Moria` C++ types:

- `MorNpcOnManageInteraction` — opens the proximity menu when the player looks at the NPC
- `MorNpcOnManageLocalInteraction` — handles the local-player interaction request
- `MorInteraction` — base class for each menu entry
- `MorNpcBaseSelectionRequest` — the selection-UI side
- `MorViewTrigger` — view-based "look at me" trigger

**Conclusion: the proximity menu is BP/component-driven, not DataTable-driven.** Adding goat menu entries means editing `BP_NpcGoat`'s graph to add `MorInteraction` instances (or equivalent BP nodes) with appropriate display labels and on-trigger logic.

There is no DataTable I can edit via JSON to add menu entries — this part requires editor work in the `BP_NpcGoat` graph itself.

### Existing reference assets to clone the pattern from

`BP_NpcGoat.json` references `WBP_UI_Inventory_Screen_StorageMode` in its NameMap, which suggests "open inventory in storage mode" is already partially wired in vanilla — the saddlebag inventory UI likely opens through that widget. Tracing that wiring in the editor will show whether the "Open Inventory" menu entry can reuse an existing event or needs new graph nodes.

For the **Dismiss** entry, the despawn path is the inverse of the summon path: destroy the goat actor and the attached persistor, but keep the persistor's save data so re-summon restores state.

### What I'd like from you

Before opening an implementation PR for the menu, I'd appreciate confirmation on a couple of things:

1. **Where to author**: do you want the proximity menu entries added directly to your existing `BP_NpcGoat` override, or in a small auxiliary BP that piggybacks via component attachment? Both are valid; direct edit is simpler, the auxiliary approach keeps `BP_NpcGoat` cleaner for future merges from vanilla updates.
2. **Inventory entry semantics**: is the goal that "Open Inventory" opens the saddlebag grid in the same UI the dwarves use for `BP_EpicPack_AdventurersPack_Large`, or a goat-specific widget? Reusing the dwarf pack UI is the lowest-effort path.
3. **Labels**: where would you like the new labels (`Open Inventory`, `Dismiss`, optionally `Pet`)? Options:
   - A new section in your existing `ST_Mod_Interactables` (mixing with the 100Buildings entries already there)
   - Inside `ST_PorterGoatStrings` (the goat-specific StringTable, which currently only ships in the cooked Assets pak — not yet in source)
   - Vanilla `ST_NPCRoles` or similar (probably wrong, since these are goat-specific)
   
   My recommendation: add to `ST_PorterGoatStrings` and surface that StringTable in the GitHub source tree alongside the new menu entries, so it's all versioned together.

Once you confirm those three, I can open a separate implementation PR with the actual menu wiring spec — or, if you'd rather do it in editor, I'll write up the same level of step-by-step instructions as I did for the persistor above.

---

## Heads-up: pre-existing bug worth flagging

Unrelated to items 5 and 6, while tracing the architecture I noticed a small bug in `Goat-npc` `DT_EpicPacks.json` that's still present as of `Goat-v1.2.0`:

The `BP_SaddleBags_Goat` row has its display strings pointing to **bell** keys:

```
"Value": "Container.PorterGoatBell.Name"
"Value": "Container.PorterGoatBell.Description"
```

These were almost certainly meant to be saddlebag keys (something like `EpicPacks.SaddleBags.Goat.Name` / `.Description`, which is what they were before this got swapped, or new keys you'd prefer). The runtime symptom: when the player examines the saddlebag, they'll see the bell's name and description, not the saddlebag's.

Easy fix in a separate small PR if you'd like, or I can roll it into the persistor PR once you confirm the right keys.

---

## Summary

| Item               | State                  | Next action                                                                  |
|--------------------|------------------------|------------------------------------------------------------------------------|
| BP_PorterGoatPersistor | Spec'd, needs editor work | You author in editor per the steps above, commit the JSON to this PR        |
| Proximity menu     | Architecture confirmed (BP-level) | You confirm 3 questions above; I'll write the implementation spec        |
| Saddlebag→Bell text bug | Identified         | Decide where to fix (this PR / separate PR / your own pipeline)              |

No code or asset changes in this PR yet — design only. Once you've reviewed and we've agreed on the approach, the actual `.json` files land in follow-up commits on this same branch.

Thanks!
