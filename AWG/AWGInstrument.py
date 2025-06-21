#import awg modules
from AWGConnection import AWG_connection
from logger import awg_logger

#import other modules
import time

class AWG_instrument:
    def __init__(self, ip_address):
        self.ip_address = ip_address

        #create insatces for connection and logger classes
        self.connection = AWG_connection(ip_address)
        self.log = awg_logger()

        #select the recourse from connection class
        self.resource = self.connection.get_resource()

    def get_slot_number(self):
        """
        Query the instrument's slot number in its AXIe frame.

        Returns:
            dict: {"Slot Number": int, "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = ":INST:SLOT?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000

                slot_number = int(response.strip())
                self.log._log_command(command, duration_ms=duration, response=response.strip())
                return {"Slot Number": slot_number, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def identify_instrument(self, duration_seconds: int = 10):
        """
        Identify the instrument by flashing the front panel's green "Access" LED.

        Args:
            duration_seconds (int): Duration to flash the LED (default is 10 seconds)

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = f":INST:IDEN {duration_seconds}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                self.log._log_command(command, duration_ms=duration, response=f"Flashing for {duration_seconds} seconds")
                return {"Status": f"Instrument identification triggered for {duration_seconds} seconds", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    

    def stop_identification(self):
        """
        Stop the flashing of the instrument's front panel green "Access" LED before the interval ends.

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = ":INST:IDEN:STOP"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                self.log._log_command(command, duration_ms=duration, response="Identification stopped")
                return {"Status": "Instrument identification stopped", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}

    def get_hardware_revision(self):
        """
        Query the hardware revision number of the instrument (e.g., Keysight M8195A).

        Returns:
            dict: {"Hardware Revision": revision_string, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                command = ":INST:HWR?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000

                revision = response.strip()
                self.log._log_command(command, duration_ms=duration, response=revision)
                return {"Hardware Revision": revision, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_dac_mode(self, mode: str):
        """
        Set the DAC operation mode of the instrument.

        Args:
            mode (str): One of ['SINGle', 'DUAL', 'FOUR', 'MARKer', 'DCDuplicate', 'DCMarker']

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        valid_modes = ['SINGle', 'DUAL', 'FOUR', 'MARKer', 'DCDuplicate', 'DCMarker']
        if mode not in valid_modes:
            return {"Error": f"Invalid DAC mode '{mode}'. Must be one of {valid_modes}"}

        if self.resource:
            try:
                command = f":INST:DACM {mode}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                response = self.get_dac_mode()
                self.log._log_command(command, duration_ms=duration, response=str(response))
                return {"Status": f"DAC mode set to {mode}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_dac_mode(self):
        """
        Query the current DAC operation mode of the instrument.

        Returns:
            dict: {"DAC Mode": mode, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                command = ":INST:DACM?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000

                mode = response.strip()
                self.log._log_command(command, duration_ms=duration, response=mode)
                return {"DAC Mode": mode, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_memory_sample_rate_divider(self, divider: str):
        """
        Set the sample rate divider for extended memory.

        Args:
            divider (str): One of ['DIV1', 'DIV2', 'DIV4']

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        valid_dividers = ['DIV1', 'DIV2', 'DIV4']
        if divider not in valid_dividers:
            return {"Error": f"Invalid divider '{divider}'. Must be one of {valid_dividers}"}

        if self.resource:
            try:
                command = f":INST:MEM:EXT:RDIV {divider}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                response = self.get_memory_sample_rate_divider()
                self.log._log_command(command, duration_ms=duration, response=str(response))
                return {"Status": f"Sample rate divider set to {divider}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_memory_sample_rate_divider(self):
        """
        Query the sample rate divider for extended memory.

        Returns:
            dict: {"Memory Sample Rate Divider": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = ":INST:MEM:EXT:RDIV?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000

                divider = response.strip()
                self.log._log_command(command, duration_ms=duration, response=divider)
                return {"Memory Sample Rate Divider": divider, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}

    def get_multi_module_config_state(self):
        """
        Query the state of the multi-module configuration mode.

        Returns:
            dict: {"Multi-Module Config": "Enabled"/"Disabled", "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = ":INST:MMOD:CONF?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000

                value = response.strip()
                state = "Enabled" if value == "1" else "Disabled"
                self.log._log_command(command, duration_ms=duration, response=state)
                return {"Multi-Module Config": state, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_multi_module_mode(self):
        """
        Query the multi-module mode of the instrument.
    
        Returns:
            dict: {"Multi-Module Mode": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = ":INST:MMOD:MODE?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000
    
                mode = response.strip()
                self.log._log_command(command, duration_ms=duration, response=mode)
                return {"Multi-Module Mode": mode, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}







