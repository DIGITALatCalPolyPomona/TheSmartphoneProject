# Component Reference

## U1 — MCP9600-E_MX (Thermocouple Amplifier)

| Field | Value |
|-------|-------|
| Manufacturer | Microchip Technology |
| Part number | MCP9600-E/MX |
| Function | Thermocouple EMF-to-temperature converter with cold-junction compensation |
| Package | QFN-20 body with large exposed thermal pad (custom footprint: 30-pin scheme) |
| Supported thermocouple types | K, J, T, N, S, E, B, R |
| I2C address | 0x60 (ADDR pin floating → default; confirmed by `0x60` annotation label in schematic) |
| Supply voltage | 2.7V – 5.5V (3.3V used here) |
| Symbol library | `jackboys:MCP9600-E_MX` (local, `jackboys.kicad_sym`) |
| Footprint library | `jackboys2:QFN65P500X500X100-21N_MCP9600-E_MX` (local, `jackboys2.pretty/`) |
| Datasheet | https://ww1.microchip.com/downloads/en/DeviceDoc/MCP9600-Data-Sheet-DS20005426E.pdf |

**Schematic status:** Placed and wired (VIN+, VIN-, VDD, GND only — see pin table below)
**PCB status:** Footprint placed, not routed

### Custom Symbol Pin Structure

The `jackboys:MCP9600-E_MX` symbol uses a 30-pin numbering scheme (21 unique nets):

| Pin numbers | Name | Type | Connection in PCB |
|-------------|------|------|-------------------|
| 2 | VIN+ | Input | `Net-(TC1-+)` → TC1 thermocouple positive ✓ |
| 4 | VIN- | Input | `Net-(TC1--)` → TC1 thermocouple negative ✓ |
| 8 | VDD | Power | +3.3V ✓ |
| 11 | ALERT_1 | Output | **unconnected** (global label exists in schematic but not wired to U1) |
| 12 | ALERT_2 | Output | **unconnected** |
| 14 | ALERT_3 | Output | **unconnected** |
| 15 | ALERT_4 | Output | **unconnected** |
| 16 | ADDR | Input | **unconnected** (floating → default I2C address 0x60) |
| 19 | SCL | Input | **unconnected** (global label SCL exists in schematic but not wired to U1) |
| 20 | SDA | Bidirectional | **unconnected** (global label SDA exists in schematic but not wired to U1) |
| 1, 3, 5, 6, 7, 9, 10, 13, 17, 18 | GND | Power | GND net ✓ (10 peripheral GND pads) |
| 21–30 | EXP | Power | `Net-(U1-EXP-Pad21)` — **NOT connected to GND** ⚠ |

**Design issue — EXP pad floating:** The exposed thermal pad (pads 21–30) is assigned its own isolated net `Net-(U1-EXP-Pad21)` in the PCB. It is NOT connected to the GND net. Per the MCP9600 datasheet, the exposed pad should be soldered and connected to a ground plane for thermal management. This needs to be corrected before fabrication.

**Design note — SCL/SDA wiring:** Despite global labels `SCL`, `SDA`, `ALERT_1`–`ALERT_4` being present in the schematic, the KiCad PCB net list shows all these pins on U1 as unconnected. The global labels in the schematic appear to be connected only to U2 (BMP581) and J1, not to U1.

### Footprint Detail

Footprint name decoded: `QFN65P500X500X100-21N_MCP9600-E_MX`
- `QFN` — Quad Flat No-lead
- `65P` — 0.65mm pad pitch
- `500X500` — 5.00mm × 5.00mm body
- `X100` — 1.0mm height
- `21N` — 21 unique electrical nets (10 signal + 10 GND + 1 EXP)

Total pads in footprint: 30 (20 peripheral + 10 EXP sub-pads in the thermal pad area)

---

## U2 — BMP581 (Barometric Pressure Sensor)

| Field | Value |
|-------|-------|
| Manufacturer | Bosch Sensortec |
| Part number | BMP581 |
| Function | 24-bit absolute barometric pressure and temperature sensor |
| Package | LGA-10 (2.0×2.0mm, 0.5mm pitch) — per Bosch datasheet; schematic Package property is "None" (SnapEDA default) |
| I2C address | 0x46 (SDO/ADR = GND per `0x46` annotation label in schematic) |
| Pressure range | 30–125 kPa |
| Supply voltage | 1.71V – 3.6V (3.3V used here; VDD and VDDIO both tied to 3.3V) |
| Symbol | `BMP581:BMP581` — **NOT in project sym-lib-table** (was in global KiCad library on developer machine) |
| Footprint | `BMP581:BMP581` — **NOT in project fp-lib-table** (was in global KiCad library on developer machine) |
| Datasheet | https://www.bosch-sensortec.com/products/environmental-sensors/pressure-sensors/bmp581/ |
| SnapEDA source | https://www.snapeda.com/parts/BMP581/Bosch/view-part/ |
| SnapEDA PROD_ID | IC-16798 |

**Schematic status:** Placed and wired
**PCB status:** NOT placed — U2 is absent from the PCB layout entirely

**ACTION REQUIRED before opening project:** The `BMP581:BMP581` library is not in this repo's sym-lib-table or fp-lib-table. KiCad will show missing symbol/footprint errors on any machine other than the original developer's. See `docs/library-notes.md` for reinstall steps.

### Pins used in schematic

| Pin | Name | Connection |
|-----|------|-----------|
| 1 | VDDIO | +3.3V |
| 2 | SCK/SCL | Global label `SCL` |
| 3 | GND | GND |
| 4 | SDI/SDA | Global label `SDA` |
| 5 | SDO/ADR | GND (sets I2C address to 0x46) |
| 6 | CSB | +3.3V (selects I2C mode, disables SPI) |
| 7 | INT | Global label `INT` |
| 8 | GND | GND |
| 9 | GND | GND |
| 10 | VDD | +3.3V |

---

## TC1 — Thermocouple

| Field | Value |
|-------|-------|
| Symbol library | `Device:Thermocouple` (standard KiCad library) |
| Footprint | **Not assigned** — physical connector type not decided |
| Connection | TC1 pin 1 → U1 VIN+ (via `Net-(TC1-+)`); TC1 pin 2 → U1 VIN- (via `Net-(TC1--)`) |

**Schematic status:** Placed and wired
**PCB status:** No footprint assigned, not in PCB layout

The TC1 ↔ U1 connection is confirmed in the PCB net list: `Net-(TC1-+)` and `Net-(TC1--)` are present and attached to U1 pads 2 and 4 respectively. The MCP9600 supports K, J, T, N, S, E, B, and R-type thermocouples — type is selected via I2C register configuration, not hardware. A physical thermocouple connector (e.g., panel-mount miniature thermocouple jack) must be chosen and footprint assigned before PCB completion.

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

**Schematic status:** Placed (no footprint annotation in schematic)
**PCB status:** Footprint placed in PCB directly; all 7 pins unconnected

All 7 J1 pins are `unconnected-` nets in the PCB (nets 13–19). The J1 footprint was placed in the PCB editor manually rather than being annotated in the schematic first. The schematic has global labels (SCL, SDA, ALERT_1–4, INT) that are intended to route through J1 to the host board, but no wires connect J1 pins to those signals in the schematic. See `docs/connector-pinout.md` for the intended pinout design.
