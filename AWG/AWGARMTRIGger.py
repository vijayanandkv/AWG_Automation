#import AWG modules
from AWGConnection import AWG_connection
from logger import awg_logger

#import other libraries
import time

class AWG_ARM_TRIGger_Controller:
    def __init__(self, ip_address):
        self.ip_address = ip_address

        #create insatces for connection and logger classes
        self.connection = AWG_connection(ip_address)
        self.log = awg_logger()

        #select the recourse from connection class
        self.resource = self.connection.get_resource()

    def set_abort(self):
        """
        Stop signal generation on all channels. The channel suffix is ignored.
        Returns:
            dict: {"Status": "Aborted", "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                command = ":ABOR"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response="Aborted)")
                return {"Status": "Aborted", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_custom_module_delay(self, delay_value: str):
        """
        Set the module delay setting.
        Args:
            delay_value (str): Delay value (e.g., '10ns', '5ms', '1e-6', 'MINimum', 'MAXimum')
        Returns:
            dict: {"Status": f"Module delay set to {delay_value}", "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                command = f":ARM:MDEL {delay_value}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=str(self.get_module_delay()))
                return {"Status": f"Module delay set to {delay_value}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_minimum_module_delay(self):
        """
        Set the module delay setting.
        Args:
            delay_value (str): Delay value (e.g., '10ns', '5ms', '1e-6', 'MINimum', 'MAXimum')
        Returns:
            dict: {"Status": f"Module delay set to {delay_value}", "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                command = f":ARM:MDEL MIN"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response= str(self.get_module_delay()))
                return {"Status": f"Module delay set to minimum", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_maximum_module_delay(self):
        """
        Set the module delay setting.
        Args:
            delay_value (str): Delay value (e.g., '10ns', '5ms', '1e-6', 'MINimum', 'MAXimum')
        Returns:
            dict: {"Status": f"Module delay set to {delay_value}", "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                command = f":ARM:MDEL MAX"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response= str(self.get_module_delay()))
                return {"Status": f"Module delay set to maximum", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_module_delay(self):
        """
        Query the current module delay setting.
        Returns:
            dict: {"Delay(s)": float_value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                command = ":ARM:MDEL?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response.strip())
                return {"Delay(s)": float(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_custom_sample_delay(self, channel: int, delay_value: str):
        """
        Set a custom sample delay for a specific channel (1 to 4).
        Args:
            channel (int): Channel number (1-4)
            delay_value (str): Delay value (e.g., '10', '25', '0')
        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be 1, 2, 3, or 4."}
            try:
                command = f":ARM:SDEL{channel} {delay_value}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                delay_query = self.get_sample_delay(channel)
                self.log._log_command(command, duration_ms=duration, response=str(delay_query))
                return {
                    "Status": f"Sample delay for channel {channel} set to {delay_value}",
                    "Duration(ms)": duration
                }
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
        
    def set_minimum_sample_delay(self, channel: int):
        """
        Set the sample delay to the minimum allowed value for a specific channel.
        Args:
            channel (int): Channel number (1–4)
        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be 1, 2, 3, or 4."}
            try:
                command = f":ARM:SDEL{channel} MIN"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                delay_query = self.get_sample_delay(channel)
                self.log._log_command(command, duration_ms=duration, response=str(delay_query))
                return {
                    "Status": f"Sample delay for channel {channel} set to MINimum",
                    "Duration(ms)": duration
                }
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_maximum_sample_delay(self, channel: int):
        """
        Set the sample delay to the maximum allowed value for a specific channel.
        Args:
            channel (int): Channel number (1–4)
        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be 1, 2, 3, or 4."}
            try:
                command = f":ARM:SDEL{channel} MAX"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                delay_query = self.get_sample_delay(channel)
                self.log._log_command(command, duration_ms=duration, response=str(delay_query))
                return {
                    "Status": f"Sample delay for channel {channel} set to MAXimum",
                    "Duration(ms)": duration
                }
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
        
    def set_arming_mode(self, mode: str):
        """
        
        Set the arming mode to SELF or ARMed.
        Args:
            mode (str): "SELF" or "ARMed"
        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if mode.upper() not in ["SELF", "ARMED"]:
                raise ValueError
            try:
                command = f":INIT:CONT:ENAB {mode.upper()}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                mode_query = self.get_arming_mode()
                self.log._log_command(command, duration_ms=duration, response=str(mode_query))
                return {"Status": f"Arming mode set to {mode.upper()}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
        
    def get_arming_mode(self):
        """
        Query the current arming mode setting.
        Returns:
            dict: {"Arming Mode": mode_str, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                command = ":INIT:CONT:ENAB?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response.strip())
                return {"Arming Mode": response.strip(), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
        
    def set_continuous_mode(self, state: str):
        """
        Set the continuous mode to ON (1) or OFF (0).
        Args:
            state (str): 'ON', 'OFF', '1', or '0'
        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            valid_states = {"ON": "ON", "1": "ON", "OFF": "OFF", "0": "OFF"}
            state_upper = state.upper()
            if state_upper not in valid_states:
                return {"Error": "Invalid state. Use 'ON', 'OFF', '1', or '0'."}
            try:
                command = f":INIT:CONT:STAT {valid_states[state_upper]}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                cont_mode = self.get_continuous_mode()
                self.log._log_command(command, duration_ms=duration, response=str(cont_mode))
                return {"Status": f"Continuous mode set to {valid_states[state_upper]}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
        
    def get_continuous_mode(self):
        """
        Query the current continuous mode setting.
        Returns:
            dict: {"Continuous Mode": 'ON' or 'OFF', "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                command = ":INIT:CONT:STAT?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000
                mode_str = "ON" if response.strip() in ["1", "ON"] else "OFF"
                self.log._log_command(command, duration_ms=duration, response=response.strip())
                return {"Continuous Mode": mode_str, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
        
    def set_gate_mode(self, state: str):
        """
        Set the gate mode to ON (1) or OFF (0).
        Args:
            state (str): 'ON', 'OFF', '1', or '0'
        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            valid_states = {"ON": "ON", "1": "ON", "OFF": "OFF", "0": "OFF"}
            state_upper = state.upper()
            if state_upper not in valid_states:
                return {"Error": "Invalid state. Use 'ON', 'OFF', '1', or '0'."}
            try:
                command = f":INIT:GATE:STAT {valid_states[state_upper]}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                gate_mode = self.get_gate_mode()
                self.log._log_command(command, duration_ms=duration, response=str(gate_mode))
                return {"Status": f"Gate mode set to {valid_states[state_upper]}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
        
    def get_gate_mode(self):
        """
        Query the current gate mode setting.
    
        Returns:
            dict: {"Gate Mode": 'ON' or 'OFF', "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                command = ":INIT:GATE:STAT?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000
    
                mode_str = "ON" if response.strip() in ["1", "ON"] else "OFF"
                self.log._log_command(command, duration_ms=duration, response=response.strip())
                return {"Gate Mode": mode_str, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def start_signal_generation(self):
        """
        Start signal generation immediately on all channels.

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = ":INIT:IMM"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                self.log._log_command(command, duration_ms=duration, response="signal generation started on all channels)")
                return {"Status": "Signal generation started", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_custom_trigger_level(self, level_value: str):
        """
        Set a custom trigger input threshold voltage level.

        Args:
            level_value (str): Threshold voltage level (e.g., '0.5', '3e-9')

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = f":ARM:TRIG:LEV {level_value}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                level_query = self.get_trigger_level()
                self.log._log_command(command, duration_ms=duration, response=str(level_query))
                return {
                    "Status": f"Trigger level set to {level_value}",
                    "Duration(ms)": duration
                }
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_minimum_trigger_level(self):
        """
        Set the trigger input threshold level to the minimum allowed value.

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = ":ARM:TRIG:LEV MIN"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                level_query = self.get_trigger_level()
                self.log._log_command(command, duration_ms=duration, response=str(level_query))
                return {"Status": "Trigger level set to MINimum", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_maximum_trigger_level(self):
        """
        Set the trigger input threshold level to the maximum allowed value.

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = ":ARM:TRIG:LEV MAX"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                level_query = self.get_trigger_level()
                self.log._log_command(command, duration_ms=duration, response=str(level_query))
                return {"Status": "Trigger level set to MAXimum", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_trigger_level(self):
        """
        Query the current trigger input threshold voltage level.

        Returns:
            dict: {"Trigger Level (V)": float_value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                command = ":ARM:TRIG:LEV?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000

                self.log._log_command(command, duration_ms=duration, response=response.strip())
                return {"Trigger Level (V)": float(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_trigger_slope(self, slope: str):
        """
        Set the trigger input slope.

        Args:
            slope (str): 'POSitive', 'NEGative', or 'EITHer' (case-insensitive)

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            valid_slopes = ["POSITIVE", "NEGATIVE", "EITHER"]
            slope_upper = slope.upper()
            if slope_upper not in valid_slopes:
                return {"Error": "Invalid slope. Use 'POSitive', 'NEGative', or 'EITHer'."}
            try:
                command = f":ARM:TRIG:SLOP {slope_upper}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                slope_query = self.get_trigger_slope()
                self.log._log_command(command, duration_ms=duration, response=str(slope_query))
                return {"Status": f"Trigger slope set to {slope_upper}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_trigger_slope(self):
        """
        Query the current trigger input slope.
    
        Returns:
            dict: {"Trigger Slope": slope, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                command = ":ARM:TRIG:SLOP?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000
    
                slope = response.strip().upper()
                self.log._log_command(command, duration_ms=duration, response=slope)
                return {"Trigger Slope": slope, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_trigger_source(self, source: str):
        """
        Set the trigger source.

        Args:
            source (str): 'TRIGger', 'EVENt', or 'INTernal' (case-insensitive)

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            valid_sources = ["TRIG", "EVEN", "INT"]
            source_upper = source.upper()
            if source_upper not in valid_sources:
                return {"Error": "Invalid source. Use 'TRIGger', 'EVENt', or 'INTernal'."}
            try:
                command = f":ARM:TRIG:SOUR {source_upper}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                source_query = self.get_trigger_source()
                self.log._log_command(command, duration_ms=duration, response=str(source_query))
                return {"Status": f"Trigger source set to {source_upper}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_trigger_source(self):
        """
        Query the current trigger source.

        Returns:
            dict: {"Trigger Source": source, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                command = ":ARM:TRIG:SOUR?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000

                source = response.strip().upper()
                self.log._log_command(command, duration_ms=duration, response=source)
                return {"Trigger Source": source, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_custom_trigger_frequency(self, frequency: str):
        """
        Set a custom frequency for the internal trigger generator.

        Args:
            frequency (str): Frequency value as a string (e.g., '1', '10.5', '1e3')

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = f":ARM:TRIG:FREQ {frequency}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                freq_query = self.get_trigger_frequency()
                self.log._log_command(command, duration_ms=duration, response=str(freq_query))
                return {"Status": f"Trigger frequency set to {frequency} Hz", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_minimum_trigger_frequency(self):
        """
        Set the trigger frequency to the minimum allowed value.

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = ":ARM:TRIG:FREQ MIN"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                freq_query = self.get_trigger_frequency()
                self.log._log_command(command, duration_ms=duration, response=str(freq_query))
                return {"Status": "Trigger frequency set to MINimum", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_maximum_trigger_frequency(self):
        """
        Set the trigger frequency to the maximum allowed value.

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = ":ARM:TRIG:FREQ MAX"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                freq_query = self.get_trigger_frequency()
                self.log._log_command(command, duration_ms=duration, response=str(freq_query))
                return {"Status": "Trigger frequency set to MAXimum", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_trigger_frequency(self):
        """
        Query the current internal trigger generator frequency.

        Returns:
            dict: {"Trigger Frequency (Hz)": float_value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                command = ":ARM:TRIG:FREQ?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000

                self.log._log_command(command, duration_ms=duration, response=response.strip())
                return {"Trigger Frequency (Hz)": float(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_trigger_operation_mode(self, mode: str):
        """
        Set the trigger operation mode.

        Args:
            mode (str): 'ASYNchronous' or 'SYNChronous' (case-insensitive)

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            valid_modes = ["ASYN", "SYN"]
            mode_upper = mode.upper()
            if mode_upper not in valid_modes:
                return {"Error": "Invalid mode. Use 'ASYNchronous' or 'SYNChronous'."}
            try:
                command = f":ARM:TRIG:OPER {mode_upper}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                mode_query = self.get_trigger_operation_mode()
                self.log._log_command(command, duration_ms=duration, response=str(mode_query))
                return {"Status": f"Trigger operation mode set to {mode_upper}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_trigger_operation_mode(self):
        """
        Query the current trigger operation mode.

        Returns:
            dict: {"Trigger Operation Mode": mode, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                command = ":ARM:TRIG:OPER?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000

                mode = response.strip().upper()
                self.log._log_command(command, duration_ms=duration, response=mode)
                return {"Trigger Operation Mode": mode, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_custom_event_level(self, level_value: str):
        """
        Set a custom input threshold voltage level for the event input.

        Args:
            level_value (str): Voltage level (e.g., '0.5', '2e-9')

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = f":ARM:EVEN:LEV {level_value}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                response = self.get_event_level()
                self.log._log_command(command, duration_ms=duration, response=str(response))
                return {"Status": f"Event input level set to {level_value}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_minimum_event_level(self):
        """
        Set the event input threshold level to the minimum supported value.

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = ":ARM:EVEN:LEV MIN"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                response = self.get_event_level()
                self.log._log_command(command, duration_ms=duration, response=str(response))
                return {"Status": "Event input level set to MINimum", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_maximum_event_level(self):
        """
        Set the event input threshold level to the maximum supported value.

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = ":ARM:EVEN:LEV MAX"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                response = self.get_event_level()
                self.log._log_command(command, duration_ms=duration, response=str(response))
                return {"Status": "Event input level set to MAXimum", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_event_level(self):
        """
        Query the current event input threshold voltage level.

        Returns:
            dict: {"Event Level (V)": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                command = ":ARM:EVEN:LEV?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000

                level = float(response.strip())
                self.log._log_command(command, duration_ms=duration, response=response.strip())
                return {"Event Level (V)": level, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_event_slope(self, slope: str):
        """
        Set the slope for the event input.

        Args:
            slope (str): 'POSitive', 'NEGative', or 'EITHer' (case-insensitive)

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            valid_slopes = ["POS", "NEG", "EITH"]
            slope_upper = slope.upper()
            if slope_upper not in valid_slopes:
                return {"Error": "Invalid slope. Use 'POSitive', 'NEGative', or 'EITHer'."}
            try:
                command = f":ARM:EVEN:SLOP {slope_upper}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                response = self.get_event_slope()
                self.log._log_command(command, duration_ms=duration, response=str(response))
                return {"Status": f"Event input slope set to {slope_upper}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_event_slope(self):
        """
        Query the current slope for the event input.

        Returns:
            dict: {"Event Slope": slope, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                command = ":ARM:EVEN:SLOP?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000

                slope = response.strip().upper()
                self.log._log_command(command, duration_ms=duration, response=slope)
                return {"Event Slope": slope, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_trigger_enable_source(self, source: str):
        """
        Set the source for the enable event.

        Args:
            source (str): 'TRIGger' or 'EVENt' (case-insensitive)

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            valid_sources = ["TRIG", "EVEN"]
            source_upper = source.upper()
            if source_upper not in valid_sources:
                return {"Error": "Invalid source. Use 'TRIGger' or 'EVENt'."}
            try:
                command = f":TRIG:SOUR:ENAB {source_upper}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                response = self.get_trigger_enable_source()
                self.log._log_command(command, duration_ms=duration, response=str(response))
                return {"Status": f"Enable source set to {source_upper}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_trigger_enable_source(self):
        """
        Query the current source for the enable event.

        Returns:
            dict: {"Enable Source": source, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                command = ":TRIG:SOUR:ENAB?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000

                source = response.strip().upper()
                self.log._log_command(command, duration_ms=duration, response=source)
                return {"Enable Source": source, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_enable_hw_disable_state(self, state: str):
        """
        Set the hardware disable state for the enable function.

        Args:
            state (str): 'ON', 'OFF', '1', or '0' (case-insensitive)

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            valid_states = ["ON", "OFF", "1", "0"]
            state_upper = state.upper()
            if state_upper not in valid_states:
                return {"Error": "Invalid state. Use 'ON', 'OFF', '1', or '0'."}
            try:
                command = f":TRIG:ENAB:HWD {state_upper}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                response = self.get_enable_hw_disable_state()
                self.log._log_command(command, duration_ms=duration, response=str(response))
                return {"Status": f"HW Disable set to {state_upper}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_enable_hw_disable_state(self):
        """
        Query the hardware disable state for the enable function.

        Returns:
            dict: {"HW Disable State": state, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                command = ":TRIG:ENAB:HWD?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000

                state = response.strip().upper()
                self.log._log_command(command, duration_ms=duration, response=state)
                return {"HW Disable State": state, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_trigger_hw_disable_state(self, state: str):
        """
        Set the hardware disable state for the trigger function.

        Args:
            state (str): 'ON', 'OFF', '1', or '0' (case-insensitive)

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            valid_states = ["ON", "OFF", "1", "0"]
            state_upper = state.upper()
            if state_upper not in valid_states:
                return {"Error": "Invalid state. Use 'ON', 'OFF', '1', or '0'."}
            try:
                command = f":TRIG:BEG:HWD {state_upper}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                response = self.get_trigger_hw_disable_state()
                self.log._log_command(command, duration_ms=duration, response=str(response))
                return {"Status": f"Trigger HW disable state set to {state_upper}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_trigger_hw_disable_state(self):
        """
        Query the current hardware disable state for the trigger function.

        Returns:
            dict: {"Trigger HW Disable State": state, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                command = ":TRIG:BEG:HWD?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000

                state = response.strip().upper()
                self.log._log_command(command, duration_ms=duration, response=state)
                return {"Trigger HW Disable State": state, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_advance_hw_disable_state(self, state: str):
        """
        Set the hardware disable state for the advancement function.

        Args:
            state (str): 'ON', 'OFF', '1', or '0' (case-insensitive)

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            valid_states = ["ON", "OFF", "1", "0"]
            state_upper = state.upper()
            if state_upper not in valid_states:
                return {"Error": "Invalid state. Use 'ON', 'OFF', '1', or '0'."}
            try:
                command = f":TRIG:ADV:HWD {state_upper}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                response = self.get_advance_hw_disable_state()
                self.log._log_command(command, duration_ms=duration, response=str(response))
                return {"Status": f"Advance HW disable state set to {state_upper}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_advance_hw_disable_state(self):
        """
        Query the current hardware disable state for the advancement function.
    
        Returns:
            dict: {"Advance HW Disable State": state, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                command = ":TRIG:ADV:HWD?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000
    
                state = response.strip().upper()
                self.log._log_command(command, duration_ms=duration, response=state)
                return {"Advance HW Disable State": state, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}









    


































