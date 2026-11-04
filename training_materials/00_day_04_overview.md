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
- [ ] **Day 3 NI TestStand**
    - Sequences and action/test steps
    - Using code modules
    - Process models and callbacks
    - **workshop**: LM321 DC test
- [x] **Day 4 Python for testing**
    - PyVISA and Streamlit libraries
    - CAN bus and CANopen
    - **workshop**: CANopen firmware test
:::
::::

## Workshop outcomes {.smaller}

1. Explain how Python connect, control, and import data from instruments
2. Explain how to develop web-based UI using Streamlit
3. Write Python code to automate and coordinate multiple instruments
    - Provide web-based UI for instrument configuration
    - Generate step-wise signals using UDP3305S
    - Measure signals periodically using UT8805E
    - Display results in table format
    - Record test data to CSV file
