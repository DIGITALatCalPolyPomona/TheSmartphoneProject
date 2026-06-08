# Hardware Architecture

## System Context

This daughter board is a peripheral sensor module designed to plug into the
**Zynq-Carrier-Power** host board (a Zynq-7000 FPGA carrier, separate repository:
https://github.com/eryn-chen/Zynq-Carrier-Power). The host board provides 3.3V
power and acts as the I2C master. This board contains two sensors that respond
as I2C slaves.

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
                  Signals: +3.3V, GND, SCL, SDA,
                           ALERT/INT (3 pins, TBD)
                       │
┌──────────────────────▼──────────────────────────────┐
│           Thermometer Daughter Board                 │
│                                                     │
│  +3.3V ──────┬────────────────────────────┐        │
│              │                            │        │
│        ┌─────▼──────┐            ┌────────▼────┐   │
│        │ U1          │            │ U2           │   │
│        │ MCP9600-E_MX│            │ BMP581       │   │
│        │ Thermocouple│            │ Pressure     │   │
│        │ Amplifier   │            │ Sensor       │   │
│        │ I2C: 0x60   │            │ I2C: 0x46    │   │
│        │ QFN-30      │            │ LGA-10       │   │
│        └──┬──────────┘            └──────────┬──┘   │
│           │SCL,SDA (not wired)        SCL,SDA│      │
│           │ALERT_1–4 (not wired)          INT│      │
│  GND ─────┴───────────────────────────────┴─┘      │
│                                                     │
│  TC1 (External Thermocouple) ──► U1 VIN+/VIN-      │
└─────────────────────────────────────────────────────┘
```

## I2C Bus

Both U1 and U2 share a single I2C bus. The Zynq host is the only master.

| Device | Address | Address Pin | Notes |
|--------|---------|-------------|-------|
| U1 MCP9600 | 0x60 | ADDR floating | Default address (ADDR=0) |
| U2 BMP581 | 0x46 | SDO/ADR = GND | SDO tied low in schematic |

**Pull-up resistors:** None on this board. The host board (Zynq-Carrier-Power)
is responsible for SCL and SDA pull-ups to 3.3V.

## Signal Inventory

The PCB net list is the ground truth for connectivity. Signals listed as "schematic only" exist as global labels in the schematic but do not appear as named nets in the PCB because U2 is not placed and/or U1's pins are unconnected.

| Signal | Source | Destination | PCB Status |
|--------|--------|-------------|------------|
| +3.3V | J1 pin (TBD) | U1 VDD (pad 8), U2 VDD, U2 VDDIO | Named net in PCB ✓ |
| GND | J1 pin (TBD) | U1 pads 1,3,5,6,7,9,10,13,17,18; U2 pins 3,8,9 | Named net in PCB ✓ |
| Net-(TC1-+) | TC1 pin 1 | U1 VIN+ (pad 2) | Named net in PCB ✓ |
| Net-(TC1--) | TC1 pin 2 | U1 VIN- (pad 4) | Named net in PCB ✓ |
| Net-(U1-EXP-Pad21) | U1 EXP pads 21–30 | (nothing) | **Floating — NOT GND** ⚠ |
| SCL | J1 pin (TBD) → U2 pin 2 | U1 pin 19 **unconnected** | Schematic only; U1-SCL unconnected in PCB |
| SDA | J1 pin (TBD) → U2 pin 4 | U1 pin 20 **unconnected** | Schematic only; U1-SDA unconnected in PCB |
| ALERT_1 | U1 pin 11 | J1 (TBD) | U1-ALERT_1 unconnected in PCB |
| ALERT_2 | U1 pin 12 | J1 (TBD) | U1-ALERT_2 unconnected in PCB |
| ALERT_3 | U1 pin 14 | J1 (TBD) | U1-ALERT_3 unconnected in PCB |
| ALERT_4 | U1 pin 15 | J1 (TBD) | U1-ALERT_4 unconnected in PCB |
| INT | U2 pin 7 | J1 (TBD) | Schematic only; U2 not in PCB |
| ADDR | U1 pin 16 | (floating) | Unconnected in PCB → default 0x60 |

**Note on SCL/SDA:** Global labels `SCL` and `SDA` exist in the schematic and are connected to U2 (BMP581) pins 2 and 4. However, U1's SCL (pin 19) and SDA (pin 20) are NOT connected to these global labels in the schematic — they are unconnected in both schematic and PCB. This is a significant design gap that must be addressed when work resumes.

The ALERT outputs (MCP9600) are open-drain active-low. They require pull-up resistors
(on host board) and can be configured for threshold monitoring via I2C registers.

## Power Architecture

- **Supply:** Single 3.3V rail from J1
- **No local regulation:** No LDO or switching regulator on this board
- **BMP581 dual supply:** Requires both VDD and VDDIO; both tied to the same 3.3V rail
- **Decoupling capacitors:** None currently placed in PCB — required before fabrication
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
