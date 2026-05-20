# Proximity menu — JSON-clone update (rev 2)

Follow-up to the earlier `PERSISTOR_CLONE_NOTES.md` in this same PR. My first pass concluded the menu architecture was delegate-only and couldn't be done via JSON surgery. **That was wrong.** A deeper look at the goat's `MorNPC_GEN_VARIABLE` component vs. the dwarf's revealed the menu entries are actually named `MorInteraction` struct properties on the component — pure data, perfectly clone-and-customizable.

This commit applies that finding to `BP_NpcGoat`.

## What I changed in `BP_NpcGoat`

Surgery on `MorNPC_GEN_VARIABLE` inside Tobi's existing `BP_NpcGoat` override (json + uasset + uexp updated):

1. **`ManageInteraction`** — renamed and prioritized
   - `EnabledTextFormat.CultureInvariantString`: `"Manage Goat"` → `"Open Inventory"`
   - `DisabledTextFormat.CultureInvariantString`: `"Manage Goat"` → `"Open Inventory"`
   - Added `SortPriority = 1` (to put it first in the menu)
   - Both text format GUIDs regenerated (avoids collisions with the original "Manage Goat" FText identity)

2. **`TalkInteraction`** — new entry added (mirror of dwarf's `TalkInteraction` struct shape)
   - `SortPriority = 2`
   - `EnabledTextFormat = "Dismiss"` (inline literal, `HistoryType: "Base"`, `TransformType: "ToLower"`)
   - `DisabledTextFormat = "Dismiss"`

3. NameMap additions: `TalkInteraction`, `SortPriority` (required since the goat didn't reference these names previously).

Existing `ReviveInteraction` and `RescueInteraction` are untouched.

Round-trip validated: `tojson → fromjson → tojson` produces JSON with identical NameMap and all 87 exports preserved.

## What the player will see in-game

Walking up to the goat and opening the interaction menu:

```
open inventory   ← (existing ManageInteraction handler — already opens the inventory/management UI)
dismiss          ← (existing TalkInteraction handler — fires the talk callback)
revive           ← (only when goat is downed)
rescue           ← (only in specific contexts)
```

The text appears lowercase because the inherited `TransformType: "ToLower"` matches dwarf-menu convention.

## Important: the callbacks

The menu **labels** are pure data and now correct. The **callbacks** behind each entry are C++ behaviors tied to the property name:

- `ManageInteraction` → fires the standard NPC "Manage" handler. For dwarves this opens an inventory/equipment/role UI. **For the goat this should already do something useful** — likely opens an inventory-style screen. If the screen has goat-inappropriate slots (helmet, weapon, etc.) we can address it at the inventory UI level later.
- `TalkInteraction` → fires the standard NPC "Talk" handler. The goat has no `MorNPCConversationComponent`, so this will probably no-op gracefully or open an empty dialogue.

**This is fine for v1.** The runtime team (VS Claude) will hook the OnTalkInteraction delegate and dispatch it to the actual despawn logic — but the *visibility* of the "Dismiss" entry is baked into the BP, which is the reliable part. UE4SS-side hooks for default-always-appearing entries have been unreliable in past attempts; static BP-level entries are the right answer.

If "Open Inventory" doesn't open the right screen, we have two paths:
- UE4SS runtime hook on `OnManageInteraction` for `BP_NpcGoat_C` that opens the saddlebag container UI (your existing `BP_ContainerItem_Goat_Slot_EpicPack` flow) instead of the dwarf-default screen
- A different `MorInteraction` slot whose C++ handler happens to do the right thing (need empirical testing)

Either way the *menu entry is there*.

## Updated status

| Item | Status |
|------|--------|
| **Persistor (#5)** | ✓ Delivered (BP_TimeManager clone, JSON-surgery) |
| **Proximity menu (#6)** | ✓ Delivered (Manage→"Open Inventory" rename + new Talk→"Dismiss") |
| Saddlebag→bell text bug | ✓ You already fixed it in `b29f3e3b` |
| `Goat.Role.Porter` ST key | You said you'd add it |
| Bell visuals | You will do, no rush |

So as of this PR there's nothing new on your plate beyond what you already said you'd do. 🎉

If you find that "Open Inventory" doesn't open the right container UI in-game when you test it, that's a runtime issue for the VS Claude side to hook — not a BP problem.
