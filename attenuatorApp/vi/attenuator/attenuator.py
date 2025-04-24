import serial
import serial.serialwin32

import socket

import time

class Attenuator:
    def __init__(self, address: str='', baudrate: int=0, timeout: float=0, timedelay=0, tcp_port: int=0):
        if not tcp_port:
            self._resource = serial.Serial(address, baudrate, timeout=timeout)
        else:
            self._resource = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4 and TCP
            self._resource.connect((address, tcp_port))

        self.echo = False

        self.timedalay = timedelay

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

    def read(self):
        if isinstance(self._resource, serial.serialwin32.Serial):
            fn = self._resource.readline().decode()
        elif isinstance(self._resource, socket.socket):
            time.sleep(self.timedalay)
            fn = self._resource.recv(1024).decode(errors='ignore')
        else:
            raise RuntimeError("read unreachable")
        return fn

    def write(self, cmd: str):
        if self.echo:
            print(cmd)

        if isinstance(self._resource, serial.serialwin32.Serial):
            fn = self._resource.write
        elif isinstance(self._resource, socket.socket):
            fn = self._resource.sendall
        else:
            raise RuntimeError("write unreachable")
        return fn(cmd.encode())


    