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
        if 0 <= atten_db <= 60:
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
        '''Allowed values between 0-9799'''
        if all([0<=steps<=9799,isinstance(steps,int)]):
            self.write_serial(f'STEPS_SET {steps}#')
            self.read_serial
        else:
            raise(ValueError('Not an excepted steps position'))
        
    @property
    def increment_store(self):
        '''Current incremental value [dB]'''
        self.write_serial('INCR_SET?')
        return self.read_serial
    
    @increment_store.setter
    def increment_store(self, increment):
        '''Allowed values between 0-10 dB'''
        if 0 <= increment <= 10:
            self.write_serial(f'INCR_SET {increment}')
            self.read_serial
        else:
            raise(ValueError('Not an excepted incrementation'))
        
    def increment(self):
        self.write_serial('INCREMENT')
        self.read_serial

    def decrement(self):
        self.write_serial('DECREMENT')
        self.read_serial