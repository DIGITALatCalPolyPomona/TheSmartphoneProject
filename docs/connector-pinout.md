# J1 Connector Pinout

## Physical Specification

| Property | Value |
|----------|-------|
| Pins | 7 |
| Pitch | 1.00mm |
| Style | Single-row, through-hole, vertical |
| Footprint | `Connector_PinHeader_1.00mm:PinHeader_1x07_P1.00mm_Vertical` |
| PCB location | (104.375, 75.945) mm |
| Mating connector | TBD — depends on Zynq-Carrier-Power host board |

## Current Status

**ALL 7 pins are unconnected.** Each pin is assigned an `unconnected-` prefixed net in the PCB (nets 13–19). No copper traces connect J1 to any other component.

The schematic contains the following global labels that are intended to route through J1 to the host board: `SCL`, `SDA`, `ALERT_1`, `ALERT_2`, `ALERT_3`, `ALERT_4`, `INT`. However, in the current schematic these labels are connected to U1 and U2 pins but are not wired to J1 pins.

## Intended Pinout (Design Draft — NOT IMPLEMENTED)

Based on signals present in the schematic and the 7-pin constraint, the following is the logical intended assignment. This is a design proposal, not a completed specification.

| Pin | Signal | Direction | Source | Notes |
|-----|--------|-----------|--------|-------|
| 1 | +3.3V | Power in | Host → board | Power supply from Zynq carrier |
| 2 | GND | Power | Common | Return path |
| 3 | SCL | Input | Host → board | I2C clock |
| 4 | SDA | Bidirectional | Host ↔ board | I2C data |
| 5 | ALERT_1 | Output | U1 MCP9600 | Temperature threshold alert 1 |
| 6 | ALERT_2 | Output | U1 MCP9600 | Temperature threshold alert 2 |
| 7 | INT / ALERT | Output | U2 BMP581 or U1 | BMP581 interrupt or remaining MCP9600 alert |

**Design constraint:** With only 7 pins (2 for power, 2 for I2C = 3 remaining signal pins), not all 5 interrupt/alert outputs (ALERT_1–4, INT) can be exposed. Pins 5–7 assignment needs a decision:
- **Option A:** Expose ALERT_1, ALERT_2, INT (drop ALERT_3 and ALERT_4)
- **Option B:** Expose ALERT_1, ALERT_2, ALERT_3 (drop ALERT_4 and INT)
- **Option C:** Use a wider connector (8–10 pin) to accommodate all signals

Pull-up resistors for ALERT outputs: MCP9600 ALERT pins are open-drain. The host board is expected to provide pull-ups. No resistors are present on this daughter board.

## Work Required to Complete J1

1. **Decide final pinout** (see design constraint above) and document chosen option here
2. **Update schematic:** Draw wires from SCL/SDA/ALERT/INT global labels to J1 pins
3. **Remove DRC suppressions:** The `unconnected-` suppressors on J1 pins 1–7 will clear automatically once pins are connected
4. **Route PCB traces** from J1 to U1 (MCP9600) and U2 (BMP581) — U2 must be placed in PCB first
5. **Confirm mating connector** on Zynq-Carrier-Power host board matches 1mm pitch 7-pin layout
6. **Add decoupling capacitors** near U1 VDD and U2 VDD/VDDIO pins (none currently placed)
