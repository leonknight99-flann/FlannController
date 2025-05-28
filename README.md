# Flann Programmable Device's Python Libary

Python libary to connect to Flann's programmable instruments and standardise the command structure.

## Example

```python
>>> from flann.vi.switch import Switch337
>>> with CommChannel(address=6) as vna:
...     vna.ch3.parameter = "S21"
...     s21 = vna.read(channel=3, data_status="corrected")
>>> 
```

## Applications
Software to control Flann's programmable devices. These currently include:

- Attenuator Application (inspired by the 625 layout)
    - 024 variable attenuator
    - 625 programmable RVA (Rotary Vane Attenuators)

- Switch Application with IMS 2025 demo
    - 337 dual-switch controller

- Switch Counter
    - 27337 IMS 2025 demo

Future plans:
- 624 programmable RVA (Rotary Vane Attenuators)
- 338 switch
