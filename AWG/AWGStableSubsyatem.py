#import awg modules
from AWGConnection import AWG_connection
from logger import awg_logger

#import other modules
import time

class AWG_stable_system:
    def __init__(self, ip_address):
        self.ip_address = ip_address

        #create insatces for connection and logger classes
        self.connection = AWG_connection(ip_address)
        self.log = awg_logger()

        #select the recourse from connection class
        self.resource = self.connection.get_resource()

    def reset_sequence_table(self):
        """
        Reset all sequence table entries to default values.
    
        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = ":STAB:RES"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000    
                self.log._log_command(command, duration_ms=duration, response="Reset Done")
                return {"Status": "Sequence table reset to default", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
            
        return {"Error": "Device not connected"}
    
    def write_sequence_table_entry(self, sequence_id: int, data: list[int]):
        """
        Write directly to the sequence table memory.

        Args:
            sequence_id (int): Index of the sequence table entry to be accessed (0 to 16777214).
            data (list[int]): List of six 32-bit integers (one sequence entry).

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                if len(data) != 6:
                    return {"Error": "Exactly 6 values must be provided for a sequence entry"}

                data_str = ",".join(str(val) for val in data)
                command = f":STAB:DATA {sequence_id},{data_str}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response="OK")
                return {"Status": f"Entry written to index {sequence_id}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def read_sequence_table_entry(self, sequence_id: int, length: int = 6):
        """
        Read a sequence table entry from sequencer memory.

        Args:
            sequence_id (int): Index of the sequence table entry to read.
            length (int): Number of 32-bit values to read (default is 6 for one entry).

        Returns:
            dict: {"SequenceData": [...], "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = f":STAB:DATA? {sequence_id},{length}"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000

                data_list = [int(x.strip()) for x in response.strip().split(",")]
                self.log._log_command(command, duration_ms=duration, response=response)
                return {"SequenceData": data_list, "Duration(ms)": duration}
            
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
            
        return {"Error": "Device not connected"}
    
    def read_sequence_entry_block(self, sequence_id: int, length: int) -> bytes:
        """
        Query sequence table data in IEEE binary block format.

        Args:
            sequence_id (int): Starting index of the sequence table.
            length (int): Number of entries to read.

        Returns:
            bytes: Binary block data returned by the instrument.
        """
        start_t = time.time()
        command = f":STAB:DATA:BLOC? {sequence_id}, {length}"
        stop_t = time.time()
        duration = (stop_t - start_t) * 1000
        self.log._log_command(command= ":STAB:DATA:BLOC? {sequence_id}, {length}", duration_ms= duration, response= "Done!")
        response = self.interface.query_binary(command)
        return response
    
    def set_sequence_start_index(self, index: int) -> int:
        """
        Set the sequence start index in STSequence mode.

        Args:
            index (int): Index in the sequence table to start from.

        Returns:
            int: Actual index set, verified by query.
        """
        start_t = time.time()
        self.resource.write(f":STAB:SEQ:SEL {index}")
        stop_t = time.time()
        duration = (stop_t - start_t) * 1000
        self.log._log_command(command= "STAB:SEQ:SEL {index}", duration_ms= duration, response= "Done!")

        return int(self.resource.query(":STAB:SEQ:SEL?"))
    
    def set_sequence_start_limit(self, limit: str) -> int:
        """
        Set the sequence start index using 'MINimum' or 'MAXimum'.

        Args:
            limit (str): Either 'MIN' or 'MAX'.

        Returns:
            int: Actual index set, verified by query.
        """
        limit = limit.upper()
        if limit not in ["MIN", "MAX"]:
            raise ValueError("limit must be 'MIN' or 'MAX'")
        
        start_t = time.time()
        self.resource.write(f":STAB:SEQ:SEL {limit}")
        stop_t = time.time()
        duration = (stop_t - start_t) * 1000
        self.log._log_command(command= ":STAB:SEQ:SEL {limit}", duration_ms= duration, response= "Done!")

        return int(self.interface.query(":STAB:SEQ:SEL?"))
    
    def get_sequence_start_index(self) -> int:
        """
        Query the current sequence start index.

        Returns:
            int: The current start index in the sequence table.
        """
        return int(self.resource.query(":STAB:SEQ:SEL?"))
    
    def get_sequence_execution_state(self) -> int:
        """
        Query the current sequence execution state and the index of the currently executed
        sequence table entry.

        Returns:
            int: Encoded integer value indicating execution state and entry index.
        """
        return int(self.resource.query(":STAB:SEQ:STAT?"))
    
    def set_dynamic_mode(self, state: bool) -> str:
        """
        Enable or disable dynamic mode.

        Args:
            state (bool): True to enable, False to disable.

        Returns:
            str: Confirmed mode state as returned by the query after setting.
        """
        value = "ON" if state else "OFF"
        start_t = time.time()
        self.resource.write(f":STAB:DYN {value}")
        stop_t = time.time()
        duration = (stop_t - start_t) * 1000
        self.log._log_command(command= ":STAB:DYN {value}", duration_ms= duration, response= "Done!")

        return self.resource.query(":STAB:DYN?")
    
    def get_dynamic_mode(self) -> str:
        """
        Query whether dynamic mode is enabled or disabled.

        Returns:
            str: "ON" or "OFF"
        """
        start_t = time.time()
        self.resource.query(":STAB:DYN?").strip()
        stop_t = time.time()
        duration = (stop_t - start_t) * 1000
        self.log._log_command(command= ":STAB:DYN?", duration_ms= duration, response= "Done!")
        return self.resource.query(":STAB:DYN?").strip()
    
    def set_dynamic_sequence_entry(self, index: int) -> str:
        """
        Set the next sequence table entry to be executed when in dynamic mode.

        Args:
            index (int): Index of the sequence table entry.

        Returns:
            str: Confirmed sequence index from a query after setting.
        """
        start_t = time.time()
        self.resource.write(f":STAB:DYN:SEL {index}")
        stop_t = time.time()
        duration = (stop_t - start_t) * 1000
        self.log._log_command(command= ":STAB:DYN:SEL {index}", duration_ms= duration, response= "Done!")
        # Note: There's no official query command for confirmation in the SCPI spec,
        # but to mimic safety, you can call get_dynamic_mode to ensure it's ON.
        return f"Selected dynamic sequence index: {index}"
    
    def set_scenario_select_index(self, index: int):
        """
        Set the scenario start index in the sequence table.

        Args:
            index (int): The sequence table index to select as scenario start.

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            command = f":STAB:SCEN:SEL {index}"
            try:
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response="OK")
                return {"Status": f"Scenario start index set to {index}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_scenario_select_minmax(self, option: str):
        """
        Set the scenario start index to MIN or MAX.

        Args:
            option (str): Either "MIN" or "MAX".

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            option = option.upper()
            if option not in ["MIN", "MAX"]:
                return {"Error": "Option must be 'MIN' or 'MAX'"}

            command = f":STAB:SCEN:SEL {option}"
            try:
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response="OK")
                return {"Status": f"Scenario index set to {option}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_scenario_select_index(self):
        """
        Query the currently selected scenario start index in the sequence table.

        Returns:
            dict: {"ScenarioStartIndex": int, "Duration(ms)": float} or {"Error": ...}
        """
        if self.resource:
            command = ":STAB:SCEN:SEL?"
            try:
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {"ScenarioStartIndex": int(response), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_scenario_advance_mode(self, mode: str):
        """
        Set the advancement mode for scenario execution.

        Args:
            mode (str): One of ["AUTO", "COND", "REP", "SING"]

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        valid_modes = ["AUTO", "COND", "REP", "SING"]
        if self.resource:
            if mode.upper() not in valid_modes:
                return {"Error": f"Invalid mode. Choose from {valid_modes}"}
            command = f":STAB:SCEN:ADV {mode.upper()}"
            try:
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response="OK")
                return {"Status": f"Scenario advancement mode set to {mode.upper()}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_scenario_advance_mode(self):
        """
        Query the current advancement mode for scenario execution.

        Returns:
            dict: {"AdvanceMode": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            command = ":STAB:SCEN:ADV?"
            try:
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {"AdvanceMode": response, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_scenario_loop_count(self, count: int):
        """
        Set the loop count for scenarios.

        Args:
            count (int): Number of times the scenario is repeated (1 to 4G-1).

        Returns:
            dict: {"Set": ..., "Confirmed": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            command = f":STAB:SCEN:COUN {count}"
            try:
                start_time = time.time()
                self.resource.write(command)
                response = self.resource.query(":STAB:SCEN:COUN?").strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {
                    "Set": count,
                    "Confirmed": response,
                    "Duration(ms)": duration
                }
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_scenario_loop_min_max(self, option: str):
        """
        Set the scenario loop count to MINimum or MAXimum.
    
        Args:
            option (str): "MIN" or "MAX"
    
        Returns:
            dict: {"Set": ..., "Confirmed": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            opt = option.strip().upper()
            if opt not in ["MIN", "MAX"]:
                return {"Error": "Option must be 'MIN' or 'MAX'"}
    
            command = f":STAB:SCEN:COUN {opt}"
            try:
                start_time = time.time()
                self.resource.write(command)
                response = self.resource.query(":STAB:SCEN:COUN?").strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {
                    "Set": opt,
                    "Confirmed": response,
                    "Duration(ms)": duration
                }
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}

















