#import awg modules
from AWGConnection import AWG_connection
from logger import awg_logger

#import other modules
import time

class AWG_Reference_Oscillator:
    def __init__(self, ip_address):
        self.ip_address = ip_address

        #create insatces for connection and logger classes
        self.connection = AWG_connection(ip_address)
        self.log = awg_logger()

        #select the recourse from connection class
        self.resource = self.connection.get_resource()

    def set_reference_clock_source(self, source: str):
        """
        Set the reference clock source.

        Args:
            source (str): One of 'EXT', 'AXI', or 'INT' (case-insensitive for EXTernal, AXI, INTernal)

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        valid_sources = {"EXT": "EXTernal", "AXI": "AXI", "INT": "INTernal"}
        source_upper = source.upper()

        if self.resource:
            if source_upper not in valid_sources:
                return {"Error": "Invalid source. Use 'EXT', 'AXI', or 'INT'"}
            try:
                command = f":ROSC:SOUR {valid_sources[source_upper]}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response="Reference clock source set")
                return {"Status": f"Reference clock source set to {valid_sources[source_upper]}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_reference_clock_source(self):
        """
        Query the current reference clock source.

        Returns:
            dict: {"Reference Clock Source": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = ":ROSC:SOUR?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {"Reference Clock Source": response, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def check_reference_clock_source_availability(self, source: str):
        """
        Check if a specific reference clock source is available.

        Args:
            source (str): One of 'EXT', 'AXI', or 'INT' (case-insensitive for EXTernal, AXI, INTernal)

        Returns:
            dict: {"Available": True/False, "Duration(ms)": ...} or {"Error": ...}
        """
        valid_sources = {"EXT": "EXTernal", "AXI": "AXI", "INT": "INTernal"}
        source_upper = source.upper()

        if self.resource:
            if source_upper not in valid_sources:
                return {"Error": "Invalid source. Use 'EXT', 'AXI', or 'INT'"}
            try:
                command = f":ROSC:SOUR:CHEC? {valid_sources[source_upper]}"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000

                available = response == "1"
                self.log._log_command(command, duration_ms=duration, response=response)
                return {"Available": available, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_reference_clock_frequency(self, frequency_hz: float):
        """
        Set a custom expected reference clock frequency for the external clock source.

        Args:
            frequency_hz (float): Frequency in Hz (e.g., 1e8 for 100 MHz)

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = f":ROSC:FREQ {frequency_hz}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response="Reference clock frequency set")
                return {"Status": f"Reference clock frequency set to {frequency_hz} Hz", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_reference_clock_frequency_min_max(self, mode: str):
        """
        Set the reference clock frequency to its minimum or maximum allowable value.

        Args:
            mode (str): 'MIN' or 'MAX' (case-insensitive)

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            mode_upper = mode.upper()
            if mode_upper not in ["MIN", "MAX"]:
                return {"Error": "Invalid mode. Use 'MIN' or 'MAX'"}
            try:
                command = f":ROSC:FREQ {mode_upper}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=f"Reference frequency set to {mode_upper}")
                return {"Status": f"Reference frequency set to {mode_upper}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_reference_clock_frequency(self):
        """
        Query the currently set reference clock frequency.

        Returns:
            dict: {"Reference Clock Frequency (Hz)": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = ":ROSC:FREQ?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {"Reference Clock Frequency (Hz)": response, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_reference_clock_range_by_frequency(self, frequency_hz: float):
        """
        Automatically set the appropriate reference clock range based on the given frequency.

        Args:
            frequency_hz (float): Expected external reference frequency in Hz (e.g., 1e8 for 100 MHz)

        Returns:
            dict: {"Selected Range": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                # Determine correct range
                if 10e6 <= frequency_hz <= 300e6:
                    range_mode = "RANG1"
                elif 210e6 <= frequency_hz <= 17e9:
                    range_mode = "RANG2"
                else:
                    return {"Error": "Frequency out of valid range (10 MHz – 17 GHz)"}

                command = f":ROSC:RANG {range_mode}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=f"Auto-selected range {range_mode}")
                return {"Selected Range": range_mode, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_reference_clock_range(self):
        """
        Query the current reference clock frequency range.

        Returns:
            dict: {"Reference Clock Range": 'RANG1' or 'RANG2', "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = ":ROSC:RANG?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {"Reference Clock Range": response, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_reference_frequency_for_range(self, range_id: str, frequency_hz: float):
        """
        Set the reference frequency for a given range (RNG1 or RNG2) without switching range.

        Args:
            range_id (str): 'RNG1' or 'RNG2'
            frequency_hz (float): Frequency value in Hz

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        range_id = range_id.upper()
        if range_id not in ["RNG1", "RNG2"]:
            return {"Error": "Invalid range. Use 'RNG1' or 'RNG2'"}

        if self.resource:
            try:
                command = f":ROSC:{range_id}:FREQ {frequency_hz}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response="Frequency set")
                return {"Status": f"Reference frequency set to {frequency_hz} Hz for {range_id}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_reference_frequency_min_max(self, range_id: str, setting: str):
        """
        Set the MINimum or MAXimum reference frequency for a given range.

        Args:
            range_id (str): 'RNG1' or 'RNG2'
            setting (str): 'MIN' or 'MAX'

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        range_id = range_id.upper()
        setting = setting.upper()
        if range_id not in ["RNG1", "RNG2"] or setting not in ["MIN", "MAX"]:
            return {"Error": "Invalid input. Use RNG1 or RNG2, and MIN or MAX."}

        if self.resource:
            try:
                command = f":ROSC:{range_id}:FREQ {setting}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=f"{setting} frequency set")
                return {"Status": f"{setting} frequency set for {range_id}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_reference_frequency_for_range(self, range_id: str):
        """
        Query the current reference frequency setting for a given range (RNG1 or RNG2).
    
        Args:
            range_id (str): 'RNG1' or 'RNG2'
    
        Returns:
            dict: {"Frequency (Hz)": value, "Duration(ms)": ...} or {"Error": ...}
        """
        range_id = range_id.upper()
        if range_id not in ["RNG1", "RNG2"]:
            return {"Error": "Invalid range. Use 'RNG1' or 'RNG2'"}
    
        if self.resource:
            try:
                command = f":ROSC:{range_id}:FREQ?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {"Frequency (Hz)": float(response), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    








