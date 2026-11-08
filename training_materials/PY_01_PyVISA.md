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


## PyVISA template: module style {.smaller}

:::: {.columns}
::: {.column width=80%}
```python
import pyvisa

_rm = None
_instr = None

def pps_init(visa_res_name:str):
    global _rm, _instr
    _rm = pyvisa.ResourceManager()
    _instr = _rm.open_resource(visa_res_name)

def pps_update(vsp:float, vsp_state:bool, vsn:float, vsn_state:bool):
    _instr.write(f':SOURce1:VOLTage {vsp}')
    _instr.write(f'OUTPut:STATe CH1,{vsp_state:d}')
    _instr.write(f':SOURce2:VOLTage {vsn}')
    _instr.write(f'OUTPut:STATe CH2,{vsn_state:d}')

def pps_close():
    _instr.close()
    _rm.close()
```
:::
::: {.column width=20%}
#### Step setting:
- Operation scope: module
- Operation type: call method
:::
::::

## PyVISA template: class style {.smaller}

:::: {.columns}
::: {.column width=75%}
```python
import pyvisa

class pps_class(object):
    def __init__(self, visa_res_name:str):
        self._rm = pyvisa.ResourceManager()
        self._instr = self._rm.open_resource(visa_res_name)

    def update(self, vsp:float, vsp_state:bool, vsn:float, vsn_state:bool):
        self._instr.write(f':SOURce1:VOLTage {vsp}')
        self._instr.write(f'OUTPut:STATe CH1,{vsp_state:d}')
        self._instr.write(f':SOURce2:VOLTage {vsn}')
        self._instr.write(f'OUTPut:STATe CH2,{vsn_state:d}')

    def close(self):
        self._instr.close()
        self._rm.close()
```
:::
::: {.column width=25%}
#### 1. Initialize object
- Operation scope: Create class instance
- Pass object into **FileGlobals** or **Locals** variable

#### 2. Invoke methods
- Operation scope: class instance
- Operation type: call method
:::
::::

## [Streamlit](https://docs.streamlit.io/) {.smaller}

Open-source Python framework to run Python scripts as interactive web applications without needing to write HTML, CSS, or JavaScript.

```python
import 
```

