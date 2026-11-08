## Workshop preparation {.smaller}
1. Explain how instruments connect to the DUT
    - Operate instruments manually and through remote software control
2. Build LabVIEW SubVIs to measure $I_{S}$ and $V_{offset}$

| VI | Device | Driver | Function |
| --- | - | - | ---- |
| `ao_init` / `ao_update` | NI-9269 | DAQmx | Supply the DUT opamp |
| `ai_init` / `ai_measure` | NI-9239 | DAQmx | Measure voltage |
| `switch_init` / `switch_ctrl` | NI-9477 | DAQmx | Control switch ON/OFF states |
| `pps_init` / `pps_update` | UDP3305S | VISA | Supply the AUX opamp |
| `dmm_init` / `dmm_read` | UT8805E | VISA | Read current |

## Workshop: LM321 $V_{OS}$ and $I_S$ test {.smaller}

| State | Device: VI | Settings |
| - | ----- | ---- |
| **Setup** | NI-9269: `ao_init` <br> NI-9239: `ai_init` <br> NI-9477: `switch_init` <br> UT8805E: `dmm_connect` <br> UDP3305S: `pps_connect`, `pps_ctrl` | DUT opamp $V_S$: CH1 = 15V, CH2 = -15V <br> **START** button $\rightarrow$ **$V_{OS}$ test** |
| **$V_{OS}$ test** | NI-9269: `ao_update` <br> NI-9239: `ai_measure` | DUT opamp $V_S$: A0 = 5V, A1 = -5V |
| **$I_S$ test** | NI-9477: `switch_ctrl` ON <br> UT8805E: `dmm_read` <br> NI-9477: `switch_ctrl` OFF | **START** button $\rightarrow$ **$V_{OS}$ test** <br> **FINISH** button $\rightarrow$ **Cleanup** |
| **Cleanup** | NI-9269: `ao_update` <br> UDP3305S: `pps_ctrl` <br> VISA close, DAQmx stop | DUT opamp $V_S$: A0/A1 = 0V <br> AUX opamp $V_S$: CH1/CH2 = 0V |