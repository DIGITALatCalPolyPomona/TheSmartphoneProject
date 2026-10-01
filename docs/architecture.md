# Hardware Architecture

## System Context

This daughter board is a peripheral sensor module designed to plug into the
**Zynq-Carrier-Power** host board (a carrier/template for pinguz97's Zynq SoM,
separate repository: https://github.com/eryn-chen/Zynq-Carrier-Power). The host
board was intended to provide 3.3V power and act as the I2C master — though no
power/ground pin is currently assigned on J1 and no J1-compatible mate exists
on the carrier design, so the host interface is unresolved. This board contains
two sensors that respond as I2C slaves.

## Block Diagram

```
┌─────────────────────────────────────────────────────┐
│               Host Board (Zynq-Carrier-Power)        │
│                                                     │
│  Zynq-7000 FPGA / PS                                │
│    I2C Master                                       │
│    I2C Pull-ups (expected on host side)             │
└──────────────────────┬──────────────────────────────┘
                       │
                  J1 (7-pin, 1mm pitch)
                  Schematic labels: INT, ALERT_4..1,
                           SDA, SCL — NO +3.3V/GND pin ⚠
                       │
┌──────────────────────▼──────────────────────────────┐
│           Thermometer Daughter Board                 │
│                                                     │
│  +3.3V ─ dead-end stub near U1.EXP ────► U2.VDD    │
│              (reaches no J1 pin; U1.VDD unpowered)  │
│        ┌───────────┐            ┌────────────┐     │
│        │ U1         │            │ U2          │    │
│        │ MCP9600-E_MX│            │ BMP581      │   │
│        │ Thermocouple│            │ Pressure    │   │
│        │ Amplifier   │            │ Sensor      │   │
│        │ I2C: 0x60*  │            │ I2C: 0x46*  │   │
│        │ QFN-20+EP   │            │ LGA-10      │   │
│        │ (30-pad fp) │            │             │   │
│        └──┬──────────┘            └──────────┬──┘   │
│      miswired ⚠                        miswired ⚠  │
│  SCL pin→GND, SDA float,          SCL pin→+3.3V,   │
│  ALERT_2/4 swapped,               SDA float,       │
│  ADDR on SCL net                  SDO↔INT swapped  │
│                                                     │
│  TC1 (Thermocouple) ── wires stop short of U1 ⚠    │
│  *addresses are intent only — see I2C Bus           │
└─────────────────────────────────────────────────────┘
```

## I2C Bus

Both U1 and U2 were intended to share a single I2C bus with the Zynq host as the
only master. **As drawn, neither device is actually on the bus:** U1's SCL pin is
tied to GND and its SDA pin floats; U2's SCL pin is tied to +3.3V and its SDA pin
floats. The `SCL`/`SDA` global labels reach J1 (pins 7/6) but land on the wrong
device pins (U1.ADDR, U2.CSB / nothing).

| Device | Address (intent) | Address Pin | Actual wiring |
|--------|---------|-------------|---------------|
| U1 MCP9600 | 0x60 | ADDR → `SCL` net (should be strapped/float for 0x60) | Miswired — address indeterminate |
| U2 BMP581 | 0x46 | SDO/ADR → `INT` net (should be GND for 0x46) | Miswired — address indeterminate |

**Pull-up resistors:** None on this board. The host board (Zynq-Carrier-Power)
was expected to provide SCL and SDA pull-ups to 3.3V.

## Signal Inventory

Two connectivity truths exist and differ: the **schematic** (what the labels and
wires currently implement) and the **PCB netlist** (stale — captured before the
J1 label row and symbol rewiring were added; "Update PCB from Schematic" was
never run since). The table shows both.

| Signal | Schematic connectivity (verified 2026-10-01) | PCB netlist (stale) |
|--------|--------|------------|
| +3.3V | U2 VDD (pin 10), U2 SCK/SCL (pin 2) ⚠, dead-end stub near U1 EXP; **no J1 pin** | `+3.3V` net on U1 VDD pad 8 (from pre-rewire netlist) |
| GND | U1 SCL pin 19 ⚠, U2 INT pin 7 ⚠; U1/U2 real GND pins floating; **no J1 pin** | `GND` net on U1 pads 1,3,5,6,7,9,10,13,17,18 (stale) |
| TC1 + | TC1 pin 1 — wire ends before reaching U1 VIN+ pin ⚠ | `Net-(TC1-+)` on U1 pad 2 (stale) |
| TC1 − | TC1 pin 2 — wire ends before reaching U1 VIN− pin ⚠ | `Net-(TC1--)` on U1 pad 4 (stale) |
| Net-(U1-EXP-Pad21) | U1 EXP pads 21–30 — anonymous net, floating | Same — **NOT GND** ⚠ |
| SCL | J1.7 + U1 **ADDR** (16) + U2 **CSB** (6) — wrong pins ⚠ | `unconnected-(J1-Pin_7)` etc.; U1-SCL on `unconnected-(U1-SCL-Pad19)` |
| SDA | J1.6 only — dead end (U1 pin 20, U2 pin 4 unconnected) | `unconnected-` nets |
| ALERT_1 | J1.5 only — dead end (U1 pin 11 bare) | `unconnected-` nets |
| ALERT_2 | J1.4 + U1 pin 15 (physical ALERT_4 — swapped ⚠) | `unconnected-` nets |
| ALERT_3 | J1.3 + U1 pin 14 ✓ (only correct alert) | `unconnected-` nets |
| ALERT_4 | J1.2 + U1 pin 12 (physical ALERT_2 — swapped ⚠) | `unconnected-` nets |
| INT | J1.1 + U2 **SDO/ADR** (5) — should be U2 INT (7), which is grounded ⚠ | `unconnected-` nets |

The ALERT outputs (MCP9600) are register-configurable (push-pull or open-drain,
active-high/low) per datasheet DS20005426 — whether host pull-ups are needed
depends on the programmed configuration; none exist on this board either way.

## Power Architecture

- **Supply:** Intended single 3.3V rail from the host — **but no J1 pin is assigned to +3.3V or GND**, so the board currently has no defined power entry. Resolving this (pin reassignment, wider connector, or separate power) is a required design decision.
- **No local regulation:** No LDO or switching regulator on this board
- **BMP581 dual supply:** Requires both VDD and VDDIO — only VDD (pin 10) is actually on +3.3V; VDDIO (pin 1) is unconnected ⚠
- **Decoupling capacitors:** None exist — the schematic contains zero capacitor/resistor symbols; required before fabrication
- **Exposed pad (U1) — DESIGN ISSUE:** MCP9600 EXP pads (21–30) are NOT connected to GND. They form an isolated net `Net-(U1-EXP-Pad21)` in the PCB. The datasheet requires the exposed thermal pad to be soldered to a GND plane. This must be corrected in the schematic before fabrication.

## PCB Design Parameters

Sourced from `thermometer.kicad_pro`:

| Parameter | Value |
|-----------|-------|
| Layer count | 2 (F.Cu front copper, B.Cu back copper) |
| Board thickness | 1.6mm |
| Default track width | 0.2mm |
| Default via diameter | 0.6mm |
| Default via drill | 0.3mm |
| Minimum clearance | 0.2mm |
| Paper size | A4 |
| Grid | Not specified (KiCad default) |

## Current PCB State

| Item | Status |
|------|--------|
| Board outline (Edge.Cuts) | Empty — no board shape defined |
| U1 MCP9600 footprint | Placed on F.Cu |
| J1 connector footprint | Placed |
| U2 BMP581 footprint | Not placed |
| TC1 thermocouple footprint | Not assigned, not placed |
| Copper traces | None routed |
| Copper pours / zones | None defined |
| Decoupling capacitors | Not placed |
| I2C pull-up resistors | Not on this board (host board responsibility) |
