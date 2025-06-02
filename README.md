# Flann Programmable Device's Python Libary

Python libary to connect to Flann's programmable instruments and standardise the command structure.

## Examples

```python
from flann.vi.switch import Switch337
switch_box1 = Switch337(switch=1, address='COM5', timedelay=0.3, timeout=0, baudrate=31250)
switch_box1.toggle_all()  # Toggle all switches connected to the switch-box
switch_box1.switch = 2  # Selecting switch 2
switch_box1.position1()  # Switching switch 2 to position 1
```

```python
from flann.vi.attenuator import Attenuator024
atten = Attenuator024(address='COM3', timedelay=0.1, timeout=0.44, baudrate=31250)
print(atten.id())  # Prints the identification of the attenuator
atten.attenuation = 20.5  # Sets the attenuation to 20.5 dB
print(atten.attenuation())  # get the current attenuation value
```

```python
from flann.vi.attenuator import Attenuator625
atten = Attenuator625(address='10.1.4.4', timedelay=0.1, tcp_port=10001)
print(atten.id())  # Prints the identification of the attenuator
atten.position = 500  # Sets the position to 500 steps
print(atten.position())  # get the current position steps value
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
