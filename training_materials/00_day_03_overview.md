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
3. Build a TestStand sequence to test DUT (LM321 opamp)

    | Group | Function |
    | - | ---- |
    | **Setup** | - Activate UDP3305S / UT8805E / NI-9269 / NI-9477 <br> - Turn ON AUX supply |
    | **Main** | - Turn ON DUT supply <br> - **SubSequence**: $I_S$ < 1.2 mA <br> - **SubSequence**: $V_{OS}$ < 7 mV <br> - Turn OFF DUT supply
    | **Cleanup** | - Turn OFF AUX supply <br> - Release DAQmx/VISA resources |
