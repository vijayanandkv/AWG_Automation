#import the required AWG modules
from VISAInterface import pyvisa_interface
from AWGConnection import AWG_connection
from logger import awg_logger

import time



class AWG_common_commands:
    def __init__(self, ip_address: str):
        self.ip_address = ip_address

        #create insatces for connection and logger classes
        self.connection = AWG_connection(ip_address)
        self.log = awg_logger()

        #select the recourse from connection class
        self.resource = self.connection.get_resource()
        
    """Returns the instrument’s identification string containing manufacturer, model number, serial number, and firmware revision details."""
    def get_device_identity(self):
        if self.resource:
            try:
                start_time = time()
                idn = self.resource.query("*IDN?")
                end_time = time()
                exe_duration = (end_time - start_time) * 1000 # in milli seconds
                log_line = self.log._log_command(command= "*IDN?", duration_ms=exe_duration, response= str(idn))
                return {"IDN": str(idn), "execution time": exe_duration}
        
            except Exception as e:
                return {"error": str(e)}
    def clear_status(self):
        """
            Sends the *CLS command to the instrument to:
            - Clear the event registers in all register groups
            - Clear the error queue
            - Cancel any pending *OPC operations """
        if self.resource:
            try:
                start_time = time()
                self.resource.write("*CLS")
                end_time = time()
                duration = (end_time - start_time) *1000
                self.log._log_command(command="*CLS", duration_ms= duration, response= "Event registers and error queue cleared.")
                return {"status": "success", "message": "Cleared event registers and error queue."}
            except Exception as e:
                self.log._log_command(command="*CLS", duration_ms=0, response= "Failed to clear event register and error queue")
                return str(e)


    def set_standard_event_status_enable(self, value: int):
        """Enables specific bits (0–255) in the Standard Event Status Enable Register so that selected events can be reported via the Status
          Byte Register"""
        
        if self.resource:
            if not (0 <= value <= 255):
                error_msg = f"Value {value} out of valid range (0–255) for *ESE."
                self._log_command(command=f"*ESE {value}", duration_ms=0, response=error_msg)
                raise ValueError(error_msg)
        
            try:
                start_t = time()
                command = f"*ESE{value}"
                query = f"*ESE{value}?"
                self.resource.write(command)
                stop_t = time()
                status = self.resource.query(query)
                duration = (stop_t - start_t) * 1000
                self.log._log_command(command= command, duration_ms= duration, response= str(status))
                return {"status": str(status), "time in milli secs":duration}
            except Exception as e:
                self.log._log_command(command= command, duration_ms= 0, response= str(e))
                return str(e)
            
    def event_status_enable(self, value: int):
        """Enables specific bits (0–255) in the Standard Event Status Enable Register so that selected events can be reported via the Status
          Byte Register"""
        
        if self.resource:
            if not (0 <= value <= 255):
                error_msg = f"Value {value} out of valid range (0–255) for *ESE."
                self._log_command(command=f"*ESE {value}", duration_ms=0, response=error_msg)
                raise ValueError(error_msg)
        
            try:
                start_t = time()
                query = f"*ESE{value}?"
                stop_t = time()
                status = self.resource.query(query)
                duration = (stop_t - start_t) * 1000
                self.log._log_command(command= query, duration_ms= duration, response= str(status))
                return {"status": str(status), "time in milli secs":duration}
            except Exception as e:
                self.log._log_command(command= query, duration_ms= 0, response= str(e))
                return str(e)
    
    def query_standard_event_status_register(self):
        """
        Query the Standard Event Status Register (*ESR?).
        Returns the binary-weighted sum of all set bits in the register.
        Bits are cleared after this query.
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query("*ESR?").strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command="*ESR?", duration_ms=duration, response=response)
                return int(response)
            except Exception as e:
                self.log._log_command(command="*ESR?", duration_ms=0, response=str(e))
                return {"error": str(e)}
        else:
            self.log._log_command(command="*ESR?", duration_ms=0, response="No connection to resource")
            return {"error": "No connection to resource"}

    def set_operation_complete(self):
        """
        Send *OPC command to set the Operation Complete bit in the Standard Event Status Register
        after all previous commands are completed.
        """
        if self.resource:
            try:
                start_time = time.time()
                self.resource.write("*OPC")
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command="*OPC", duration_ms=duration, response="Set operation complete")
                return {"status": "Operation Complete bit set", "duration_ms": duration}
            except Exception as e:
                self.log._log_command(command="*OPC", duration_ms=0, response=str(e))
                return {"error": str(e)}
        else:
            self.log._log_command(command="*OPC", duration_ms=0, response="No connection to resource")
            return {"error": "No connection to resource"}
        
    def query_operation_complete(self):
        """
        Send *OPC? query to check if all prior commands have completed.
        Returns '1' when operations are complete.
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query("*OPC?")
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command="*OPC?", duration_ms=duration, response=response.strip())
                return {"OPC_Response": response.strip(), "duration_ms": duration}
            except Exception as e:
                self.log._log_command(command="*OPC?", duration_ms=0, response=str(e))
                return {"error": str(e)}
        else:
            self.log._log_command(command="*OPC?", duration_ms=0, response="No connection to resource")
            return {"error": "No connection to resource"}
    
    def read_installed_options(self):
        """
        Query the installed options on the AWG using *OPT?.

        Returns:
            dict: A dictionary with installed options and execution duration.
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query("*OPT?")
                duration = (time.time() - start_time) * 1000  # ms
                self.log._log_command("*OPT?", duration_ms=duration, response=response.strip())
                return {"Options": response.strip(), "Duration (ms)": duration}
            except Exception as e:
                self.log._log_command("*OPT?", duration_ms=0, response=str(e))
                return {"Error": str(e), "Options": None}
        else:
            self.log._log_command("*OPT?", duration_ms=0, response="No resource connected")
            return {"Error": "No connection to device", "Options": None}
        
    def reset_instrument(self):
        """
        Reset the AWG to its factory default state using *RST.

        Returns:
            dict: Status message and execution duration.
        """
        if self.resource:
            try:
                start_time = time.time()
                self.resource.write("*RST")
                duration = (time.time() - start_time) * 1000  # ms
                self.log._log_command("*RST", duration_ms=duration, response="Instrument reset to factory defaults")
                return {"Status": "Instrument reset", "Duration (ms)": duration}
            except Exception as e:
                self.log._log_command("*RST", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command("*RST", duration_ms=0, response="No resource connected")
            return {"Error": "No connection to device"}
    
    def set_service_request_enable_register(self, value: int):
        """
        Set bits in the Status Byte Register to enable Service Requests (*SRE) and query the result.

        Args:
            value (int): Integer (0–255) indicating bits to enable.

        Returns:
            dict: Status and value returned by *SRE? query.
        """
        if not (0 <= value <= 255):
            return {"Error": "Value must be between 0 and 255"}

        if self.resource:
            try:
                start_time = time.time()

                # Set the SRE
                self.resource.write(f"*SRE {value}")
                write_duration = (time.time() - start_time) * 1000
                self.log._log_command(f"*SRE {value}", duration_ms=write_duration, response="SRE set")

                # Query the SRE
                query_start = time.time()
                response = self.resource.query("*SRE?")
                query_duration = (time.time() - query_start) * 1000
                self.log._log_command("*SRE?", duration_ms=query_duration, response=response.strip())

                return {
                    "SRE Value Set": value,
                    "SRE? Response": response.strip(),
                    "Total Duration (ms)": write_duration + query_duration
                }

            except Exception as e:
                self.log._log_command("*SRE / *SRE?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command("*SRE / *SRE?", duration_ms=0, response="No connection to device")
            return {"Error": "No connection to device"}
        
    def query_service_request_enable_register(self):
        """
        Query the current value of the Status Byte Enable Register using *SRE?.

        Returns:
            dict: Current SRE register value or error message.
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query("*SRE?")
                duration = (time.time() - start_time) * 1000
                self.log._log_command("*SRE?", duration_ms=duration, response=response.strip())
                return {"SRE? Response": response.strip(), "Query Duration (ms)": duration}
            except Exception as e:
                self.log._log_command("*SRE?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command("*SRE?", duration_ms=0, response="Device not connected")
            return {"Error": "No connection to device"}


    def query_status_byte_register(self):
        """
        Query the Status Byte Register using *STB?.

        Returns:
            dict: Status byte value or error message.
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query("*STB?")
                duration = (time.time() - start_time) * 1000
                self.log._log_command("*STB?", duration_ms=duration, response=response.strip())
                return {"STB? Response": response.strip(), "Query Duration (ms)": duration}
            except Exception as e:
                self.log._log_command("*STB?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command("*STB?", duration_ms=0, response="Device not connected")
            return {"Error": "No connection to device"}
        
    def run_self_test(self):
        """
        Execute built-in self-test using *TST?.

        Returns:
            dict: Test result (0 = pass, >0 = failure count) or error details.
        """
        if self.resource:
            try:
                start_time = time.time()
                result = self.resource.query("*TST?").strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command("*TST?", duration_ms=duration, response=result)
                return {"SelfTest Result": result, "Duration (ms)": duration}
            except Exception as e:
                self.log._log_command("*TST?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command("*TST?", duration_ms=0, response="Device not connected")
            return {"Error": "No connection to device"}
        
    def get_learn_string(self):
        """
        Query the instrument's current configuration state (learn string) using *LRN?.

        Returns:
            dict: Learn string or error information.
        """
        if self.resource:
            try:
                start_time = time.time()
                learn_string = self.resource.query("*LRN?")
                duration = (time.time() - start_time) * 1000
                self.log._log_command("*LRN?", duration_ms=duration, response="Learn string retrieved")
                return {"LearnString": learn_string.strip(), "Duration (ms)": duration}
            except Exception as e:
                self.log._log_command("*LRN?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command("*LRN?", duration_ms=0, response="Device not connected")
            return {"Error": "No connection to device"}
        
    def wait_until_done(self):
        """
        Prevent the instrument from executing further commands until the current one finishes.
    
        Uses *WAI to block execution until all pending operations are complete.
        """
        if self.resource:
            try:
                start_time = time.time()
                self.resource.write("*WAI")
                duration = (time.time() - start_time) * 1000
                self.log._log_command("*WAI", duration_ms=duration, response="Wait completed")
                return {"Status": "Wait complete", "Duration (ms)": duration}
            except Exception as e:
                self.log._log_command("*WAI", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command("*WAI", duration_ms=0, response="Device not connected")
            return {"Error": "No connection to device"}









            


