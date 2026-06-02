# Component Reference

## U1 — MCP9600-E_MX (Thermocouple Amplifier)

| Field | Value |
|-------|-------|
| Manufacturer | Microchip Technology |
| Part number | MCP9600-E/MX |
| Function | Thermocouple EMF-to-temperature converter with cold-junction compensation |
| Package | QFN-30 (5.0×5.0×1.0mm, 0.65mm pitch) |
| Supported thermocouple types | K, J, T, N, S, E, B, R |
| I2C address | 0x60 (ADDR pin floating → default) |
| Supply voltage | 2.7V – 5.5V (3.3V used here) |
| Symbol library | `jackboys:MCP9600-E_MX` (local, `jackboys.kicad_sym`) |
| Footprint library | `jackboys2:QFN65P500X500X100-21N_MCP9600-E_MX` (local, `jackboys2.pretty/`) |
| Datasheet | https://ww1.microchip.com/downloads/en/DeviceDoc/MCP9600-Data-Sheet-DS20005426E.pdf |

**Schematic status:** Placed and wired
**PCB status:** Footprint placed, not routed

### Pins used in schematic

| Pin | Name | Connection |
|-----|------|-----------|
| 2 | VIN+ | TC1 pin 1 (thermocouple positive) |
| 4 | VIN- | TC1 pin 2 (thermocouple negative) |
| 8 | VDD | +3.3V |
| 11 | ALERT_1 | Global label `ALERT_1` |
| 12 | ALERT_2 | Global label `ALERT_2` |
| 14 | ALERT_3 | Global label `ALERT_3` |
| 15 | ALERT_4 | Global label `ALERT_4` |
| 16 | ADDR | Floating (no net) → address 0x60 |
| 19 | SCL | Global label `SCL` |
| 20 | SDA | Global label `SDA` |
| 21–30 | EXP/GND | GND (thermal pad + thermal vias) |
| Multiple | GND | GND |

---

## U2 — BMP581 (Barometric Pressure Sensor)

| Field | Value |
|-------|-------|
| Manufacturer | Bosch Sensortec |
| Part number | BMP581 |
| Function | 24-bit absolute barometric pressure and temperature sensor |
| Package | LGA-10 (2.0×2.0mm, 0.5mm pitch) |
| I2C address | 0x46 (SDO/ADR = GND per schematic label) |
| Pressure range | 30–125 kPa |
| Supply voltage | 1.71V – 3.6V (3.3V used here; VDD and VDDIO both tied to 3.3V) |
| Symbol library | `BMP581:BMP581` (**NOT in repo** — must reinstall from SnapEDA) |
| Footprint library | `BMP581:BMP581` (**NOT in repo** — must reinstall from SnapEDA) |
| Datasheet | https://www.bosch-sensortec.com/products/environmental-sensors/pressure-sensors/bmp581/ |
| SnapEDA source | https://www.snapeda.com/parts/BMP581/Bosch/view-part/ |

**Schematic status:** Placed and wired
**PCB status:** NOT placed — U2 is absent from the PCB layout entirely

**ACTION REQUIRED before opening project:** The `BMP581:BMP581` library is missing from this repo. KiCad will show missing symbol/footprint errors. See `docs/library-notes.md` for reinstall steps.

### Pins used in schematic

| Pin | Name | Connection |
|-----|------|-----------|
| 1 | VDDIO | +3.3V |
| 2 | SCK/SCL | Global label `SCL` |
| 3 | GND | GND |
| 4 | SDI/SDA | Global label `SDA` |
| 5 | SDO/ADR | GND (sets I2C address to 0x46) |
| 6 | CSB | +3.3V (selects I2C mode, not SPI) |
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
| Connection | TC1 pin 1 → U1 VIN+; TC1 pin 2 → U1 VIN- |

**Schematic status:** Placed and wired
**PCB status:** No footprint assigned, not in PCB layout

The MCP9600 supports K, J, T, N, S, E, B, and R-type thermocouples. The type is selected via firmware configuration over I2C, not hardware. A physical thermocouple connector (e.g., panel-mount miniature TC connector) needs to be chosen and footprint assigned before PCB completion.

---

## J1 — Interface Connector

| Field | Value |
|-------|-------|
| Description | 7-pin single-row pin header |
| Symbol library | `Connector_Generic:Conn_01x07` (standard KiCad library) |
| Footprint library | `Connector_PinHeader_1.00mm:PinHeader_1x07_P1.00mm_Vertical` (standard KiCad library) |
| Pitch | 1.00mm |
| Style | Through-hole, vertical |
| PCB location | (104.375, 75.945) mm |

**Schematic status:** Placed
**PCB status:** Footprint placed, all 7 pins unconnected

All 7 J1 pins are `unconnected-` nets in the PCB. The schematic shows global labels (SCL, SDA, ALERT_1–4, INT) that were intended to be routed to J1, but the net connections were never drawn. See `docs/connector-pinout.md` for the intended pinout design.
