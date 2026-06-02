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
│           │SCL,SDA                    SCL,SDA│      │
│           │ALERT_1–4                      INT│      │
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

| Signal | Source | Destination | Status |
|--------|--------|-------------|--------|
| SCL | J1 pin (TBD) | U1 pin 19, U2 pin 2 | In schematic via global label |
| SDA | J1 pin (TBD) | U1 pin 20, U2 pin 4 | In schematic via global label |
| +3.3V | J1 pin 1 (intended) | U1 VDD, U2 VDD, U2 VDDIO | In schematic |
| GND | J1 pin 2 (intended) | U1 GND, U2 GND | In schematic |
| ALERT_1 | U1 pin 11 | J1 (TBD) | In schematic, not wired to J1 |
| ALERT_2 | U1 pin 12 | J1 (TBD) | In schematic, not wired to J1 |
| ALERT_3 | U1 pin 14 | J1 (TBD) | In schematic, not wired to J1 |
| ALERT_4 | U1 pin 15 | J1 (TBD) | In schematic, not wired to J1 |
| INT | U2 pin 7 | J1 (TBD) | In schematic, not wired to J1 |

The ALERT outputs (MCP9600) are open-drain active-low. They require pull-up resistors
(on host board) and can be configured for threshold monitoring via I2C registers.

## Power Architecture

- **Supply:** Single 3.3V rail from J1
- **No local regulation:** No LDO or switching regulator on this board
- **BMP581 dual supply:** Requires both VDD and VDDIO; both tied to the same 3.3V rail
- **Decoupling capacitors:** None currently placed in PCB — required before fabrication
- **Exposed pad (U1):** MCP9600 thermal pad (pad 21) and 9 thermal vias (pads 22–30) connected to GND for thermal relief

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
