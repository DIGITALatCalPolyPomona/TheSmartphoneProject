# Component Reference

## U1 — MCP9600-E_MX (Thermocouple Amplifier)

| Field | Value |
|-------|-------|
| Manufacturer | Microchip Technology |
| Part number | MCP9600-E/MX |
| Function | Thermocouple EMF-to-temperature converter with cold-junction compensation |
| Package | QFN-20 body with large exposed thermal pad (custom footprint: 30-pin scheme) |
| Supported thermocouple types | K, J, T, N, S, E, B, R |
| I2C address | 0x60 intended (`0x60` annotation label in schematic) — but ADDR is actually wired to the `SCL` net, so the real address is indeterminate |
| Supply voltage | 2.7V – 5.5V (3.3V used here) |
| Symbol library | `jackboys:MCP9600-E_MX` (local, `jackboys.kicad_sym`) |
| Footprint library | `jackboys2:QFN65P500X500X100-21N_MCP9600-E_MX` (local, `jackboys2.pretty/`) |
| Datasheet | https://ww1.microchip.com/downloads/en/DeviceDoc/MCP9600-Data-Sheet-DS20005426E.pdf |

**Schematic status:** Placed but **miswired** (paused mid-refactor — see pin table)
**PCB status:** Footprint placed, not routed; PCB netlist is stale (predates the schematic rewiring)

### Custom Symbol Pin Structure

The `jackboys:MCP9600-E_MX` symbol uses a 30-pin numbering scheme (12 unique nets):

| Pin numbers | Name | Type | Actual schematic connection (verified 2026-10-01) |
|-------------|------|------|-------------------|
| 2 | VIN+ | Input | **unconnected** ⚠ — TC1 wire ends before reaching the pin |
| 4 | VIN- | Input | **unconnected** ⚠ — same, TC1 wire stops short |
| 8 | VDD | Power | **unconnected** ⚠ — no +3.3V reaches U1 at all |
| 11 | ALERT_1 | Output | **unconnected** — `ALERT_1` label floats nearby, doesn't touch the pin |
| 12 | ALERT_2 | Output | on `ALERT_4` net ⚠ (label mismatch — swapped) |
| 14 | ALERT_3 | Output | on `ALERT_3` net ✓ (only correctly-wired alert) |
| 15 | ALERT_4 | Output | on `ALERT_2` net ⚠ (label mismatch — swapped) |
| 16 | ADDR | Input | on `SCL` net ⚠ — should be strapped or floating for a defined I2C address |
| 19 | SCL | Input | **tied to GND** ⚠ — a `GND` power symbol sits exactly on the pin |
| 20 | SDA | Bidirectional | **unconnected** ⚠ |
| 1, 3, 5, 6, 7, 9, 10, 13, 17, 18 | GND | Power | **unconnected** ⚠ — the stacked GND pins never received a ground symbol |
| 21–30 | EXP | Power | anonymous net `Net-(U1-EXP-Pad21)` — **NOT connected to GND** ⚠ |

**Root cause hypothesis:** the wires/labels/power symbols around U1 and U2 appear
drawn for *vertically mirrored* symbol geometry, but the placed instances carry
no mirror token — so every connection lands one "reflected" pin-position away.
Fix the wiring (not the symbol) and re-run ERC.

**Design issue — EXP pad floating:** The exposed thermal pad (pads 21–30) forms its own anonymous net `Net-(U1-EXP-Pad21)`. It is NOT connected to the GND net. Per the MCP9600 datasheet, the exposed pad should be soldered and connected to a ground plane for thermal management. This needs to be corrected before fabrication.

### Footprint Detail

Footprint name decoded: `QFN65P500X500X100-21N_MCP9600-E_MX`
- `QFN` — Quad Flat No-lead
- `65P` — 0.65mm pad pitch
- `500X500` — 5.00mm × 5.00mm body
- `X100` — 1.0mm height
- `21N` — IPC terminal count (20 leads + 1 exposed pad); electrically the footprint carries 12 unique nets (10 signal + GND + EXP)

Total pad objects in footprint: 30 (20 peripheral `smd` + pad 21 EP `smd` + pads 22–30 `thru_hole` thermal vias under the EP)

---

## U2 — BMP581 (Barometric Pressure Sensor)

| Field | Value |
|-------|-------|
| Manufacturer | Bosch Sensortec |
| Part number | BMP581 |
| Function | 24-bit absolute barometric pressure and temperature sensor |
| Package | LGA-10 (2.0×2.0mm, 0.5mm pitch) — per Bosch datasheet; schematic Package property is "None" (SnapEDA default) |
| I2C address | 0x46 intended (`0x46` annotation label) — but SDO/ADR is actually wired to the `INT` net, so the real address is indeterminate |
| Pressure range | 30–125 kPa |
| Supply voltage | 1.71V – 3.6V (3.3V used here; VDD and VDDIO both tied to 3.3V) |
| Symbol | `BMP581:BMP581` — **NOT in project sym-lib-table** (was in global KiCad library on developer machine) |
| Footprint | `BMP581:BMP581` — **NOT in project fp-lib-table** (was in global KiCad library on developer machine) |
| Datasheet | https://www.bosch-sensortec.com/products/environmental-sensors/pressure-sensors/bmp581/ |
| SnapEDA source | https://www.snapeda.com/parts/BMP581/Bosch/view-part/ |
| SnapEDA PROD_ID | IC-16798 |

**Schematic status:** Placed but **miswired** (paused mid-refactor — see pin table)
**PCB status:** NOT placed — U2 is absent from the PCB layout entirely

**ACTION REQUIRED before opening project:** The `BMP581:BMP581` library is not in this repo's sym-lib-table or fp-lib-table. KiCad will report a missing library on any machine other than the original developer's (the symbol still renders from the schematic's embedded `lib_symbols` cache). See `docs/library-notes.md` for reinstall steps.

### Pins in schematic — actual connections (verified 2026-10-01)

| Pin | Name | Should be | Actually is |
|-----|------|-----------|-------------|
| 1 | VDDIO | +3.3V | **unconnected** ⚠ |
| 2 | SCK/SCL | `SCL` | **+3.3V** ⚠ (a power symbol sits on the pin) |
| 3 | GND | GND | **unconnected** ⚠ |
| 4 | SDI/SDA | `SDA` | **unconnected** ⚠ |
| 5 | SDO/ADR | GND (for address 0x46) | `INT` net ⚠ (SDO/INT appear swapped) |
| 6 | CSB | +3.3V (I2C mode) | `SCL` net ⚠ |
| 7 | INT | `INT` | **GND** ⚠ (a power symbol sits on the pin) |
| 8 | GND | GND | **unconnected** ⚠ |
| 9 | GND | GND | **unconnected** ⚠ |
| 10 | VDD | +3.3V | +3.3V ✓ (only correct power pin) |

---

## TC1 — Thermocouple

| Field | Value |
|-------|-------|
| Symbol library | `Device:Thermocouple` (standard KiCad library) |
| Footprint | **Not assigned** — physical connector type not decided |
| Connection | Intended: TC1 pin 1 → U1 VIN+; TC1 pin 2 → U1 VIN−. Actual: wires end short of U1's pins (schematic); `Net-(TC1-+/-)` only exist in the stale PCB netlist |

**Schematic status:** Placed; wires drawn toward U1 but they end before reaching the VIN+/VIN− pin points — **TC1 is not actually connected** ⚠
**PCB status:** No footprint assigned, not in PCB layout

The PCB net list shows `Net-(TC1-+)`/`Net-(TC1--)` attached to U1 pads 2 and 4, but that netlist predates the schematic rewiring — in the current schematic the TC1 wires terminate short of U1's pins, so VIN+/VIN− are unconnected. The MCP9600 supports K, J, T, N, S, E, B, and R-type thermocouples — type is selected via I2C register configuration, not hardware. A physical thermocouple connector (e.g., panel-mount miniature thermocouple jack) must be chosen and footprint assigned before PCB completion.

---

## J1 — Interface Connector

| Field | Value |
|-------|-------|
| Description | 7-pin single-row pin header |
| Symbol library | `Connector_Generic:Conn_01x07` (standard KiCad library) |
| Footprint in schematic | **EMPTY** — Footprint property is blank in the schematic symbol instance |
| Footprint in PCB | `Connector_PinHeader_1.00mm:PinHeader_1x07_P1.00mm_Vertical` (placed directly in PCB editor) |
| Pitch | 1.00mm |
| Style | Through-hole, vertical |
| PCB location | (104.375, 75.945) mm |

**Schematic status:** Placed and **labeled** — global labels sit exactly on all 7 pin attach points: pin 1 = `INT`, 2 = `ALERT_4`, 3 = `ALERT_3`, 4 = `ALERT_2`, 5 = `ALERT_1`, 6 = `SDA`, 7 = `SCL`. **No pin carries +3.3V or GND** — the board's power path is undefined. No footprint annotation in schematic.
**PCB status:** Footprint placed in PCB directly; all 7 pads on stale `unconnected-` nets

All 7 J1 pads are `unconnected-(J1-Pin_N-PadN)` nets in the PCB because the PCB netlist predates the schematic label row — "Update PCB from Schematic" was never run since. The J1 footprint was placed in the PCB editor manually rather than being annotated in the schematic first. See `docs/connector-pinout.md` for the as-implemented pinout, its defects, and remaining work.
