from logger import awg_logger
from VISAInterface import pyvisa_interface
import time


class AWG_connection:
    """
    Controller class for Keysight AWG (e.g., M8195A) communication via SCPI over LAN.
    Handles connection, communication, logging, and device limits.
    """

    def __init__(self, ip_address: str):
        # Device limits (fixed, not editable by user)
        self._device_voltage_limit = 3  # Volts
        self._device_frequency_limit = 6e9  # Hz
        self._device_power_limit = (self._device_voltage_limit ** 2) / 50  # Power (W) assuming 50Ω load

        # VISA interface setup
        self.visa = pyvisa_interface()
        self._rm = self.visa.rm
        self._resource = None

        # Logger setup
        self.log = awg_logger()

        # IP address
        self.ip_address = ip_address

    # --------------------- SETTINGS TAB METHODS ---------------------

    def connect(self):
        """Establish connection to the AWG using its IP address, and log IDN."""
        if self.log._log_file_path is None:
            self.log._initialize_log_file(f"awg_{self.ip_address}")

        try:
            start_time = time.time()
            self._resource = self._rm.open_resource(f"TCPIP0::{self.ip_address}::inst0::INSTR")
            self._resource.write_termination = '\n'
            self._resource.read_termination = '\n'
            self._resource.timeout = 5000  # milliseconds
            self.visa.resource = self._resource  # keep visa_interface in sync
            connect_duration = (time.time() - start_time) * 1000

            # Query *IDN?
            idn_start = time.time()
            idn = self._resource.query("*IDN?")
            idn_duration = (time.time() - idn_start) * 1000

            self.log._log_command(f"TCPIP0::{self.ip_address}::inst0::INSTR", duration_ms=connect_duration, response=True)
            self.log._log_command("*IDN?", duration_ms=idn_duration, response=idn.strip())

            return {"IDN": idn.strip(), "ConnectTime(ms)": connect_duration}

        except Exception as e:
            self.log._log_command(f"TCPIP0::{self.ip_address}::inst0::INSTR", duration_ms=0, response=str(e))
            return {"Error": str(e), "ConnectTime(ms)": None}

    def disconnect(self):
        """Close the AWG connection and log the action."""
        if self._resource is not None:
            start_time = time.time()
            self._resource.close()
            duration = (time.time() - start_time) * 1000
            self.log._log_command("resource.close()", duration_ms=duration, response="Device disconnected")
            self._resource = None
            self.visa.resource = None
            return {"Status": "Disconnected", "Duration(ms)": duration}
        else:
            self.log._log_command("resource.close()", duration_ms=0, response="Device not connected")
            return {"Status": "Device not connected", "Duration(ms)": 0}
        
    def is_connected(self):
        if self._resource is not None:
            return "Device connected"
        else:
            return "Device not connected"
        
    def get_resource(self):
        """return the connected resource"""
        return self._resource
