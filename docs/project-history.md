# Project History

## Timeline

| Date | Commit | Event |
|------|--------|-------|
| 2025-07-16 | (backups) | Initial design iterations — 5 backup snapshots in `thermometer-backups/` before first git commit |
| 2025-07-19 | `18f5047` | First git commit — MCP9600 schematic + initial PCB layout uploaded |
| 2025-07-27 | `dfb0be3` | BMP581 pressure sensor added to schematic ("Added bmp581 Pressure Sensor to temperature sensor daughter board") |
| 2025-08-13 | `0baa108` | Zynq-Carrier-Power added as git submodule |
| 2025-08-13 | `4633a5a`–`e697671` | Multiple attempts to configure the Zynq-Carrier-Power submodule |
| 2025-08-23 | `e8460a1`–`3b9bdd7` | DIGITALBot submodule added, re-added, and adjusted |
| 2025-08-26 | `c81e8e5` | DIGITALBot submodule removed — last design commit |
| 2026-06-02 | `0a96fb0` | Preservation documentation added (README, CLAUDE.md, docs/, .claude/skills/) |

Active design span: ~38 days (July 19 – August 26, 2025).

## Team Members

| Name | Email | GitHub |
|------|-------|--------|
| pyson2k | paung@cpp.edu | pyson2k |
| Sebastian Graciano | sebgra518@gmail.com | sebgra518 |
| pixelatedknight27 | maxgross72@gmail.com | maxgross72 |
| eryn-chen | eryncchen@gmail.com | eryn-chen |

## Submodule History

### Zynq-Carrier-Power
- **URL:** `https://github.com/eryn-chen/Zynq-Carrier-Power` (branch: master)
- **Added:** August 13, 2025
- **Status:** Entry still present in `.gitmodules` but directory is empty — submodule was never populated
- **Purpose:** The intended host/carrier board this daughter board was designed to connect to
- **To initialize:** `git submodule update --init --recursive`

### DIGITALBot
- **Added:** ~August 23, 2025
- **Removed:** August 26, 2025 (commit `c81e8e5`)
- **Purpose:** Unclear in context of this hardware project; appeared to be a chatbot submodule
- **Status:** Fully removed from `.gitmodules` and repo

## Design Decisions Recorded

- **BMP581 I2C address: 0x46** — SDO/ADR pin tied to GND in schematic. Note: BMP581 addresses are 0x46/0x47 (not 0x76/0x77 — those belong to BMP280/BMP388).
- **MCP9600 I2C address: 0x60** — ADDR pin floating (default), schematic annotated with annotation label `0x60` (a global_label of type tri_state used as a visual note, not a signal connection).
- **No I2C pull-up resistors on this board** — the host board (Zynq-Carrier-Power) is expected to provide them.
- **1mm pitch chosen for J1** — compact form factor for daughter board interface.
- **Custom MCP9600 footprint** — standard KiCad QFN-20 was insufficient; team created a 30-pad footprint: 20 peripheral pads (10 signal + 10 GND) + 10 EXP sub-pads (21–30) inside the exposed thermal pad area. The "21N" in the footprint name refers to 21 unique electrical nets.
- **BMP581 library not localized** — sourced from SnapEDA and added to the GLOBAL KiCad library on the developer's machine. The project-level `sym-lib-table` and `fp-lib-table` have no BMP581 entry. This is the project's most critical "must fix before reopening" issue.

## Unresolved Issues at Time of Abandonment

These were open issues in the design when work stopped:

1. **EXP pad floating** — MCP9600 exposed thermal pad (pads 21–30) forms isolated net `Net-(U1-EXP-Pad21)`. Should be connected to GND in the schematic.
2. **U1 SCL/SDA not wired** — MCP9600's SCL (pin 19) and SDA (pin 20) are unconnected in both schematic and PCB. Global labels exist but are not wired to U1.
3. **U1 ALERT pins not wired** — ALERT_1–4 global labels exist but not wired to U1.
4. **J1 footprint set in PCB only** — the schematic J1 symbol has an empty Footprint property; the footprint was placed directly in the PCB editor.
5. **IgnorePin label** — a `global_label "IgnorePin"` at schematic coordinate (96.52, 67.31) exists for unknown purpose, possibly to suppress a DRC error on a pin near U1.

## Why Abandoned

No explicit reason recorded in commit messages. Last activity (August 23–26) was submodule cleanup with no schematic or PCB changes. The PCB remained incomplete:
- No copper traces routed
- No board outline defined
- BMP581 not placed in PCB (schematic only)
- J1 connector pinout never finalized

The project appears to have been paused rather than cancelled — the schematic work is substantially complete and the design intent is clear.

## Backup Archive Contents

The `thermometer-backups/` directory contains 6 timestamped KiCad ZIP backups from the day of initial setup (July 16, 2025), before version control was initialized. These represent the pre-git design iterations:

| Archive | Timestamp |
|---------|-----------|
| thermometer-2025-07-16_213626.zip | 2025-07-16 21:36 |
| thermometer-2025-07-16_214447.zip | 2025-07-16 21:44 |
| thermometer-2025-07-16_215526.zip | 2025-07-16 21:55 |
| thermometer-2025-07-16_220757.zip | 2025-07-16 22:07 |
| thermometer-2025-07-16_221732.zip | 2025-07-16 22:17 |
| thermometer-2025-07-27_215053.zip | 2025-07-27 21:50 |
