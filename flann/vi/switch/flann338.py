from flann.vi import FlannProgrammable

class Switch338(FlannProgrammable):
    def __init__(self, address: str, timedelay: float=0):# baudrate: int=0, timeout: float=0, timedelay=0, tcp_port: int=0):
        super().__init__(address, timedelay)  # baudrate, timeout, timedelay, tcp_port)
        self._resource.port = address