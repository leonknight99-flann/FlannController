from . import Attenuator


class Attenuator024(Attenuator):
    def __init__(self, com_address, baudrate, timeout):
        super().__init__(com_address, baudrate, timeout)

    def id(self):
        '''Instrument ID string'''
        self.write_serial('CL_IDENTITY?#')
        return self.read_serial

    def reset(self):
        '''Reset instrument.'''
        self.write_serial('CL_RESET_INST#')

    @property
    def attenuation(self):
        pass