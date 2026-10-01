# J1 Connector Pinout

## Physical Specification

| Property | Value |
|----------|-------|
| Pins | 7 |
| Pitch | 1.00mm |
| Style | Single-row, through-hole, vertical |
| Footprint | `Connector_PinHeader_1.00mm:PinHeader_1x07_P1.00mm_Vertical` |
| PCB location | (104.375, 75.945) mm |
| Mating connector | TBD — no matching 1.00mm 7-pin connector was found in the Zynq-Carrier-Power submodule (it uses USB-C, barrel jack, 2.54mm headers, JST, and a DF40C SoM connector) |

## As-Implemented Pinout (in the schematic)

**The pins ARE assigned in the schematic** — seven global labels sit exactly on
J1's pin attach points (J1 is horizontally mirrored, so its pins face the label
row at x=40.64mm). As wired:

| Pin | Signal | Intended source | Notes |
|-----|--------|-----------------|-------|
| 1 | INT | U2 BMP581 | Interrupt — but see miswiring below |
| 2 | ALERT_4 | U1 MCP9600 | Reaches U1 pin 12 (physical ALERT_2 — swapped) |
| 3 | ALERT_3 | U1 MCP9600 | Reaches U1 pin 14 — correct |
| 4 | ALERT_2 | U1 MCP9600 | Reaches U1 pin 15 (physical ALERT_4 — swapped) |
| 5 | ALERT_1 | U1 MCP9600 | U1 pin 11 is bare; this net ends at J1 |
| 6 | SDA | I2C | U1 pin 20 is unconnected — this net ends at J1 |
| 7 | SCL | I2C | Reaches U1 pin 16 (ADDR) and U2 pin 6 (CSB) — wrong pins |

**Critical gap: no J1 pin carries +3.3V or GND.** All 7 pins are signals, so the
board currently has no defined power path from the host. This must be resolved
(fewer alert pins exposed, a wider connector, or a separate power path).

## Defects affecting this pinout (verified 2026-10-01)

The labels land on J1's pins, so miswiring propagates to the connector:

- `SCL` net = J1.7 + **U1 pin 16 (ADDR)** + **U2 pin 6 (CSB)** — U1's actual SCL
  pin (19) is tied to GND by a power symbol sitting on it.
- `SDA` net = J1.6 only — U1 pin 20 (SDA) and U2 pin 4 (SDI/SDA) are unconnected.
- `INT` net = J1.1 + **U2 pin 5 (SDO/ADR)** — U2's actual INT pin (7) is tied to
  GND. (For I2C address 0x46, SDO/ADR should go to GND; INT should be the alert line.)
- `ALERT_2`/`ALERT_4` nets are swapped relative to U1's physical pins.
- Pull-up planning is unvalidated: MCP9600 ALERT pins are **register-configurable
  (push-pull or open-drain, active-high/low)** per datasheet DS20005426 — whether
  host pull-ups are needed depends on the programmed configuration. No resistors
  exist on this board.

## PCB state

In `thermometer.kicad_pcb`, all 7 J1 pads carry auto-generated
`unconnected-(J1-Pin_N-PadN)` nets (indices 13–19 — auto-assigned, will shift on
any netlist change) and zero copper exists. The PCB netlist **predates the
schematic wiring** — "Update PCB from Schematic" has never been run since the
labels were placed, and must not be run until the schematic defects are fixed.

## Work Required to Complete J1

1. **Fix the schematic miswiring** (see `wiki/hardware/thermometer.md` defect list) — SCL pin off GND, ADDR to its proper net, SDO→GND / INT→INT on U2, ALERT_2/4 un-swapped, SDA to U1 pin 20.
2. **Resolve the power question** — assign +3.3V/GND on J1 (drops 2 signal pins) or define another power path; record the choice in a wiki decision page.
3. **Fill J1's schematic Footprint property** (currently blank — footprint was set PCB-side only).
4. **Run Update PCB from Schematic** — the `unconnected-` net names on the J1 pads will be replaced by INT/ALERT_*/SDA/SCL automatically.
5. **Confirm mating connector** — no mate exists in the current Zynq-Carrier-Power design; cable/adapter or carrier revision needed.
6. **Add decoupling capacitors** near U1 VDD and U2 VDD/VDDIO pins (none exist in schematic or PCB).
