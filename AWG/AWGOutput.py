#import awg modules
from AWGConnection import AWG_connection
from logger import awg_logger

#import other modules
import time

class AWG_output:
    def __init__(self, ip_address):
        self.ip_address = ip_address

        #create insatces for connection and logger classes
        self.connection = AWG_connection(ip_address)
        self.log = awg_logger()

        #select the recourse from connection class
        self.resource = self.connection.get_resource()

    def set_output_state(self, channel: int, state: bool):
        """
        Turn ON or OFF the output of a specific AWG channel.

        Args:
            channel (int): Channel number (1 to 4)
            state (bool): True for ON, False for OFF

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be 1, 2, 3, or 4."}

            try:
                command = f":OUTP{channel} {'ON' if state else 'OFF'}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                self.log._log_command(command, duration_ms=duration, response=f"Output {'enabled' if state else 'disabled'}")
                return {
                    "Status": f"Channel {channel} output turned {'ON' if state else 'OFF'}",
                    "Duration(ms)": duration
                }
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}

        return {"Error": "Device not connected"}
    
    def get_output_state(self, channel: int):
        """
        Query the output state of a specific AWG channel.

        Args:
            channel (int): Channel number (1 to 4)

        Returns:
            dict: {"Output State": True/False, "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be 1, 2, 3, or 4."}
            try:
                command = f":OUTP{channel}?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000

                state = response.strip() in ["1", "ON"]
                self.log._log_command(command, duration_ms=duration, response=response.strip())
                return {"Output State": state, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_reference_clock_source(self, source: str):
        """
        Set the source for the reference clock output.

        Args:
            source (str): One of "INTernal", "EXTernal", "SCLK1", or "SCLK2"

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        valid_sources = ["INTernal", "EXTernal", "SCLK1", "SCLK2"]
        if self.resource:
            if source not in valid_sources:
                return {"Error": f"Invalid source. Must be one of {valid_sources}"}
            try:
                command = f":OUTP:ROSC:SOUR {source}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=f"Source set to {source}")
                return {"Status": f"Reference clock source set to {source}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_reference_clock_source(self):
        """
        Query the current reference clock output source.

        Returns:
            dict: {"Reference Clock Source": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = ":OUTP:ROSC:SOUR?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {"Reference Clock Source": response, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_sample_clock_divider(self, divider):
        """
        Set the DAC sample clock divider for the reference clock output.

        Args:
            divider (int or str): A valid divider value (e.g., 1, 2, 4) or 'MINimum'/'MAXimum'

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        valid_keywords = ["MINimum", "MAXimum"]
        if self.resource:
            try:
                if isinstance(divider, int):
                    divider_str = str(divider)
                elif isinstance(divider, str) and divider.upper() in [v.upper() for v in valid_keywords]:
                    divider_str = divider.upper()
                else:
                    return {"Error": f"Invalid divider. Must be an integer or one of {valid_keywords}"}

                command = f":OUTP:ROSC:SCD {divider_str}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                self.log._log_command(command, duration_ms=duration, response="Divider set")
                return {"Status": f"Sample clock divider set to {divider_str}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_sample_clock_divider(self):
        """
        Query the current DAC sample clock divider for the reference clock output.

        Returns:
            dict: {"Sample Clock Divider": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = ":OUTP:ROSC:SCD?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000

                self.log._log_command(command, duration_ms=duration, response=response)
                return {"Sample Clock Divider": response, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_reference_clock_divider1(self, divider):
        """
        Set the first divider of the reference clock signal routed to the reference clock output.

        Args:
            divider (int or str): Divider value (e.g., 1, 2, ...) or 'MINimum'/'MAXimum'

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        valid_keywords = ["MINimum", "MAXimum"]
        if self.resource:
            try:
                if isinstance(divider, int):
                    divider_str = str(divider)
                elif isinstance(divider, str) and divider.upper() in [v.upper() for v in valid_keywords]:
                    divider_str = divider.upper()
                else:
                    return {"Error": f"Invalid divider. Must be an integer or one of {valid_keywords}"}

                command = f":OUTP:ROSC:RCD1 {divider_str}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                self.log._log_command(command, duration_ms=duration, response="Reference Clock Divider 1 set")
                return {"Status": f"Reference Clock Divider 1 set to {divider_str}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_reference_clock_divider1(self):
        """
        Query the first divider of the reference clock signal routed to the reference clock output.

        Returns:
            dict: {"Reference Clock Divider 1": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = ":OUTP:ROSC:RCD1?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000

                self.log._log_command(command, duration_ms=duration, response=response)
                return {"Reference Clock Divider 1": response, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_reference_clock_divider2(self, divider):
        """
        Set the second divider of the external reference clock signal.

        Args:
            divider (int or str): Divider value (e.g., 1, 2, ...) or 'MINimum'/'MAXimum'

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        valid_keywords = ["MINimum", "MAXimum"]
        if self.resource:
            try:
                if isinstance(divider, int):
                    divider_str = str(divider)
                elif isinstance(divider, str) and divider.upper() in [v.upper() for v in valid_keywords]:
                    divider_str = divider.upper()
                else:
                    return {"Error": f"Invalid divider. Must be an integer or one of {valid_keywords}"}

                command = f":OUTP:ROSC:RCD2 {divider_str}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                self.log._log_command(command, duration_ms=duration, response="Reference Clock Divider 2 set")
                return {"Status": f"Reference Clock Divider 2 set to {divider_str}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_reference_clock_divider2(self):
        """
        Query the second divider of the external reference clock signal.

        Returns:
            dict: {"Reference Clock Divider 2": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = ":OUTP:ROSC:RCD2?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000

                self.log._log_command(command, duration_ms=duration, response=response)
                return {"Reference Clock Divider 2": response, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_differential_offset(self, channel, offset):
        """
        Set the differential offset for a specific output channel.

        Args:
            channel (int): Output channel (1 to 4)
            offset (float or str): Offset value or 'MINimum' / 'MAXimum'

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        valid_keywords = ["MINimum", "MAXimum"]
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be 1, 2, 3, or 4."}
            try:
                if isinstance(offset, float) or isinstance(offset, int):
                    offset_str = str(offset)
                elif isinstance(offset, str) and offset.upper() in [k.upper() for k in valid_keywords]:
                    offset_str = offset.upper()
                else:
                    return {"Error": f"Invalid offset. Must be float or one of {valid_keywords}"}

                command = f":OUTP{channel}:DIOF {offset_str}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                self.log._log_command(command, duration_ms=duration, response="Differential offset set")
                return {"Status": f"Differential offset for channel {channel} set to {offset_str}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_differential_offset(self, channel):
        """
        Query the differential offset for a specific output channel.

        Args:
            channel (int): Output channel (1 to 4)

        Returns:
            dict: {"Differential Offset": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be 1, 2, 3, or 4."}
            try:
                command = f":OUTP{channel}:DIOF?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000

                self.log._log_command(command, duration_ms=duration, response=response)
                return {"Differential Offset": float(response), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_fir_filter_coefficients(self, channel, coefficients):
        """
        Set 16 FIR filter coefficients for the specified channel (USER-defined filter only).

        Args:
            channel (int): Channel number (1–4)
            coefficients (list of float): 16 float values in range [-2, 2]

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be 1 to 4."}
            if not isinstance(coefficients, list) or len(coefficients) != 16:
                return {"Error": "Must provide a list of exactly 16 coefficients."}
            if not all(isinstance(c, (int, float)) and -2 <= c <= 2 for c in coefficients):
                return {"Error": "Each coefficient must be a float between -2 and 2."}

            try:
                coeff_str = ",".join([str(c) for c in coefficients])
                command = f":OUTP{channel}:FILT:FRAT {coeff_str}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response="FIR filter coefficients set")
                return {"Status": f"FIR coefficients set for channel {channel}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_fir_filter_coefficients(self, channel):
        """
        Query FIR filter coefficients for the specified channel.

        Args:
            channel (int): Channel number (1–4)

        Returns:
            dict: {"FIR Coefficients": [...], "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be 1 to 4."}
            try:
                command = f":OUTP{channel}:FILT:FRAT?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000

                coeffs = [float(val.strip()) for val in response.split(",")]
                self.log._log_command(command, duration_ms=duration, response=response)
                return {"FIR Coefficients": coeffs, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_fir_filter_type(self, channel, filter_type):
        """
        Set the FIR filter type for a specific output channel.

        Args:
            channel (int): Output channel number (1 to 4)
            filter_type (str): One of 'LOWPass', 'ZOH', or 'USER'

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        valid_types = ["LOWPass", "ZOH", "USER"]
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be 1 to 4."}
            if filter_type.upper() not in [t.upper() for t in valid_types]:
                return {"Error": f"Invalid filter type. Must be one of {valid_types}"}
            try:
                command = f":OUTP{channel}:FILT:FRAT:TYPE {filter_type.upper()}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=f"Filter type set to {filter_type.upper()}")
                return {"Status": f"FIR filter type set to {filter_type.upper()} for channel {channel}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_fir_filter_type(self, channel):
        """
        Query the FIR filter type for a specific output channel.

        Args:
            channel (int): Output channel number (1 to 4)

        Returns:
            dict: {"FIR Filter Type": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be 1 to 4."}
            try:
                command = f":OUTP{channel}:FILT:FRAT:TYPE?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {"FIR Filter Type": response, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}

    def set_fir_filter_scale(self, channel, scale: float):
        """
        Set a specific FIR filter scale (0.0 to 1.0) for the given output channel.

        Args:
            channel (int): Output channel (1 to 4)
            scale (float): Value between 0.0 and 1.0

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be between 1 and 4."}
            if not isinstance(scale, (int, float)) or not (0.0 <= scale <= 1.0):
                raise ValueError
            try:
                command = f":OUTP{channel}:FILT:FRAT:SCAL {scale}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response="Set FIR scale")
                return {"Status": f"Filter scale set to {scale}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def _set_fir_filter_scale_keyword(self, channel, keyword):
        """
        Internal method to send MINimum or MAXimum as FIR filter scale.

        Args:
            channel (int): Output channel
            keyword (str): 'MINimum' or 'MAXimum'

        Returns:
            dict
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be 1 to 4."}
            if keyword.upper() not in ["MIN", "MAX"]:
                raise ValueError
            try:
                command = f":OUTP{channel}:FILT:FRAT:SCAL {keyword.upper()}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=f"Scale set to {keyword}")
                return {"Status": f"FIR filter scale set to {keyword.upper()}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_fir_filter_scale(self, channel):
        """
        Query the current FIR filter scaling factor for the given output channel.

        Args:
            channel (int): Output channel (1 to 4)

        Returns:
            dict: {"Filter Scale": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be 1 to 4."}
            try:
                command = f":OUTP{channel}:FILT:FRAT:SCAL?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {"Filter Scale": float(response), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}

    
    def set_fir_filter_delay(self, channel, delay_value: str):
        """
        Set the FIR filter delay for the specified output channel (used with LOWPass filter type only).

        Args:
            channel (int): Output channel (1 to 4)
            delay_value (str): Delay string with units (e.g., '-25ps', '10ps', '0')

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be 1 to 4."}
            try:
                command = f":OUTP{channel}:FILT:FRAT:DEL {delay_value}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=f"Delay set to {delay_value}")
                return {"Status": f"FIR delay for channel {channel} set to {delay_value}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def _set_fir_filter_delay_keyword(self, channel, keyword):
        """
        Internal method to send MINimum or MAXimum FIR filter delay.

        Args:
            channel (int): Output channel
            keyword (str): 'MINimum' or 'MAXimum'

        Returns:
            dict
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be 1 to 4."}
            if keyword.upper() not in ["MIN", "MAX"]:
                return {"Error": "Invalid keyword. Must be 'MINimum' or 'MAXimum'."}
            try:
                command = f":OUTP{channel}:FILT:FRAT:DEL {keyword.upper()}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=f"Delay set to {keyword}")
                return {"Status": f"FIR delay set to {keyword.upper()} for channel {channel}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_fir_filter_delay(self, channel):
        """
        Query the current FIR filter delay for the specified output channel.

        Args:
            channel (int): Output channel (1 to 4)

        Returns:
            dict: {"FIR Delay": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be 1 to 4."}
            try:
                command = f":OUTP{channel}:FILT:FRAT:DEL?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {"FIR Delay": response, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_high_rate_filter_coefficients(self, channel, coefficients):
        """
        Set FIR filter coefficients for HRATe (Sample Rate Divider = 2) on the specified channel.

        Args:
            channel (int): Output channel (1 to 4)
            coefficients (list of float): 32 coefficients between -2.0 and 2.0

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be 1 to 4."}
            if not isinstance(coefficients, list) or len(coefficients) != 32:
                return {"Error": "You must provide exactly 32 coefficients."}
            if not all(isinstance(c, (int, float)) and -2.0 <= c <= 2.0 for c in coefficients):
                return {"Error": "All coefficients must be floats between -2.0 and 2.0."}
            try:
                coeff_str = ",".join(f"{c:.6g}" for c in coefficients)
                command = f":OUTP{channel}:FILT:HRAT {coeff_str}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response="HRAT coefficients set")
                return {"Status": f"32 FIR coefficients set for HRATe on channel {channel}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    

    def get_high_rate_filter_coefficients(self, channel):
        """
        Query FIR filter coefficients for HRATe (Sample Rate Divider = 2) on the specified channel.

        Args:
            channel (int): Output channel (1 to 4)

        Returns:
            dict: {"HRAT Coefficients": [...], "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be 1 to 4."}
            try:
                command = f":OUTP{channel}:FILT:HRAT?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000
                coeffs = [float(val.strip()) for val in response.split(',') if val.strip()]
                self.log._log_command(command, duration_ms=duration, response=response)
                return {"HRAT Coefficients": coeffs, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_high_rate_filter_type(self, channel, filter_type: str):
        """
        Set predefined FIR filter type for HRATe filter (Sample Rate Divider = 2) on the given channel.

        Args:
            channel (int): Output channel (1 to 4)
            filter_type (str): One of 'NYQuist', 'LINear', 'ZOH', 'USER'

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            valid_types = ["NYQ", "LIN", "ZOH", "USER"]
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be between 1 and 4."}
            if filter_type.upper() not in valid_types:
                return {"Error": f"Invalid filter type. Allowed: {', '.join(valid_types)}"}
            try:
                command = f":OUTP{channel}:FILT:HRAT:TYPE {filter_type.upper()}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response="Set HRAT filter type")
                return {"Status": f"Filter type set to {filter_type.upper()}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_high_rate_filter_type(self, channel):
        """
        Query the current FIR filter type for HRATe on the specified output channel.

        Args:
            channel (int): Output channel (1 to 4)

        Returns:
            dict: {"HRAT Filter Type": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be 1 to 4."}
            try:
                command = f":OUTP{channel}:FILT:HRAT:TYPE?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {"HRAT Filter Type": response, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_high_rate_filter_scale(self, channel, scale: float):
        """
        Set FIR filter scale factor for HRATe filter (SR Divider = 2) on the specified channel.

        Args:
            channel (int): Output channel (1 to 4)
            scale (float): Scale factor between 0.0 and 1.0

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be between 1 and 4."}
            if not (0.0 <= scale <= 1.0):
                return {"Error": "Scale must be between 0.0 and 1.0."}
            try:
                command = f":OUTP{channel}:FILT:HRAT:SCAL {scale:.6g}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response="Scale factor set")
                return {"Status": f"HRAT scale set to {scale} for channel {channel}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def _set_hrat_scale_keyword(self, channel, keyword):
        """
        Internal helper to send MINimum or MAXimum scale value to HRAT filter.

        Args:
            channel (int): Output channel
            keyword (str): 'MINimum' or 'MAXimum'

        Returns:
            dict
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be between 1 and 4."}
            if keyword.upper() not in ["MIN", "MAX"]:
                return {"Error": "Invalid keyword. Must be 'MINimum' or 'MAXimum'."}
            try:
                command = f":OUTP{channel}:FILT:HRAT:SCAL {keyword.upper()}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=f"Set to {keyword.upper()}")
                return {"Status": f"HRAT scale set to {keyword.upper()} for channel {channel}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_high_rate_filter_scale(self, channel):
        """
        Query the current FIR filter scale factor for HRATe filter on the specified channel.

        Args:
            channel (int): Output channel (1 to 4)

        Returns:
            dict: {"HRAT Scale": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be between 1 and 4."}
            try:
                command = f":OUTP{channel}:FILT:HRAT:SCAL?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {"HRAT Scale": response, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_high_rate_filter_delay(self, channel, delay: str):
        """
        Set FIR filter delay for HRATe filter (Sample Rate Divider = 2) on the specified channel.

        Args:
            channel (int): Output channel (1 to 4)
            delay (str): Delay with unit (e.g., '10ps', '-50ps', '0.5ns')

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be 1 to 4."}
            if not isinstance(delay, str):
                return {"Error": "Delay must be a string with unit, e.g., '10ps'"}
            try:
                command = f":OUTP{channel}:FILT:HRAT:DEL {delay}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response="Set delay")
                return {"Status": f"Delay set to {delay} on channel {channel}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def _set_hrat_delay_keyword(self, channel, keyword: str):
        """
        Internal helper to send MINimum or MAXimum delay to HRAT filter.

        Args:
            channel (int): Output channel
            keyword (str): 'MINimum' or 'MAXimum'

        Returns:
            dict
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be 1 to 4."}
            if keyword.upper() not in ["MIN", "MAX"]:
                return {"Error": "Keyword must be 'MINimum' or 'MAXimum'."}
            try:
                command = f":OUTP{channel}:FILT:HRAT:DEL {keyword.upper()}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=f"Set to {keyword.upper()}")
                return {"Status": f"Delay set to {keyword.upper()} for channel {channel}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_high_rate_filter_delay(self, channel):
        """
        Query current FIR filter delay for HRATe filter on the specified output channel.

        Args:
            channel (int): Output channel (1 to 4)

        Returns:
            dict: {"HRAT Delay": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be 1 to 4."}
            try:
                command = f":OUTP{channel}:FILT:HRAT:DEL?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {"HRAT Delay": response, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_qrate_filter_coefficients(self, channel, coefficients: list):
        """
        Set 64 FIR filter coefficients for the QRATe filter (SR Divider = 4) for a specific channel.

        Args:
            channel (int): Output channel (1 to 4)
            coefficients (list): List of 64 float values between -2.0 and 2.0

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be between 1 and 4."}
            if not isinstance(coefficients, list) or len(coefficients) != 64:
                return {"Error": "Exactly 64 coefficients must be provided."}
            if not all(isinstance(c, (int, float)) and -2.0 <= c <= 2.0 for c in coefficients):
                return {"Error": "Each coefficient must be a number between -2.0 and 2.0."}

            try:
                coeff_str = ",".join(f"{c:.6g}" for c in coefficients)
                command = f":OUTP{channel}:FILT:QRAT {coeff_str}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response="QRAT coefficients set")
                return {"Status": f"QRAT coefficients set for channel {channel}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_qrate_filter_coefficients(self, channel):
        """
        Query the FIR filter coefficients for the QRATe filter (SR Divider = 4) for a specific channel.

        Args:
            channel (int): Output channel (1 to 4)

        Returns:
            dict: {"QRAT Coefficients": [...], "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be between 1 and 4."}

            try:
                command = f":OUTP{channel}:FILT:QRAT?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000

                coeffs = [float(val.strip()) for val in response.split(",") if val.strip()]
                if len(coeffs) != 64:
                    raise ValueError("Unexpected number of coefficients returned.")
                self.log._log_command(command, duration_ms=duration, response=response)
                return {"QRAT Coefficients": coeffs, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_qrate_filter_scale(self, channel: int, scale: float):
        """
        Set the FIR filter scaling factor for QRATe filter (Sample Rate Divider = 4) on a specified channel.

        Args:
            channel (int): Output channel (1–4)
            scale (float): Scaling factor (between 0.0 and 1.0)

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be 1 to 4."}
            if not isinstance(scale, (int, float)) or not (0.0 <= scale <= 1.0):
                return {"Error": "Scale must be a float between 0 and 1."}

            try:
                command = f":OUTP{channel}:FILT:QRAT:SCAL {scale}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response="Scaling factor set")
                return {"Status": f"QRAT scaling factor set to {scale} for channel {channel}",
                        "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_qrate_filter_scale_min(self, channel: int):
        """
        Set the FIR filter scaling factor to MIN for QRATe filter (SR Divider = 4) on a specific channel.

        Args:
            channel (int): Output channel (1–4)

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be 1 to 4."}
            try:
                command = f":OUTP{channel}:FILT:QRAT:SCAL MIN"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response="Set to MIN")
                return {"Status": f"QRAT scaling factor set to MIN for channel {channel}",
                        "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_qrate_filter_scale_max(self, channel: int):
        """
        Set the FIR filter scaling factor to MAX for QRATe filter (SR Divider = 4) on a specific channel.

        Args:
            channel (int): Output channel (1–4)

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be 1 to 4."}
            try:
                command = f":OUTP{channel}:FILT:QRAT:SCAL MAX"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response="Set to MAX")
                return {"Status": f"QRAT scaling factor set to MAX for channel {channel}",
                        "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_qrate_filter_scale(self, channel: int):
        """
        Query the FIR filter scaling factor for QRATe filter (Sample Rate Divider = 4) on a specific channel.

        Args:
            channel (int): Output channel (1–4)

        Returns:
            dict: {"QRAT Scale": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be 1 to 4."}
            try:
                command = f":OUTP{channel}:FILT:QRAT:SCAL?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000

                scale_value = float(response)
                self.log._log_command(command, duration_ms=duration, response=response)
                return {"QRAT Scale": scale_value, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_qrate_filter_custom_delay(self, channel: int, delay: str):
        """
        Set a custom FIR filter delay for the QRATe filter (SR Divider = 4) on a specific channel.

        Args:
            channel (int): Output channel (1-4)
            delay (str): Delay value with units (e.g., '10ps', '0.2ns', '-100ps')

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be between 1 and 4"}
            try:
                command = f":OUTP{channel}:FILT:QRAT:DEL {delay}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response="Custom delay set")
                return {"Status": f"QRAT delay set to {delay} on channel {channel}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_qrate_filter_delay_min_max(self, channel: int, mode: str):
        """
        Set the FIR filter delay to MINimum or MAXimum for QRATe filter on a specific channel.

        Args:
            channel (int): Output channel (1-4)
            mode (str): Either "MIN" or "MAX"

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be between 1 and 4"}
            if mode.upper() not in ["MIN", "MAX"]:
                return {"Error": "Invalid mode. Use 'MIN' or 'MAX'"}
            try:
                command = f":OUTP{channel}:FILT:QRAT:DEL {mode.upper()}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=f"Delay set to {mode.upper()}")
                return {"Status": f"QRAT delay set to {mode.upper()} for channel {channel}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_qrate_filter_delay(self, channel: int):
        """
        Query the FIR filter delay for QRATe filter on a specified channel.
    
        Args:
            channel (int): Output channel (1–4)
    
        Returns:
            dict: {"QRAT Delay": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be 1 to 4."}
            try:
                command = f":OUTP{channel}:FILT:QRAT:DEL?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {"QRAT Delay": response, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}





























    










