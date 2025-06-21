#import awg modules
from AWGConnection import AWG_connection
from logger import awg_logger

#import other modules
import time

class AWG_Function_Mode:
    def __init__(self, ip_address):
        self.ip_address = ip_address

        #create insatces for connection and logger classes
        self.connection = AWG_connection(ip_address)
        self.log = awg_logger()

        #select the recourse from connection class
        self.resource = self.connection.get_resource()

    def set_function_mode(self, mode: str):
        """
        Set the function mode for channels using extended memory.

        Args:
            mode (str): 'ARBitrary', 'STSequence', or 'STSCenario'

        Returns:
            dict: Actual queried mode and execution duration, or error.
        """
        valid_modes = ["ARB", "STS", "STSC"]
        mode = mode.upper()        

        if mode not in valid_modes:
            return {"Error": f"Invalid mode. Use one of: {valid_modes}"}

        if self.resource:
            try:
                command = f":FUNC:MODE {mode}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                response = self.get_function_mode()
                self.log._log_command(command, duration_ms=duration, response=str(response))
                return {**response, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}

        return {"Error": "Device not connected"}
    
    def get_function_mode(self):
        """
        Query the current function mode for channels using extended memory.
    
        Returns:
            dict: Current mode or error message.
        """
        if self.resource:
            try:
                command = ":FUNC:MODE?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000
                mode = response.strip()
    
                self.log._log_command(command, duration_ms=duration, response=mode)
                return {"Function Mode": mode}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
