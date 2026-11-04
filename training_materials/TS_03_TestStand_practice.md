## LM321 specification {.smaller}

![LM321](figs/TS_03_LM321_spec.jpg)\


## $I_{S}$ measurement {.smaller}

:::: {.columns}
::: {.column width=50%}
1. **UDP3305S**: supply CH1 (15 V) / CH2 (15 V)
2. **UT8805E**: measure DC current using the 20 mA range
:::
::: {.column width=50%}
3. **NI-9477**: control switch S7
4. **NI-9269**: supply AO0 (5 V) / AO1 (5 V)
:::
::::
![IS](figs/Instr_01_IS_meas.jpg)\

## TestStand practice: $I_{S}$ measurement {.smaller}

| Group | Code modules | Function | Variables | 
| :- | :- | :---- | :-- |
| **Setup** | `pps_connect` <br> `dmm_connect` <br> `switch_init` <br> `ao_init` | Connect UDP3305S <br> Connect UT8805E <br> Connect NI-9477 <br> Connect NI-9269 | &rarr; `FG.ppsRef`^[VISA/DAQmx resources use the [`LabVIEWIOControl` type](https://knowledge.ni.com/KnowledgeArticleDetails?id=kA03q000000YGp8CAG&l=en-TH)] <br> &rarr; `FG.dmmRef`^[LC means Locals, FG means FileGlobals, SG means StationGlobals] <br> &rarr; `FG.switchRef` <br> &rarr; `FG.aoRef` |
| **Main** | `pps_ctrl` <br> `switch_ctrl` <br> `ao_update` <br> Numeric Limit Test (`dmm_read`) | Supply AUX ±15 V <br> Turn S7 on <br> Supply DUT ±5 V <br> Test $I_{S}$ < 1.2 mA | |
| **Cleanup** |`visa_close` <br> `daqmx_stop` | Close the VISA connection <br> Close the DAQmx connection | &larr; ... <br> &larr; ... |

## TestStand practice {.smaller}
![TestStand](figs/TS_03_TS_IS.jpg)\

## TestStand practice: sequence call {.smaller}

| Group | Code modules | Function | Variables | 
| :- | :-- | :--- | :-- |
| **Setup** | ... | ... | ... |
| **Main** | `pps_ctrl` <br> `ao_update` <br> Call `I_S_test` | Supply AUX ±15 V <br> Supply DUT ±5 V <br> Test $I_{S}$ < 1.2 mA | ... |
| **Cleanup** | ... | ... | ... |

<br>

:::: {.columns}
::: {.column width=20%}
#### Sub-sequence: "I_S test"
:::
::: {.column width=75%}

::: {style="border: 2px solid black; padding: 10px; display: inline-block;"}

| Group | Code modules | Function | 
| :- | :--- | :--- |
| **Setup** | `switch_ctrl` | Turn S7 on |
| **Main** | Numeric Limit Test (`dmm_read`) | Test $I_{S}$ < 1.2 mA |
| **Cleanup** | `switch_ctrl` | Turn S7 off |

:::

:::
::::
