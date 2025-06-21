#import awg modules
from AWGConnection import AWG_connection
from logger import awg_logger

#import other modules
import time

class AWG_Trigger_input:
    def __init__(self, ip_address):
        self.ip_address = ip_address

        #create insatces for connection and logger classes
        self.connection = AWG_connection(ip_address)
        self.log = awg_logger()

        #select the recourse from connection class
        self.resource = self.connection.get_resource()

    def set_trig_advance_source(self, source_type: str):
        """
        Set the source for the advancement event.

        Args:
            source_type (str): One of ['TRIGger', 'EVENt', 'INTernal']

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        valid_sources = ["TRIGger", "EVENt", "INTernal"]

        if source_type not in valid_sources:
            return {"Error": f"Invalid source_type '{source_type}'. Must be one of {valid_sources}"}

        if self.resource:
            try:
                command = f":TRIG:SOUR:ADV {source_type}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                response = self.get_trig_advance_source()
                self.log._log_command(command, duration_ms=duration, response=str(response))
                return {"Status": f"Advance source set to {source_type}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_trig_advance_source(self):
        """
        Query the current source for the advancement event.

        Returns:
            dict: {"Advance Source": source, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                command = ":TRIG:SOUR:ADV?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000

                source = response.strip()
                self.log._log_command(command, duration_ms=duration, response=source)
                return {"Advance Source": source, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def send_enable_event(self):
        """
        Send the enable event to a channel (immediate trigger enable).

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = ":TRIG:ENAB"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                self.log._log_command(command, duration_ms=duration, response="Enable event sent")
                return {"Status": "Enable event sent successfully", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def send_begin_event(self):
        """
        Send the start/begin event in triggered mode.

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = ":TRIG:BEG"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                self.log._log_command(command, duration_ms=duration, response="Begin event sent")
                return {"Status": "Begin event sent successfully", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_begin_gate_state(self, state: str):
        """
        Set the gate state in gated mode (open or close the gate).

        Args:
            state (str): 'ON', 'OFF', '1', or '0'

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        valid_states = ["ON", "OFF", "1", "0"]
        if state.upper() not in valid_states:
            return {"Error": f"Invalid state '{state}'. Must be one of {valid_states}"}

        if self.resource:
            try:
                command = f":TRIG:BEG:GATE {state.upper()}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                response = self.get_begin_gate_state()
                self.log._log_command(command, duration_ms=duration, response=str(response))
                return {"Status": f"Gate state set to {state.upper()}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_begin_gate_state(self):
        """
        Query the current gate state in gated mode.

        Returns:
            dict: {"Gate State": 'ON' or 'OFF', "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                command = ":TRIG:BEG:GATE?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000

                state = response.strip()
                self.log._log_command(command, duration_ms=duration, response=state)
                return {"Gate State": state, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def send_advance_event(self):
        """
        Send the advancement event to the AWG (used to manually advance in sequence mode).
    
        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = ":TRIG:ADV"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
    
                self.log._log_command(command, duration_ms=duration, response="Advance event sent")
                return {"Status": "Advance event sent successfully", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}






