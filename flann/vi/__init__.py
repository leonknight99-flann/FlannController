"""
.. module:: flann.vi
===============================================

Provides a class to interact with Flann's programmable instruments
using either serial or ethernet via socket

Flann Instument Classes
===============================================

attenuator.flann024
attenuator.flann624
attenuator.flann625
switch.flann337
switch.flann338

Flann Instrument Base Class
===============================================
All Flann's instruments are built upon the base class 'FlannProgrammable'

"""
from .programmableDrivers import FlannProgrammable
from . import attenuator, switch
