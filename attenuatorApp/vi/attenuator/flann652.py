from attenuator import Attenuator


class Attenuator625(Attenuator):
    def __init__(self, com_address, baudrate, timeout):
        super().__init__(com_address, baudrate, timeout)

        id_str = self.id()
        assert('625' in id_str)

    def id(self):
        '''Instrument ID string'''
        self.write_serial('IDENTITY?')
        return self.read_serial

    def reset(self):
        '''Reset instrument.'''
        self.write_serial('RESET_INST')

    @property
    def attenuation(self):
        '''Current attenuation [dB]'''
        self.write_serial('VALUE_SET?')
        return self.read_serial
    
    @attenuation.setter
    def attenuation(self, atten_db):
        '''Allowed values between 0-60 dB with 0.1 dB precision'''
        if 0 < atten_db < 60:
            self.write_serial(f'VALUE_SET {atten_db}')
            self.read_serial
        else:
            raise(ValueError('Not an excepted attenuation'))
        
    @property
    def position(self):
        '''Current Step Position'''
        self.write_serial('STEPS_SET?')
        return self.read_serial
    
    @position.setter
    def position(self, steps):
        '''Allowed values between 0-8000'''
        if all([0<steps<8000,isinstance(steps,int)]):
            self.write_serial(f'CL_STEPS_SET {steps}#')
            self.read_serial
        else:
            raise(ValueError('Not an excepted attenuation'))
