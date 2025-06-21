#import awg modules
from AWGConnection import AWG_connection
from logger import awg_logger

#import other modules
import time

class AWG_carrier:
    def __init__(self, ip_address):
        self.ip_address = ip_address

        #create insatces for connection and logger classes
        self.connection = AWG_connection(ip_address)
        self.log = awg_logger()

        #select the recourse from connection class
        self.resource = self.connection.get_resource()

    def set_carrier_frequency(self, channel: int, frequency_hz: float):
        """
        Set the carrier frequency for a given channel.

        Args:
            channel (int): Channel number (1-4)
            frequency_hz (float): Carrier frequency in Hz

        Returns:
            dict: SCPI response with set frequency
        """
        if self.resource:
            try:
                command = f":CARR{channel}:FREQ {frequency_hz}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                response = self.get_carrier_frequency(channel)
                self.log._log_command(command, duration_ms=duration, response=str(response))
                return {"Carrier Frequency (Hz)": response.get("Carrier Frequency (Hz)"), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_carrier_frequency_mode(self, channel: int, mode: str):
        """
        Set the carrier frequency to MIN, MAX, or DEF for a given channel.

        Args:
            channel (int): Channel number (1-4)
            mode (str): One of 'MIN', 'MAX', or 'DEF'

        Returns:
            dict: SCPI response with set frequency
        """
        if self.resource:
            try:
                mode = mode.upper()
                if mode not in ['MIN', 'MAX', 'DEF']:
                    return {"Error": "Mode must be one of 'MIN', 'MAX', or 'DEF'"}

                command = f":CARR{channel}:FREQ {mode}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                response = self.get_carrier_frequency(channel)
                self.log._log_command(command, duration_ms=duration, response=str(response))
                return {"Carrier Frequency (Hz)": response.get("Carrier Frequency (Hz)"), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_carrier_frequency(self, channel: int):
        """
        Query the carrier frequency for a given channel.

        Args:
            channel (int): Channel number (1-4)

        Returns:
            dict: {"Carrier Frequency (Hz)": value, "Duration(ms)": duration} or {"Error": ...}
        """
        if self.resource:
            try:
                command = f":CARR{channel}:FREQ?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000

                freq = float(response.strip())
                self.log._log_command(command, duration_ms=duration, response=response.strip())
                return {"Carrier Frequency (Hz)": freq, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_carrier_scale(self, channel: int, scale: float):
        """
        Set a custom amplitude scale for the carrier on a given channel.

        Args:
            channel (int): Channel number (1-4)
            scale (float): Amplitude scale value

        Returns:
            dict: SCPI response with updated scale
        """
        if self.resource:
            try:
                command = f":CARR{channel}:SCAL {scale}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                response = self.get_carrier_scale(channel)
                self.log._log_command(command, duration_ms=duration, response=str(response))
                return {"Carrier Scale": response.get("Carrier Scale"), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, 0, str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_carrier_scale_mode(self, channel: int, mode: str):
        """
        Set carrier scale to a preset mode: MIN, MAX, or DEF.

        Args:
            channel (int): Channel number (1–4)
            mode (str): One of 'MIN', 'MAX', or 'DEF'

        Returns:
            dict: SCPI response with updated scale
        """
        if self.resource:
            try:
                mode = mode.upper()
                if mode not in ["MIN", "MAX", "DEF"]:
                    return {"Error": "Mode must be 'MIN', 'MAX', or 'DEF'"}

                command = f":CARR{channel}:SCAL {mode}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                response = self.get_carrier_scale(channel)
                self.log._log_command(command, duration_ms=duration, response=str(response))
                return {"Carrier Scale": response.get("Carrier Scale"), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, 0, str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_carrier_scale(self, channel: int):
        """
        Query the carrier amplitude scale for a given channel.

        Args:
            channel (int): Channel number (1–4)

        Returns:
            dict: {"Carrier Scale": value, "Duration(ms)": duration} or error message
        """
        if self.resource:
            try:
                command = f":CARR{channel}:SCAL?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000

                scale = float(response.strip())
                self.log._log_command(command, duration_ms=duration, response=response.strip())
                return {"Carrier Scale": scale, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, 0, str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}





