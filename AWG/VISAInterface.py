import pyvisa

class pyvisa_interface:
    def __init__(self):
        self.rm = pyvisa.ResourceManager()
        self.resource = None