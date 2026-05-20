# Persistor — JSON-clone attempt (and what we learned about the menu)

Hi Tobi — per your direction ("clone and change like for #5; same for #6"), I tried producing both deliverables by JSON-only surgery on vanilla assets. **#5 worked. #6 didn't, and the reason is interesting.**

This PR adds the persistor; the menu situation is documented below so you have the full picture.

---

## #5 — `BP_PorterGoatPersistor` (delivered)

**Files added:**
- `json/Moria/Content/Mods/PorterGoat/Persistor/BP_PorterGoatPersistor.json`
- `uasset/Moria/Content/Mods/PorterGoat/Persistor/BP_PorterGoatPersistor.uasset`
- `uasset/Moria/Content/Mods/PorterGoat/Persistor/BP_PorterGoatPersistor.uexp`

**How it was built (same pattern you used for `BP_SaddleBags_Goat` / `EQ_GoatBell`):**

1. Searched all small vanilla `.uasset` files (<200 KB) for the `MorSaveGameObjectCallbacks` interface marker. 6 hits.
2. Picked the smallest viable template: `BP_TimeManager.uasset` (11 KB). It's an `AActor` subclass that implements `MorSaveGameObjectCallbacks` with all 6 interface methods already wired (`SaveGameObjectPreStore`, `PostStore`, `PreRestore`, `PostRestore`, `PreRestoreDestroy`, `UpgradeClass`), plus the standard `DefaultSceneRoot` + `SimpleConstructionScript` setup.
3. Ran `UAssetGUI tojson` on the vanilla asset.
4. JSON-edited 5 places (all string substitutions, no structural changes):
   - NameMap entry for the package path: `/Game/Tech/Managers/BP_TimeManager` → `/Game/Mods/PorterGoat/Persistor/BP_PorterGoatPersistor`
   - NameMap entry for the class name: `BP_TimeManager_C` → `BP_PorterGoatPersistor_C`
   - NameMap entry for the CDO: `Default__BP_TimeManager_C` → `Default__BP_PorterGoatPersistor_C`
   - `FolderName`: same path swap
   - Two Export `ObjectName` fields: the class export and the CDO export
5. `UAssetGUI fromjson` baked it back to `.uasset` + `.uexp`.
6. Round-tripped (`tojson` → `fromjson` → `tojson`) and the JSON came out byte-identical. Class identity properly renamed; interface still resolves to `MorSaveGameObjectCallbacks`.

**One thing to know:** I kept the internal ubergraph function name (`ExecuteUbergraph_BP_TimeManager`) untouched. UE doesn't require this to match the class — it's just a compiler artifact. When I tried renaming it, UAssetGUI's bytecode serializer choked on offset shifts. The class identity is correct (`BP_PorterGoatPersistor_C`), only the embedded function happens to keep the original name. This should be invisible at runtime.

**Honest caveat — what the clone carries with it:**

Because we cloned `BP_TimeManager` whole, the resulting persistor still has:

- The TimeManager's 11 variables in its CDO (`Progress_OrcsAreScary_Westgate_1` through `_4`, `OrcsAreScaryTimerHandle`, `bRunOrcsAreScary`, `Progress_Westgate_SecondNight`, `Tip`, etc.) — these are time-of-day game-state markers, not goat data.
- The original BP function bytecode (the `OrcsAreScary_*` timer logic, the `ReceiveBeginPlay` handler that sets up the time manager's tick).

In other words: the persistor is an *Actor that thinks it's a Time Manager but lives under a different class name*. None of its variables are `CPF_SaveGame`-flagged (TimeManager does its serialization manually in the interface methods, referencing the `Progress_*` and `Tip` variables).

**Two ways to use it:**

- **Pragmatic v1 (recommended):** UE4SS spawns the persistor but suppresses its `BeginPlay` (or destroys/respawns it without ticking). The persistor's only role is to *exist as a save-system-iterated actor of a stable, identifiable class*. UE4SS-side code carries the actual goat state in a small sidecar file or in-memory state, keyed off the persistor's instance.
- **Cleanest v2 (future):** You add 7 goat-specific variables with the `Save Game` flag in the editor, replacing the TimeManager-era variables. At that point the engine's automatic `CPF_SaveGame` serialization handles everything and we don't need UE4SS for save state. JSON-surgery can't add those variables — UE4.27's BP Python API doesn't expose `add_member_variable` cleanly (your earlier `ue4_create_portergoat_persistor.py` script notes this), and hand-editing `LoadedProperties` to add new SaveGame-flagged FProperty entries is fragile.

For the runtime team (UE4SS side), v1 is enough to unblock save/load work — the persistor exists at a stable path with a stable class, which is the contract they were waiting for.

---

## #6 — Proximity menu (couldn't do via JSON; here's why)

I tried the same clone-and-customize approach. The plan was: find the proximity menu's "entries" data in `BP_NpcGoat` (or a parent), clone an existing entry, retarget its label/callback to "Open Inventory" and "Dismiss".

**The architecture is delegate-based, not entry-array-based.**

Tracing `BP_NpcGoat.json` on your `Goat-npc` branch:

- Only 2 interaction-relevant Exports: `BndEvt__BP_NpcGoat_MorNPC_K2Node_ComponentBoundEvent_2_MorNpcOnManageLocalInteraction__DelegateSignature` and `BndEvt__..._MorNpcOnManageInteraction__DelegateSignature` — these are **event-handler function bodies**, not a list of menu items.
- Only 1 relevant interaction class import: `MorViewTrigger`.
- There is no array of `MorInteraction` instances in the goat's CDO that we could append to. The menu's contents come from C++ logic that runs inside `OnManageInteraction` and emits menu entries dynamically.

So there's nothing for a JSON clone to extend. Adding "Open Inventory" / "Dismiss" entries requires one of:

- **Editor work** in your `BP_NpcGoat` graph: open the `MorNpcOnManageInteraction` event handler, drop in nodes that add new menu entries with our labels and our callback functions. Can't be done in JSON without authoring BP bytecode from scratch (not realistic).
- **UE4SS runtime hook**: the runtime mod hooks the `OnManageInteraction` delegate at game start and injects custom entries when the targeted NPC is a `BP_NpcGoat`. This is what we're now planning to do on the runtime side — no editor changes from you needed for the menu.

I'd lean on the UE4SS runtime path. It keeps your `BP_NpcGoat` override clean and avoids re-cooking the larger goat BP every time the menu changes. Let me know which way you'd prefer.

**Side benefit of the runtime route:** your "doubt about whether the goat will have the slot for the saddlebags and the helmet in that UI" goes away. UE4SS opens whatever container UI we want — we'll just point "Open Inventory" at the saddlebag container UI you already wired (`BP_ContainerItem_Goat_Slot_EpicPack`), not at the dwarf EpicPack screen.

---

## Updated to-do for you (just one item)

You said you'll add the `Goat.Role.Porter` key to `ST_PorterGoatStrings`. That's the only thing left on your plate from the editor side for this iteration. After that's in, the Porter role label will show as "Porter Goat" instead of the raw key string in the in-game NPC menus.

When you're ready to do the bell visuals from the Sketchfab model (https://sketchfab.com/3d-models/hand-bell-41c7b3b48369437bb07797de09ca6232), that's the last cosmetic piece. No rush.

---

## Summary

| Item | What was delivered | What's next |
|------|---------|-------------|
| Persistor (#5) | Cloned from `BP_TimeManager`, renamed via JSON surgery, round-trip-validated. Lives at `/Game/Mods/PorterGoat/Persistor/BP_PorterGoatPersistor`. | UE4SS-side save/load wiring (runtime team) |
| Proximity menu (#6) | Not in this PR — architecture is delegate-based and can't be JSON-cloned | UE4SS-side delegate hook (runtime team), no editor changes from you |
| `Goat.Role.Porter` ST key | You're adding it | (you, when ready) |
| Bell visuals | You will do | (you, when ready) |

Happy to translate any of this to Spanish if useful.
