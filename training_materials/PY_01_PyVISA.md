## [PyVISA](https://www.pyvisa.com/docs) {.smaller}
Python package that provides bindings to the Virtual Instrument Software Architecture (VISA) library

:::: {.columns}
::: {.column width=40%}
#### Procedure
1. Install PyVISA library
    - Install with `pip install pyvisa`
2. Check instrument's **resource name** from NI MAX
:::
::: {.column width=60%}
#### Python code

```python
import pyvisa
rm = pyvisa.ResourceManager()
print(rm.list_resources())
pps = rm.open_resource('USB0::0xFFFF::0xFFFF::FFFFFF::INSTR')
volt = pps.query(':SOUR1:VOLT?\n')
print(volt)
```
:::
::::

#### Python advantages for VISA instruments
- Functions and libraries for text processing
- Known for data-oriented libraries: [Pandas](https://pandas.pydata.org/docs/), [Streamlit](https://docs.streamlit.io/), [OpenCV](https://docs.opencv.org/5.0/) 

## PyVISA for UDP3305S {.smaller}


## PyVISA for UT8805E {.smaller}


## Instrument coordination {.smaller}


## [Streamlit](https://docs.streamlit.io/) {.smaller}
