from attenuator import Attenuator

print(isinstance(float(50), float))

class Attenuator024(Attenuator):
    def __init__(self, com_address, baudrate, timeout):
        super().__init__(com_address, baudrate, timeout)

        id_str = self.id()
        assert('024' in id_str)

    def id(self):
        '''Instrument ID string'''
        self.write_serial('CL_IDENTITY?#')
        return self.read_serial

    def reset(self):
        '''Reset instrument.'''
        self.write_serial('CL_RESET_INST#')

    @property
    def attenuation(self):
        '''Current attenuation [dB]'''
        self.write_serial('CL_VALUE_SET?#')
        return self.read_serial
    
    @attenuation.setter
    def attenuation(self, atten_db):
        '''Allowed values between 0-50 dB with 0.1 dB precision'''
        if 0 < atten_db < 50:
            self.write_serial(f'CL_VALUE_SET {atten_db}#')
            self.read_serial
        else:
            raise(ValueError('Not an excepted attenuation'))
