from .attenuator import Attenuator


class Attenuator625(Attenuator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # id_str = self.id()
        # assert('625' in id_str)

    def id(self):
        '''Instrument ID string'''
        self.write('IDENTITY?\r\n')
        return self.read

    def reset(self):
        '''Reset instrument.'''
        self.write('RESET_INST\r\n')

    @property
    def attenuation(self):
        '''Current attenuation [dB]'''
        self.write('VALUE_SET?\r\n')
        return self.read
    
    @attenuation.setter
    def attenuation(self, atten_db):
        '''Allowed values between 0-60 dB with 0.1 dB precision'''
        if 0 <= atten_db <= 60:
            self.write(f'VALUE_SET {atten_db}\r\n')
            self.read
        else:
            raise(ValueError('Not an excepted attenuation'))
        
    @property
    def position(self):
        '''Current Step Position'''
        self.write('STEPS_SET?')
        return self.read
    
    @position.setter
    def position(self, steps):
        '''Allowed values between 0-9799'''
        if all([0<=steps<=9799,isinstance(steps,int)]):
            self.write(f'STEPS_SET {steps}\r\n')
            self.read
        else:
            raise(ValueError('Not an excepted steps position'))
        
    @property
    def increment_store(self):
        '''Current incremental value [dB]'''
        self.write('INCR_SET?\r\n')
        return self.read
    
    @increment_store.setter
    def increment_store(self, increment):
        '''Allowed values between 0-10 dB'''
        if 0 <= increment <= 10:
            self.write(f'INCR_SET {increment}\r\n')
            self.read
        else:
            raise(ValueError('Not an excepted incrementation'))
        
    def increment(self):
        self.write('INCREMENT\r\n')
        self.read

    def decrement(self):
        self.write('DECREMENT\r\n')
        self.read