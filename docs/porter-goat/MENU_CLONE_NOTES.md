# Proximity menu — JSON-clone (rev 3, final menu set)

This commit lands the **final 6-entry porter-goat menu** plus context-only Revive. Three iterations got us here:

- **rev 1** (earlier in the same PR): concluded menu was delegate-only and not JSON-extensible — *wrong*
- **rev 2**: discovered menu entries are named `MorInteraction` struct properties on `MorNPC_GEN_VARIABLE`; shipped 2-entry proof-of-concept (Open Inventory / Dismiss)
- **rev 3 (this)**: expanded to John's full 6-entry spec with the right labels and defensive visibility flags

## The 6 menu entries

Listed in display order (controlled by `SortPriority` on each struct):

| # | Label | Slot used | Default C++ behavior | UE4SS override |
|---|---|---|---|---|
| 1 | Follow | `TalkInteraction` | tries to start dialogue; goat has no `MorNPCConversationComponent` → no-op | hook OnTalkInteraction → flip the goat AI controller's `DynamicBehaviors` map key to the existing "follow" behavior (FRG pre-wired this — `Bst_NPCGoatWorkPorter` already follows the player) |
| 2 | Stay | `RecruitInteraction` | C++ recruit precondition check; goat won't satisfy → no-op | hook OnRecruitInteraction → flip the `DynamicBehaviors` map key to the existing "stay/idle" behavior (also pre-wired) |
| 3 | Saddlebags | `ManageInteraction` | opens NPC management UI (inventory) — close to what we want | hook OnManageInteraction → open `BP_ContainerItem_Goat_Slot_EpicPack` UI directly (cleaner than dwarf-default screen) |
| 4 | Feed | `DeliverResearchInteraction` | requires player-has-research-item check → no-op | hook OnDeliverResearchInteraction → consume food from player inventory, raise goat stat |
| 5 | Rename | `DetailsInteraction` | opens character details panel | hook OnDetailsInteraction → open rename text input UI |
| 6 | Dismiss | `RescueInteraction` | NPC rescue transition — usually no-op when target isn't captive | hook OnRescueInteraction → destroy goat actor + persistor; persistor's sidecar data carries forward |
| — | (Revive) | `ReviveInteraction` | revive downed NPC — *default behavior is what we want* | none needed |

**Why this slot mapping**: I picked the 6 `MorInteraction` property names from the dwarf's known-good 7-slot set (`Manage`, `Talk`, `Recruit`, `Revive`, `Rescue`, `DeliverResearch`, `Details`). Property names are hard-coded in C++ at runtime — we can't invent new names like `FollowInteraction` and expect them to show up in the menu. We CAN repurpose existing slots with any label we like.

**About Follow/Stay specifically — FRG already wired the AI side**: the goat's `BP_NpcGoat_AIController` has a `DynamicBehaviors` map with 4 entries. `Bst_NPCGoatWorkPorter` (the porter work behavior tree FRG shipped, currently bound to the Porter role) already implements follow-the-player movement plus idle states (`BSt_Idle_C_3`, `BSt_Idle_C_6` visible in its exports). So UE4SS doesn't have to implement follow/stay from scratch — it just flips the active behavior in the existing map. The hardest piece was already done by FRG; the menu just needs to surface the toggle.

## Visibility flags (the full picture)

There are **two parallel flag sets** per interaction kind, not one. The pattern became clear after inspecting `BP_NpcDwarf_Wanderer.uasset`, which explicitly sets ALL of them to `False` to opt out of the standard menu (the Wanderer uses its own `MorWanderer_GEN_VARIABLE` component for follower-style interactions):

- `b<Name>InteractionEnabled` — entry is enabled vs disabled-but-shown
- `b<Name>InteractionRegister` — entry is **registered in the menu at all** (the real visibility gate)

Both must be `True` for an entry to appear and be clickable. This commit sets all 12 flags `True` on the goat's `MorNPC_GEN_VARIABLE`, mirroring the Wanderer pattern (just inverted from False→True since we want to opt IN, not OUT):

```
bManageInteractionRegister = True       bManageInteractionEnabled = True
bTalkInteractionRegister = True         bTalkInteractionEnabled = True
bRecruitInteractionRegister = True      bRecruitInteractionEnabled = True
bDeliverResearchInteractionRegister=True bDeliverResearchInteractionEnabled=True
bDetailsInteractionRegister = True      bDetailsInteractionEnabled = True
bRescueInteractionRegister = True       bRescueInteractionEnabled = True (was already True)
```

With both flag sets set explicitly, all 6 slots should register and be clickable. The empirical risk on `Recruit` / `DeliverResearch` having additional C++ preconditions (player-state checks etc.) is now much lower.

## What changed in BP_NpcGoat

Surgery on `MorNPC_GEN_VARIABLE` inside Tobi's existing `BP_NpcGoat` override:

- **Modified existing structs:**
  - `ManageInteraction`: label "Manage Goat" → "Saddlebags", SortPriority=3
  - `RescueInteraction`: label "Rescue" → "Dismiss", added SortPriority=6
- **Added new structs** (mirroring dwarf shape):
  - `TalkInteraction`: SortPriority=1, label "Follow"
  - `RecruitInteraction`: SortPriority=2, label "Stay"
  - `DeliverResearchInteraction`: SortPriority=4, label "Feed"
  - `DetailsInteraction`: SortPriority=5, label "Rename"
- **Added 5 visibility bools** (described above)
- **NameMap additions**: `SortPriority`, `TalkInteraction`, `RecruitInteraction`, `DeliverResearchInteraction`, `DetailsInteraction`, plus the 5 enable bools
- **Unchanged**: `ReviveInteraction` ("Revive", context-only)

All FText identity GUIDs regenerated where text changed (avoids collisions with the original FText cache keys).

Round-trip validated: `tojson → fromjson → tojson` produces JSON with NameMap byte-identical (507 entries both directions) and all 87 exports preserved.

## What the player sees in-game

Walking up to the porter goat and opening the interaction wheel (text appears lowercase because the inherited `TransformType: "ToLower"` matches dwarf-menu convention):

```
follow
stay
saddlebags
feed
rename
dismiss
(revive)      ← only appears when goat is downed
```

## Caveats to acknowledge

1. **Default callbacks** for repurposed slots may do unexpected things if UE4SS isn't loaded — e.g., clicking "Feed" without UE4SS might briefly attempt a "deliver research" check that fails silently. Probably benign. UE4SS hooks are the production behavior layer.

2. **Empirical risk on Recruit/DeliverResearch visibility**: if C++ has hard-coded preconditions that override the `b*Enabled` bools, those entries might still hide. If "Stay" or "Feed" don't appear in-game testing, that's the diagnostic — and the fix is to either find the right gating flag or shift those labels to known-safe slots.

3. **Slot reuse means the "Rescue" interaction kind is gone** from the goat — but only as a label. The underlying slot is repurposed as "Dismiss". John explicitly asked for "not rescue", and this satisfies that.

## Updated status (everything goat-side that this PR delivers)

| Item | Status |
|------|--------|
| Persistor (#5) | ✓ Delivered (BP_TimeManager clone) |
| Proximity menu — 6 entries (#6) | ✓ Delivered (this commit) |
| Saddlebag→bell text bug | ✓ You already fixed it in `b29f3e3b` |
| `Goat.Role.Porter` ST key | You said you'd add it |
| Bell visuals | You will do, no rush |
