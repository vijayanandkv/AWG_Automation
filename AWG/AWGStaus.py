#import the required AWG modules
from VISAInterface import pyvisa_interface
from AWGConnection import AWG_connection
from logger import awg_logger

import time



class AWG_system_status:
    def __init__(self, ip_address: str):
        self.ip_address = ip_address

        #create insatces for connection and logger classes
        self.connection = AWG_connection(ip_address)
        self.log = awg_logger()

        #select the recourse from connection class
        self.resource = self.connection.get_resource()

    def preset_status_registers(self):
        """
        Clears all status group event registers and presets the PTR and NTR registers.
        Sets: ENABle = 0x0000, PTR = 0xffff, NTR = 0x0000
        """
        if self.resource is not None:
            try:
                start_time = time.time()
                self.resource.write(":STAT:PRESet")
                duration = (time.time() - start_time) * 1000
                self.log._log_command(":STAT:PRESet", duration_ms=duration, response="Status registers preset successfully.")
                return {"Status": "Preset successful", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:PRESet", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:PRESet", duration_ms=0, response="Resource not connected")
            return {"Error": "Device not connected"}
        
    def query_status_byte_register(self):
        """
        Query the Status Byte Register using *STB? and log the response.
        Returns a decimal integer representing the current status.
        """
        if self.resource is not None:
            try:
                start_time = time.time()
                status_value = self.resource.query("*STB?")
                duration = (time.time() - start_time) * 1000
                self.log._log_command("*STB?", duration_ms=duration, response=status_value.strip())
                return {"StatusByte": int(status_value.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command("*STB?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command("*STB?", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}
        
    def query_questionable_event_status(self):
        """
        Query the questionable status event register using :STAT:QUES:EVENt?
        Returns a dictionary with the status code and duration.
        """
        if self.resource is not None:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:QUES:EVENt?")
                duration = (time.time() - start_time) * 1000
                self.log._log_command(":STAT:QUES:EVENt?", duration_ms=duration, response=response.strip())
                return {"QuestionableEventStatus": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:EVENt?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:QUES:EVENt?", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}

    def get_questionable_condition(self):
        """
        Query the real-time status of the Questionable Condition Register.
        Returns a decimal value where each bit represents a different condition.
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:QUES:COND?")
                duration = (time.time() - start_time) * 1000  # in milliseconds

                self.log._log_command(
                    command=":STAT:QUES:COND?",
                    duration_ms=duration,
                    response=response.strip()
                )
                return int(response.strip())
            except Exception as e:
                self.log._log_command(
                    command=":STAT:QUES:COND?",
                    duration_ms=0,
                    response=str(e)
                )
                return f"Error: {str(e)}"
        else:
            return "Error: No connected resource"
        
    def set_questionable_enable(self, value: int):
        """
        Set the enable register in the Questionable Status group.
        Accepts a decimal value (0–255) representing which bits to enable.
        """
        if not (0 <= value <= 255):
            return "Error: Value must be between 0 and 255."

        if self.resource:
            try:
                start_time = time.time()
                self.resource.write(f":STAT:QUES:ENAB {value}")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(
                    command=f":STAT:QUES:ENAB {value}",
                    duration_ms=duration,
                    response="Enable bits set"
                )
                return f"Questionable enable register set to {value}"
            except Exception as e:
                self.log._log_command(
                    command=f":STAT:QUES:ENAB {value}",
                    duration_ms=0,
                    response=str(e)
                )
                return f"Error: {str(e)}"
        else:
            return "Error: No connected resource"
        
    def get_questionable_enable(self):
        """
        Query the enable register in the Questionable Status group.
        Returns a decimal value representing enabled bits.
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:QUES:ENAB?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(
                    command=":STAT:QUES:ENAB?",
                    duration_ms=duration,
                    response=response.strip()
                )
                return int(response.strip())
            except Exception as e:
                self.log._log_command(
                    command=":STAT:QUES:ENAB?",
                    duration_ms=0,
                    response=str(e)
                )
                return f"Error: {str(e)}"
        else:
            return "Error: No connected resource"
        
    def get_questionable_ntransition(self):
        """
        Query the negative-transition register in the Questionable Status group.
        Returns a decimal value indicating which bits are monitored for false transitions.
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:QUES:NTR?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(
                    command=":STAT:QUES:NTR?",
                    duration_ms=duration,
                    response=response.strip()
                )
                return int(response.strip())
            except Exception as e:
                self.log._log_command(
                    command=":STAT:QUES:NTR?",
                    duration_ms=0,
                    response=str(e)
                )
                return f"Error: {str(e)}"
        else:
            return "Error: No connected resource"
        
    def set_questionable_ntransition(self, value: int):
        """
        Set the negative-transition register in the Questionable Status group.
        Value must be between 0 and 65535.
        """
        if not (0 <= value <= 65535):
            return "Error: Value must be between 0 and 65535."

        if self.resource:
            try:
                start_time = time.time()
                self.resource.write(f":STAT:QUES:NTR {value}")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(
                    command=f":STAT:QUES:NTR {value}",
                    duration_ms=duration,
                    response="Negative-transition register updated"
                )
                return f"NTR set to {value}"
            except Exception as e:
                self.log._log_command(
                    command=f":STAT:QUES:NTR {value}",
                    duration_ms=0,
                    response=str(e)
                )
                return f"Error: {str(e)}"
        else:
            return "Error: No connected resource"
        
    def questionable_positive_transition(self, value: int = None):
        """
        Set or query the positive-transition register in the questionable status group.
        - If `value` is provided, sets the register to that value.
        - If no value is provided, queries and returns the current register value.

        A positive transition filter allows events to be reported when a condition changes
        from False to True. Value should be in the range 0–65535.
        """
        try:
            if self.resource is None:
                raise ConnectionError("Device not connected.")

            if value is not None:
                if not (0 <= value <= 65535):
                    raise ValueError("Value must be between 0 and 65535.")
                start = time.time()
                self.resource.write(f":STAT:QUES:PTR {value}")
                duration = (time.time() - start) * 1000
                self.log._log_command(":STAT:QUES:PTR", duration_ms=duration, response=f"Set to {value}")
                return {"Set": value, "Duration(ms)": duration}
            else:
                start = time.time()
                response = self.resource.query(":STAT:QUES:PTR?")
                duration = (time.time() - start) * 1000
                self.log._log_command(":STAT:QUES:PTR?", duration_ms=duration, response=response.strip())
                return {"PTR_Value": int(response.strip()), "Duration(ms)": duration}

        except Exception as e:
            self.log._log_command(":STAT:QUES:PTR or :STAT:QUES:PTR?", duration_ms=0, response=str(e))
            return {"Error": str(e)}

    ################################## OPERATION STATUS SUBSYSTEM############################################

    def query_operation_event_status(self):
        """
        Query the event register in the Operation Status group using :STAT:OPER:EVEN?.

        This register is read-only and latches status bits when the associated condition changes from false to true.
        The register is cleared after reading or by *CLS.

        """
        if self.resource is not None:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:OPER:EVEN?")
                duration = (time.time() - start_time) * 1000  # in milliseconds

                self.log._log_command(
                    command=":STAT:OPER:EVEN?",
                    duration_ms=duration,
                    response=response.strip()
                )
                return {"OperationEventStatus": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(
                    command=":STAT:OPER:EVEN?",
                    duration_ms=0,
                    response=str(e)
                )
                return {"Error": str(e)}
        else:
            self.log._log_command(
                command=":STAT:OPER:EVEN?",
                duration_ms=0,
                response="Device not connected"
            )
            return {"Error": "Device not connected"}

    def get_operation_condition(self):
        """
        Query the condition register in the Operation Status group using :STAT:OPER:COND?.

        This register reflects the current real-time status of conditions in the operation group.
        It is read-only and not cleared by reading.

        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:OPER:COND?")
                duration = (time.time() - start_time) * 1000  # in milliseconds

                self.log._log_command(
                    command=":STAT:OPER:COND?",
                    duration_ms=duration,
                    response=response.strip()
                )
                return {"OperationCondition": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(
                    command=":STAT:OPER:COND?",
                    duration_ms=0,
                    response=str(e)
                )
                return {"Error": str(e)}
        else:
            self.log._log_command(
                command=":STAT:OPER:COND?",
                duration_ms=0,
                response="Device not connected"
            )
            return {"Error": "Device not connected"}
        
    def set_operation_enable(self, value: int):
        """
        Set the enable register in the Operation Status group using :STAT:OPER:ENAB.

        Args:
            value (int): Decimal value (0–65535) corresponding to bits to enable.

        Notes:
            - This register determines which operation status bits are reported to the Status Byte.
            - *CLS does NOT clear this register (only clears the event register).
        """
        if not (0 <= value <= 65535):
            return {"Error": "Value must be between 0 and 65535."}

        if self.resource:
            try:
                start_time = time.time()
                self.resource.write(f":STAT:OPER:ENAB {value}")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(
                    command=f":STAT:OPER:ENAB {value}",
                    duration_ms=duration,
                    response="Enable bits set"
                )
                return {"SetEnableValue": value, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(
                    command=f":STAT:OPER:ENAB {value}",
                    duration_ms=0,
                    response=str(e)
                )
                return {"Error": str(e)}
        else:
            self.log._log_command(
                command=f":STAT:OPER:ENAB {value}",
                duration_ms=0,
                response="Device not connected"
            )
            return {"Error": "Device not connected"}

    def get_operation_enable(self):
        """
        Query the enable register in the Operation Status group using :STAT:OPER:ENAB?.

        Returns:
            dict:
                - On success: {"OperationEnable": <value>, "Duration(ms)": <duration>}
                - On error  : {"Error": "<error message>"}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:OPER:ENAB?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(
                    command=":STAT:OPER:ENAB?",
                    duration_ms=duration,
                    response=response.strip()
                )
                return {"OperationEnable": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(
                    command=":STAT:OPER:ENAB?",
                    duration_ms=0,
                    response=str(e)
                )
                return {"Error": str(e)}
        else:
            self.log._log_command(
                command=":STAT:OPER:ENAB?",
                duration_ms=0,
                response="Device not connected"
            )
            return {"Error": "Device not connected"}
        
    def set_operation_negative_transition(self, value: int):
        """
        Set the negative-transition register in the Operation Status group.

        Args:
            value (int): A 16-bit integer (0 to 65535) to set the NTR register.

        """
        if not (0 <= value <= 65535):
            return {"Error": "Value must be between 0 and 65535."}

        if self.resource:
            try:
                start_time = time.time()
                self.resource.write(f":STAT:OPER:NTR {value}")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:OPER:NTR", duration_ms=duration, response=f"Set to {value}")
                return {"Set": value, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:OPER:NTR", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:OPER:NTR", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}
        
    def get_operation_negative_transition(self):
        """
        Query the negative-transition register in the Operation Status group.

        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:OPER:NTR?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:OPER:NTR?", duration_ms=duration, response=response.strip())
                return {"NTR_Value": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:OPER:NTR?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:OPER:NTR?", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}
        

    def set_operation_positive_transition(self, value: int):
        """
        Set the positive-transition register in the Operation Status group.

        Args:
            value (int): A 16-bit integer (0 to 65535) to set the PTR register.

        Notes:
            - Reports events when a condition changes from False to True.
            - Not cleared by *CLS or *RST.
        """
        if not (0 <= value <= 65535):
            return {"Error": "Value must be between 0 and 65535."}

        if self.resource:
            try:
                start_time = time.time()
                self.resource.write(f":STAT:OPER:PTR {value}")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(
                    command=":STAT:OPER:PTR",
                    duration_ms=duration,
                    response=f"Set to {value}"
                )
                return {"Set": value, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:OPER:PTR", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:OPER:PTR", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}
        
    def get_operation_positive_transition(self):
        """
        Query the positive-transition register in the Operation Status group.

        Notes:
            - Reports events when a condition changes from False to True.
            - Not cleared by *CLS or *RST.
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:OPER:PTR?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(
                    command=":STAT:OPER:PTR?",
                    duration_ms=duration,
                    response=response.strip()
                )
                return {"PTR_Value": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:OPER:PTR?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:OPER:PTR?", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}

    ####################################  VOLTAGE STATUS SUBSYSTEM  ###########################################

    def get_voltage_event_status(self):
        """
        Query the Voltage Event Register in the Questionable Status group.

        Returns:
            dict: {"VoltageEventStatus": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:QUES:VOLT:EVEN?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:VOLT:EVEN?", duration_ms=duration, response=response.strip())
                return {"VoltageEventStatus": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:VOLT:EVEN?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:QUES:VOLT:EVEN?", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}
        
    def get_voltage_condition(self):
        """
        Query the real-time Voltage Condition Register in the Questionable Status group.

        Returns:
            dict: {"VoltageCondition": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:QUES:VOLT:COND?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:VOLT:COND?", duration_ms=duration, response=response.strip())
                return {"VoltageCondition": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:VOLT:COND?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:QUES:VOLT:COND?", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}
        
    def set_voltage_enable(self, value: int):
        """
        Set the Voltage Enable Register in the Questionable Status group.

        Args:
            value (int): 0–65535

        Returns:
            dict: {"Set": value, "Duration(ms)": duration} or {"Error": message}
        """
        if not (0 <= value <= 65535):
            return {"Error": "Value must be between 0 and 65535."}

        if self.resource:
            try:
                start_time = time.time()
                self.resource.write(f":STAT:QUES:VOLT:ENAB {value}")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:VOLT:ENAB", duration_ms=duration, response=f"Set to {value}")
                return {"Set": value, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:VOLT:ENAB", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:QUES:VOLT:ENAB", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}

    def get_voltage_enable(self):
        """
        Query the Voltage Enable Register in the Questionable Status group.

        Returns:
            dict: {"VoltageEnable": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:QUES:VOLT:ENAB?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:VOLT:ENAB?", duration_ms=duration, response=response.strip())
                return {"VoltageEnable": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:VOLT:ENAB?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:QUES:VOLT:ENAB?", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}


    def set_voltage_ntransition(self, value: int):
        """
        Set the Voltage Negative-Transition Register in the Questionable Status group.

        Returns:
            dict: {"Set": value, "Duration(ms)": duration} or {"Error": message}
        """
        if not (0 <= value <= 65535):
            return {"Error": "Value must be between 0 and 65535."}

        if self.resource:
            try:
                start_time = time.time()
                self.resource.write(f":STAT:QUES:VOLT:NTR {value}")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:VOLT:NTR", duration_ms=duration, response=f"Set to {value}")
                return {"Set": value, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:VOLT:NTR", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:QUES:VOLT:NTR", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}

    def get_voltage_ntransition(self):
        """
        Query the Voltage Negative-Transition Register in the Questionable Status group.

        Returns:
            dict: {"NTR_Value": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:QUES:VOLT:NTR?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:VOLT:NTR?", duration_ms=duration, response=response.strip())
                return {"NTR_Value": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:VOLT:NTR?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:QUES:VOLT:NTR?", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}
        
    def set_voltage_ptransition(self, value: int):
        """
        Set the Voltage Positive-Transition Register in the Questionable Status group.

        Returns:
            dict: {"Set": value, "Duration(ms)": duration} or {"Error": message}
        """
        if not (0 <= value <= 65535):
            return {"Error": "Value must be between 0 and 65535."}

        if self.resource:
            try:
                start_time = time.time()
                self.resource.write(f":STAT:QUES:VOLT:PTR {value}")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:VOLT:PTR", duration_ms=duration, response=f"Set to {value}")
                return {"Set": value, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:VOLT:PTR", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:QUES:VOLT:PTR", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}

    def get_voltage_ptransition(self):
        """
        Query the Voltage Positive-Transition Register in the Questionable Status group.

        Returns:
            dict: {"PTR_Value": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:QUES:VOLT:PTR?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:VOLT:PTR?", duration_ms=duration, response=response.strip())
                return {"PTR_Value": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:VOLT:PTR?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:QUES:VOLT:PTR?", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}
        
    ############################################## FREQUENCY STATUS SUBSYSTEM #############################################

    def get_frequency_event_status(self):
        """
        Query the Frequency Event Register in the Questionable Status group.

        Returns:
            dict: {"FrequencyEventStatus": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:QUES:FREQ:EVEN?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:FREQ:EVEN?", duration_ms=duration, response=response.strip())
                return {"FrequencyEventStatus": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:FREQ:EVEN?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:QUES:FREQ:EVEN?", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}
        
    def get_frequency_condition(self):
        """
        Query the real-time Frequency Condition Register in the Questionable Status group.

        Returns:
            dict: {"FrequencyCondition": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:QUES:FREQ:COND?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:FREQ:COND?", duration_ms=duration, response=response.strip())
                return {"FrequencyCondition": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:FREQ:COND?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:QUES:FREQ:COND?", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}
        
    def set_frequency_enable(self, value: int):
        """
        Set the Frequency Enable Register in the Questionable Status group.

        Args:
            value (int): Value between 0 and 65535

        Returns:
            dict: {"Set": value, "Duration(ms)": duration} or {"Error": message}
        """
        if not (0 <= value <= 65535):
            return {"Error": "Value must be between 0 and 65535."}

        if self.resource:
            try:
                start_time = time.time()
                self.resource.write(f":STAT:QUES:FREQ:ENAB {value}")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:FREQ:ENAB", duration_ms=duration, response=f"Set to {value}")
                return {"Set": value, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:FREQ:ENAB", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:QUES:FREQ:ENAB", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}

    def get_frequency_enable(self):
        """
        Query the Frequency Enable Register in the Questionable Status group.

        Returns:
            dict: {"FrequencyEnable": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:QUES:FREQ:ENAB?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:FREQ:ENAB?", duration_ms=duration, response=response.strip())
                return {"FrequencyEnable": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:FREQ:ENAB?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:QUES:FREQ:ENAB?", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}
        
    def set_frequency_ntransition(self, value: int):
        """
        Set the Frequency Negative-Transition Register in the Questionable Status group.

        Returns:
            dict: {"Set": value, "Duration(ms)": duration} or {"Error": message}
        """
        if not (0 <= value <= 65535):
            return {"Error": "Value must be between 0 and 65535."}

        if self.resource:
            try:
                start_time = time.time()
                self.resource.write(f":STAT:QUES:FREQ:NTR {value}")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:FREQ:NTR", duration_ms=duration, response=f"Set to {value}")
                return {"Set": value, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:FREQ:NTR", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:QUES:FREQ:NTR", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}

    def get_frequency_ntransition(self):
        """
        Query the Frequency Negative-Transition Register in the Questionable Status group.

        Returns:
            dict: {"NTR_Value": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:QUES:FREQ:NTR?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:FREQ:NTR?", duration_ms=duration, response=response.strip())
                return {"NTR_Value": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:FREQ:NTR?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:QUES:FREQ:NTR?", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}
        
    def set_frequency_ptransition(self, value: int):
        """
        Set the Frequency Positive-Transition Register in the Questionable Status group.

        Returns:
            dict: {"Set": value, "Duration(ms)": duration} or {"Error": message}
        """
        if not (0 <= value <= 65535):
            return {"Error": "Value must be between 0 and 65535."}

        if self.resource:
            try:
                start_time = time.time()
                self.resource.write(f":STAT:QUES:FREQ:PTR {value}")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:FREQ:PTR", duration_ms=duration, response=f"Set to {value}")
                return {"Set": value, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:FREQ:PTR", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:QUES:FREQ:PTR", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}

    def get_frequency_ptransition(self):
        """
        Query the Frequency Positive-Transition Register in the Questionable Status group.

        Returns:
            dict: {"PTR_Value": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:QUES:FREQ:PTR?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:FREQ:PTR?", duration_ms=duration, response=response.strip())
                return {"PTR_Value": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:FREQ:PTR?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:QUES:FREQ:PTR?", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}
        
    ##################################### SEQUENCE STATUS SUBSYSTEM #####################################################

    def get_sequence_event_status(self):
        """
        Query the Sequence Event Register in the Questionable Status group.

        Returns:
            dict: {"SequenceEventStatus": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:QUES:SEQ:EVEN?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:SEQ:EVEN?", duration_ms=duration, response=response.strip())
                return {"SequenceEventStatus": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:SEQ:EVEN?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:QUES:SEQ:EVEN?", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}
        

    def get_sequence_condition(self):
        """
        Query the Sequence Condition Register in the Questionable Status group.

        Returns:
            dict: {"SequenceCondition": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:QUES:SEQ:COND?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:SEQ:COND?", duration_ms=duration, response=response.strip())
                return {"SequenceCondition": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:SEQ:COND?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:QUES:SEQ:COND?", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}
        
    def set_sequence_enable(self, value: int):
        """
        Set the Sequence Enable Register in the Questionable Status group.

        Args:
            value (int): Value between 0 and 65535

        Returns:
            dict: {"Set": value, "Duration(ms)": duration} or {"Error": message}
        """
        if not (0 <= value <= 65535):
            return {"Error": "Value must be between 0 and 65535."}

        if self.resource:
            try:
                start_time = time.time()
                self.resource.write(f":STAT:QUES:SEQ:ENAB {value}")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:SEQ:ENAB", duration_ms=duration, response=f"Set to {value}")
                return {"Set": value, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:SEQ:ENAB", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:QUES:SEQ:ENAB", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}

    def get_sequence_enable(self):
        """
        Query the Sequence Enable Register in the Questionable Status group.

        Returns:
            dict: {"SequenceEnable": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:QUES:SEQ:ENAB?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:SEQ:ENAB?", duration_ms=duration, response=response.strip())
                return {"SequenceEnable": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:SEQ:ENAB?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:QUES:SEQ:ENAB?", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}
        
    def set_sequence_ntransition(self, value: int):
        """
        Set the Sequence Negative-Transition Register in the Questionable Status group.

        Returns:
            dict: {"Set": value, "Duration(ms)": duration} or {"Error": message}
        """
        if not (0 <= value <= 65535):
            return {"Error": "Value must be between 0 and 65535."}

        if self.resource:
            try:
                start_time = time.time()
                self.resource.write(f":STAT:QUES:SEQ:NTR {value}")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:SEQ:NTR", duration_ms=duration, response=f"Set to {value}")
                return {"Set": value, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:SEQ:NTR", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:QUES:SEQ:NTR", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}

    def get_sequence_ntransition(self):
        """
        Query the Sequence Negative-Transition Register in the Questionable Status group.

        Returns:
            dict: {"NTR_Value": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:QUES:SEQ:NTR?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:SEQ:NTR?", duration_ms=duration, response=response.strip())
                return {"NTR_Value": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:SEQ:NTR?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:QUES:SEQ:NTR?", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}
        
    def set_sequence_ptransition(self, value: int):
        """
        Set the Sequence Positive-Transition Register in the Questionable Status group.

        Returns:
            dict: {"Set": value, "Duration(ms)": duration} or {"Error": message}
        """
        if not (0 <= value <= 65535):
            return {"Error": "Value must be between 0 and 65535."}

        if self.resource:
            try:
                start_time = time.time()
                self.resource.write(f":STAT:QUES:SEQ:PTR {value}")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:SEQ:PTR", duration_ms=duration, response=f"Set to {value}")
                return {"Set": value, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:SEQ:PTR", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:QUES:SEQ:PTR", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}

    def get_sequence_ptransition(self):
        """
        Query the Sequence Positive-Transition Register in the Questionable Status group.

        Returns:
            dict: {"PTR_Value": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:QUES:SEQ:PTR?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:SEQ:PTR?", duration_ms=duration, response=response.strip())
                return {"PTR_Value": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:SEQ:PTR?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            self.log._log_command(":STAT:QUES:SEQ:PTR?", duration_ms=0, response="Device not connected")
            return {"Error": "Device not connected"}
        
    ######################################## DUS STATUS SUBSYSTEM ##############################################

    def get_duc_event_status(self):
        """
        Query the DUC Event Register in the Questionable Status group.

        Returns:
            dict: {"DUCEventStatus": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:QUES:DUC:EVEN?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:DUC:EVEN?", duration_ms=duration, response=response.strip())
                return {"DUCEventStatus": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:DUC:EVEN?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            return {"Error": "Device not connected"}
    def get_duc_condition(self):
        """
        Query the DUC Condition Register in the Questionable Status group.

        Returns:
            dict: {"DUCCondition": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:QUES:DUC:COND?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:DUC:COND?", duration_ms=duration, response=response.strip())
                return {"DUCCondition": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:DUC:COND?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            return {"Error": "Device not connected"}
        
    def set_duc_enable(self, value: int):
        """
        Set the DUC Enable Register in the Questionable Status group.

        Args:
            value (int): Value between 0 and 65535

        Returns:
            dict: {"Set": value, "Duration(ms)": duration} or {"Error": message}
        """
        if not (0 <= value <= 65535):
            return {"Error": "Value must be between 0 and 65535."}

        if self.resource:
            try:
                start_time = time.time()
                self.resource.write(f":STAT:QUES:DUC:ENAB {value}")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:DUC:ENAB", duration_ms=duration, response=f"Set to {value}")
                return {"Set": value, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:DUC:ENAB", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            return {"Error": "Device not connected"}

    def get_duc_enable(self):
        """
        Query the DUC Enable Register in the Questionable Status group.

        Returns:
            dict: {"DUCEnable": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:QUES:DUC:ENAB?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:DUC:ENAB?", duration_ms=duration, response=response.strip())
                return {"DUCEnable": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:DUC:ENAB?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            return {"Error": "Device not connected"}
        
    def set_duc_ntransition(self, value: int):
        """
        Set the DUC Negative-Transition Register in the Questionable Status group.

        Returns:
            dict: {"Set": value, "Duration(ms)": duration} or {"Error": message}
        """
        if not (0 <= value <= 65535):
            return {"Error": "Value must be between 0 and 65535."}

        if self.resource:
            try:
                start_time = time.time()
                self.resource.write(f":STAT:QUES:DUC:NTR {value}")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:DUC:NTR", duration_ms=duration, response=f"Set to {value}")
                return {"Set": value, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:DUC:NTR", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            return {"Error": "Device not connected"}

    def get_duc_ntransition(self):
        """
        Query the DUC Negative-Transition Register in the Questionable Status group.

        Returns:
            dict: {"NTR_Value": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:QUES:DUC:NTR?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:DUC:NTR?", duration_ms=duration, response=response.strip())
                return {"NTR_Value": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:DUC:NTR?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            return {"Error": "Device not connected"}
        
    def set_duc_ptransition(self, value: int):
        """
        Set the DUC Positive-Transition Register in the Questionable Status group.

        Returns:
            dict: {"Set": value, "Duration(ms)": duration} or {"Error": message}
        """
        if not (0 <= value <= 65535):
            return {"Error": "Value must be between 0 and 65535."}

        if self.resource:
            try:
                start_time = time.time()
                self.resource.write(f":STAT:QUES:DUC:PTR {value}")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:DUC:PTR", duration_ms=duration, response=f"Set to {value}")
                return {"Set": value, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:DUC:PTR", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            return {"Error": "Device not connected"}

    def get_duc_ptransition(self):
        """
        Query the DUC Positive-Transition Register in the Questionable Status group.

        Returns:
            dict: {"PTR_Value": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:QUES:DUC:PTR?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:DUC:PTR?", duration_ms=duration, response=response.strip())
                return {"PTR_Value": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:DUC:PTR?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        else:
            return {"Error": "Device not connected"}
        
    ################################# CONNECTION STATUS SUBSYSTEM ############################################
    def get_connection_event_status(self):
        """
        Query the Connection Event Register in the Questionable Status group.

        Returns:
            dict: {"ConnectionEventStatus": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:QUES:CONN:EVEN?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:CONN:EVEN?", duration_ms=duration, response=response.strip())
                return {"ConnectionEventStatus": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:CONN:EVEN?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_connection_condition(self):
        """
        Query the Connection Condition Register in the Questionable Status group.

        Returns:
            dict: {"ConnectionCondition": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:QUES:CONN:COND?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:CONN:COND?", duration_ms=duration, response=response.strip())
                return {"ConnectionCondition": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:CONN:COND?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_connection_enable(self, value: int):
        """
        Set the Connection Enable Register in the Questionable Status group.

        Args:
            value (int): Value between 0 and 65535

        Returns:
            dict: {"Set": value, "Duration(ms)": duration} or {"Error": message}
        """
        if not (0 <= value <= 65535):
            return {"Error": "Value must be between 0 and 65535."}

        if self.resource:
            try:
                start_time = time.time()
                self.resource.write(f":STAT:QUES:CONN:ENAB {value}")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:CONN:ENAB", duration_ms=duration, response=f"Set to {value}")
                return {"Set": value, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:CONN:ENAB", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}

    def get_connection_enable(self):
        """
        Query the Connection Enable Register in the Questionable Status group.

        Returns:
            dict: {"ConnectionEnable": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:QUES:CONN:ENAB?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:CONN:ENAB?", duration_ms=duration, response=response.strip())
                return {"ConnectionEnable": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:CONN:ENAB?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_connection_ntransition(self, value: int):
        """
        Set the Connection Negative-Transition Register in the Questionable Status group.

        Returns:
            dict: {"Set": value, "Duration(ms)": duration} or {"Error": message}
        """
        if not (0 <= value <= 65535):
            return {"Error": "Value must be between 0 and 65535."}

        if self.resource:
            try:
                start_time = time.time()
                self.resource.write(f":STAT:QUES:CONN:NTR {value}")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:CONN:NTR", duration_ms=duration, response=f"Set to {value}")
                return {"Set": value, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:CONN:NTR", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}

    def get_connection_ntransition(self):
        """
        Query the Connection Negative-Transition Register in the Questionable Status group.

        Returns:
            dict: {"NTR_Value": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:QUES:CONN:NTR?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:CONN:NTR?", duration_ms=duration, response=response.strip())
                return {"NTR_Value": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:CONN:NTR?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}

    def set_connection_ptransition(self, value: int):
        """
        Set the Connection Positive-Transition Register in the Questionable Status group.

        Returns:
            dict: {"Set": value, "Duration(ms)": duration} or {"Error": message}
        """
        if not (0 <= value <= 65535):
            return {"Error": "Value must be between 0 and 65535."}

        if self.resource:
            try:
                start_time = time.time()
                self.resource.write(f":STAT:QUES:CONN:PTR {value}")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:CONN:PTR", duration_ms=duration, response=f"Set to {value}")
                return {"Set": value, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:CONN:PTR", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}

    def get_connection_ptransition(self):
        """
        Query the Connection Positive-Transition Register in the Questionable Status group.

        Returns:
            dict: {"PTR_Value": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:QUES:CONN:PTR?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:QUES:CONN:PTR?", duration_ms=duration, response=response.strip())
                return {"PTR_Value": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:QUES:CONN:PTR?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}

    ################################# RUN STATUS SUBSYSTEM ###################################################

    def get_run_event_status(self):
        """
        Query the Run Event Register in the Operation Status group.

        Returns:
            dict: {"RunEventStatus": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:OPER:RUN:EVEN?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:OPER:RUN:EVEN?", duration_ms=duration, response=response.strip())
                return {"RunEventStatus": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:OPER:RUN:EVEN?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_run_condition(self):
        """
        Query the Run Condition Register in the Operation Status group.

        Returns:
            dict: {"RunCondition": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:OPER:RUN:COND?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:OPER:RUN:COND?", duration_ms=duration, response=response.strip())
                return {"RunCondition": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:OPER:RUN:COND?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_run_enable(self, value: int):
        """
        Set the Run Enable Register in the Operation Status group.

        Args:
            value (int): Value between 0 and 65535

        Returns:
            dict: {"Set": value, "Duration(ms)": duration} or {"Error": message}
        """
        if not (0 <= value <= 65535):
            return {"Error": "Value must be between 0 and 65535."}

        if self.resource:
            try:
                start_time = time.time()
                self.resource.write(f":STAT:OPER:RUN:ENAB {value}")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:OPER:RUN:ENAB", duration_ms=duration, response=f"Set to {value}")
                return {"Set": value, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:OPER:RUN:ENAB", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}

    def get_run_enable(self):
        """
        Query the Run Enable Register in the Operation Status group.

        Returns:
            dict: {"RunEnable": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:OPER:RUN:ENAB?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:OPER:RUN:ENAB?", duration_ms=duration, response=response.strip())
                return {"RunEnable": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:OPER:RUN:ENAB?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_run_ntransition(self, value: int):
        """
        Set the Run Negative-Transition Register in the Operation Status group.

        Returns:
            dict: {"Set": value, "Duration(ms)": duration} or {"Error": message}
        """
        if not (0 <= value <= 65535):
            return {"Error": "Value must be between 0 and 65535."}

        if self.resource:
            try:
                start_time = time.time()
                self.resource.write(f":STAT:OPER:RUN:NTR {value}")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:OPER:RUN:NTR", duration_ms=duration, response=f"Set to {value}")
                return {"Set": value, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:OPER:RUN:NTR", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}

    def get_run_ntransition(self):
        """
        Query the Run Negative-Transition Register in the Operation Status group.

        Returns:
            dict: {"NTR_Value": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:OPER:RUN:NTR?")
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":STAT:OPER:RUN:NTR?", duration_ms=duration, response=response.strip())
                return {"NTR_Value": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:OPER:RUN:NTR?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_run_ptransition(self, value: int):
        """
        Set the Run Positive-Transition Register in the Operation Status group.
    
        Returns:
            dict: {"Set": value, "Duration(ms)": duration} or {"Error": message}
        """
        if not (0 <= value <= 65535):
            return {"Error": "Value must be between 0 and 65535."}
    
        if self.resource:
            try:
                start_time = time.time()
                self.resource.write(f":STAT:OPER:RUN:PTR {value}")
                duration = (time.time() - start_time) * 1000
    
                self.log._log_command(":STAT:OPER:RUN:PTR", duration_ms=duration, response=f"Set to {value}")
                return {"Set": value, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:OPER:RUN:PTR", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_run_ptransition(self):
        """
        Query the Run Positive-Transition Register in the Operation Status group.
    
        Returns:
            dict: {"PTR_Value": value, "Duration(ms)": duration} or {"Error": message}
        """
        if self.resource:
            try:
                start_time = time.time()
                response = self.resource.query(":STAT:OPER:RUN:PTR?")
                duration = (time.time() - start_time) * 1000
    
                self.log._log_command(":STAT:OPER:RUN:PTR?", duration_ms=duration, response=response.strip())
                return {"PTR_Value": int(response.strip()), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":STAT:OPER:RUN:PTR?", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    
    






























