#import awg modules
from AWGConnection import AWG_connection
from logger import awg_logger

#import other modules
import time

class AWG_Voltage_Subsystem:
    def __init__(self, ip_address):
        self.ip_address = ip_address

        #create insatces for connection and logger classes
        self.connection = AWG_connection(ip_address)
        self.log = awg_logger()

        #select the recourse from connection class
        self.resource = self.connection.get_resource()

    def set_output_voltage(self, channel: int, amplitude: float):
        """
        Set the output voltage amplitude for a specified channel.

        Args:
            channel (int): Output channel number (1–4)
            amplitude (float): Voltage amplitude in volts

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if channel not in [1, 2, 3, 4]:
            return {"Error": "Invalid channel. Must be 1, 2, 3, or 4"}

        if self.resource:
            try:
                command = f":VOLT{channel} {amplitude}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response="Voltage set")
                return {"Status": f"Set channel {channel} voltage to {amplitude} V", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_output_voltage_min_max(self, channel: int, setting: str):
        """
        Set the MINimum or MAXimum voltage amplitude for a channel.

        Args:
            channel (int): Output channel number (1–4)
            setting (str): 'MIN' or 'MAX'

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        setting = setting.upper()
        if channel not in [1, 2, 3, 4] or setting not in ["MIN", "MAX"]:
            return {"Error": "Invalid input. Channel must be 1–4, setting must be 'MIN' or 'MAX'"}

        if self.resource:
            try:
                command = f":VOLT{channel} {setting}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=f"{setting} voltage set")
                return {"Status": f"{setting} voltage set on channel {channel}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_output_voltage(self, channel: int):
        """
        Query the output voltage amplitude for a specified channel.

        Args:
            channel (int): Output channel number (1–4)

        Returns:
            dict: {"Amplitude (V)": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if channel not in [1, 2, 3, 4]:
            return {"Error": "Invalid channel. Must be 1, 2, 3, or 4"}

        if self.resource:
            try:
                command = f":VOLT{channel}?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {"Amplitude (V)": float(response), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_output_offset(self, channel: int, offset_value: float):
        """
        Set a custom voltage offset for the output channel.

        Args:
            channel (int): Channel number (1–4)
            offset_value (float): Offset voltage (e.g., 0.02)

        Returns:
            dict: Status or Error with execution time
        """
        if self.resource:
            try:
                command = f":VOLT{channel}:OFFS {offset_value}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                response = self.get_output_offset(channel)
                self.log._log_command(command, duration_ms=duration, response=str(response))
                return {"Status": f"Offset set to {offset_value} V on channel {channel}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_output_offset_min_max(self, channel: int, mode: str):
        """
        Set the voltage offset to the MINimum or MAXimum supported value for a channel.

        Args:
            channel (int): Channel number (1–4)
            mode (str): Either "MIN" or "MAX" (case-insensitive)

        Returns:
            dict: Status or Error with execution time
        """
        mode = mode.strip().upper()
        if mode not in ["MIN", "MAX"]:
            return {"Error": "Invalid mode. Use 'MIN' or 'MAX'."}

        if self.resource:
            try:
                command = f":VOLT{channel}:OFFS {mode}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                response = self.get_output_offset(channel)
                self.log._log_command(command, duration_ms=duration, response=str(response))
                return {
                    "Status": f"Offset set to {mode} for channel {channel}",
                    "Duration(ms)": duration
                }
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}

        return {"Error": "Device not connected"}

    
    def get_output_offset(self, channel: int):
        """
        Query the current output voltage offset for a channel.

        Args:
            channel (int): Channel number (1–4)

        Returns:
            dict: Offset voltage and duration, or error message
        """
        if self.resource:
            try:
                command = f":VOLT{channel}:OFFS?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000
                offset = float(response.strip())
                self.log._log_command(command, duration_ms=duration, response=response.strip())
                return {"Offset (V)": offset, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_output_high_level(self, channel: int, level: float):
        """
        Set a custom high-level output voltage for a specific channel.

        Args:
            channel (int): Channel number (1–4)
            level (float): Desired high voltage level (e.g., 0.3)

        Returns:
            dict: Actual value from the query and execution duration.
        """
        if self.resource:
            try:
                command = f":VOLT{channel}:HIGH {level}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                response = self.get_output_high_level(channel)
                self.log._log_command(command, duration_ms=duration, response=str(response))
                return {**response, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_output_high_level_min_max(self, channel: int, mode: str):
        """
        Set the high-level voltage to MIN or MAX for the specified channel.

        Args:
            channel (int): Channel number (1–4)
            mode (str): "MIN" or "MAX"

        Returns:
            dict: Actual value from the query and execution duration.
        """
        mode = mode.strip().upper()
        if mode not in ["MIN", "MAX"]:
            return {"Error": "Invalid mode. Use 'MIN' or 'MAX'."}

        if self.resource:
            try:
                command = f":VOLT{channel}:HIGH {mode}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                response = self.get_output_high_level(channel)
                self.log._log_command(command, duration_ms=duration, response=str(response))
                return {**response, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    

    def get_output_high_level(self, channel: int):
        """
        Query the current high-level output voltage for a specific channel.

        Args:
            channel (int): Channel number (1–4)

        Returns:
            dict: High level voltage value or error
        """
        if self.resource:
            try:
                command = f":VOLT{channel}:HIGH?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000
                value = float(response.strip())
                self.log._log_command(command, duration_ms=duration, response=response.strip())
                return {"High Level (V)": value}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_output_low_level(self, channel: int, level: float):
        """
        Set a custom low-level output voltage for a specific channel.

        Args:
            channel (int): Channel number (1–4)
            level (float): Desired low voltage level (e.g., -0.3)

        Returns:
            dict: Actual queried value and execution duration.
        """
        if self.resource:
            try:
                command = f":VOLT{channel}:LOW {level}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                response = self.get_output_low_level(channel)
                self.log._log_command(command, duration_ms=duration, response=str(response))
                return {**response, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_output_low_level_min_max(self, channel: int, mode: str):
        """
        Set the low-level voltage to MIN or MAX for the specified channel.

        Args:
            channel (int): Channel number (1–4)
            mode (str): "MIN" or "MAX"

        Returns:
            dict: Actual queried value and execution duration.
        """
        mode = mode.strip().upper()
        if mode not in ["MIN", "MAX"]:
            return {"Error": "Invalid mode. Use 'MIN' or 'MAX'."}

        if self.resource:
            try:
                command = f":VOLT{channel}:LOW {mode}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                response = self.get_output_low_level(channel)
                self.log._log_command(command, duration_ms=duration, response=str(response))
                return {**response, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_output_low_level(self, channel: int):
        """
        Query the current low-level output voltage for a specific channel.

        Args:
            channel (int): Channel number (1–4)

        Returns:
            dict: Low level voltage value or error
        """
        if self.resource:
            try:
                command = f":VOLT{channel}:LOW?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000
                value = float(response.strip())
                self.log._log_command(command, duration_ms=duration, response=response.strip())
                return {"Low Level (V)": value}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_output_termination_voltage(self, channel: int, level: float):
        """
        Set a custom termination voltage level for the specified channel.

        Args:
            channel (int): Output channel (1–4)
            level (float): Desired termination voltage (e.g., 0.3)

        Returns:
            dict: Actual queried value and execution duration.
        """
        if self.resource:
            try:
                command = f":VOLT{channel}:TERM {level}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                response = self.get_output_termination_voltage(channel)
                self.log._log_command(command, duration_ms=duration, response=str(response))
                return {**response, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_output_termination_voltage_min_max(self, channel: int, mode: str):
        """
        Set termination voltage to MIN or MAX for the specified channel.

        Args:
            channel (int): Output channel (1–4)
            mode (str): "MIN" or "MAX"

        Returns:
            dict: Actual queried value and execution duration.
        """
        mode = mode.strip().upper()
        if mode not in ["MIN", "MAX"]:
            return {"Error": "Invalid mode. Use 'MIN' or 'MAX'."}

        if self.resource:
            try:
                command = f":VOLT{channel}:TERM {mode}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                response = self.get_output_termination_voltage(channel)
                self.log._log_command(command, duration_ms=duration, response=str(response))
                return {**response, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    

    def get_output_termination_voltage(self, channel: int):
        """
        Query the current termination voltage for the specified channel.
    
        Args:
            channel (int): Output channel (1–4)
    
        Returns:
            dict: Termination voltage or error message.
        """
        if self.resource:
            try:
                command = f":VOLT{channel}:TERM?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000
                value = float(response.strip())
    
                self.log._log_command(command, duration_ms=duration, response=response.strip())
                return {"Termination Voltage (V)": value}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}













