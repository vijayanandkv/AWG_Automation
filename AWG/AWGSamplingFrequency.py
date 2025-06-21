#import awg modules
from AWGConnection import AWG_connection
from logger import awg_logger

#import other modules
import time

class AWG_sampling_frequency:
    def __init__(self, ip_address):
        self.ip_address = ip_address

        #create insatces for connection and logger classes
        self.connection = AWG_connection(ip_address)
        self.log = awg_logger()

        #select the recourse from connection class
        self.resource = self.connection.get_resource()

    def set_dac_custom_frequency(self, frequency_hz: float):
        """
        Set a custom DAC sample frequency.

        Args:
            frequency_hz (float): Frequency in Hz (e.g., 6e9 for 6 GHz)

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = f":FREQ:RAST {frequency_hz}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response="Custom frequency set")
                return {"Status": f"DAC frequency set to {frequency_hz} Hz", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_dac_frequency_min_max(self, mode: str):
        """
        Set the DAC sample frequency to its minimum or maximum limit.

        Args:
            mode (str): Either "MIN" or "MAX" (case-insensitive)

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if mode.upper() not in ["MIN", "MAX"]:
                return {"Error": "Invalid mode. Use 'MIN' or 'MAX'"}
            try:
                command = f":FREQ:RAST {mode.upper()}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=f"Frequency set to {mode.upper()}")
                return {"Status": f"DAC frequency set to {mode.upper()}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_dac_sample_frequency(self):
        """
        Query the current DAC sample frequency.
    
        Returns:
            dict: {"DAC Sample Frequency (Hz)": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = ":FREQ:RAST?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {"DAC Sample Frequency (Hz)": response, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}

