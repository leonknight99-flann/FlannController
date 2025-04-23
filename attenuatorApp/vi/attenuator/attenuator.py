import serial
import serial.serialwin32


class Attenuator:
    def __init__(self, com_address: str, baudrate: int, timeout: float):
        self._resource = serial.Serial(com_address, baudrate, timeout=timeout)

        self.echo = False

    @property
    def timeout(self) -> float | None:
        return self._resource.timeout
    
    @timeout.setter
    def timeout(self, timeout: float | None) -> None:
        self._resource.timeout = timeout

    @property
    def baudrate(self) -> int | None:
        return self._resource.baudrate
    
    @baudrate.setter
    def baudrate(self, baurate: int | None) -> None:
        self._resource.baudrate = baurate

    def close(self):
        self._resource.close()

    def read_serial(self):
        if isinstance(self._resource, serial.serialwin32.Serial):
            fn = self._resource.readline().decode()
        else:
            raise RuntimeError("read unreachable")
        return fn

    def write_serial(self, cmd: str):
        if self.echo:
            print(cmd)

        if isinstance(self._resource, serial.serialwin32.Serial):
            fn = self._resource.write
        else:
            raise RuntimeError("write unreachable")
        return fn(cmd.encode())


    