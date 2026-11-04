## Course outline {.smaller}

:::: {.columns}
::: {.column width=50%}
- [ ] **Day 1 LabVIEW + myRIO**
    - Automated Test Equipment
    - LabVIEW tutorials
    - Analog loopback with myRIO
    - **workshop**: frequency response test
- [ ] **Day 2 Instrument drivers**
    - Programmable instruments
    - DAQmx and VISA/SCPI drivers
    - Instrument automation
    - **workshop**: LM321 $V_{OS}$ and $I_S$ test
:::
::: {.column width=50%}
- [x] **Day 3 NI TestStand**
    - Sequences and action/test steps
    - Using code modules
    - Process models and callbacks
    - **workshop**: LM321 DC test
- [ ] **Day 4 Python for testing**
    - PyVISA and Streamlit libraries
    - CAN bus and CANopen
    - **workshop**: CANopen firmware test
:::
::::

## Workshop outcomes {.smaller}
1. Explain sequences, steps and adapters
2. Create a test sequence in NI TestStand
3. Build a TestStand sequence to measure DUT opamp supply current $I_{S}$

    | Group | Function |
    | - | --- |
    | **Setup** | Connect UDP3305S / UT8805E / NI-9269 / NI-9477 |
    | **Main** | - Supply AUX opamp ±15 V <br> - Turn switch S7 on <br> - Supply DUT opamp ±5 V <br> - **Test that current does not exceed 1.2 mA**
    | **Cleanup** | Turn off DUT supply <br> Turn off AUX supply <br> Turn S7 off <br> Release DAQmx/VISA resources |
