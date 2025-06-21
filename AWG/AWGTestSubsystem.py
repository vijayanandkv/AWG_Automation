#import awg modules
from AWGConnection import AWG_connection
from logger import awg_logger

#import other modules
import time

class AWG_test:
    def __init__(self, ip_address):
        self.ip_address = ip_address

        #create insatces for connection and logger classes
        self.connection = AWG_connection(ip_address)
        self.log = awg_logger()

        #select the recourse from connection class
        self.resource = self.connection.get_resource()

    def get_power_on_self_test_results(self):
        """
        Query the results of the Power-On Self-Test (POST).

        Returns:
            dict: {"POST Result": result, "Duration(ms)": duration} or error message
        """
        if self.resource:
            try:
                command = ":TEST:PON?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000

                self.log._log_command(command, duration_ms=duration, response=response.strip())
                return {"POST Result": response.strip(), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, 0, str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_detailed_self_test_messages(self):
        """
        Query detailed self-test messages (same as *TST? but returns actual test messages).
    
        Returns:
            dict: {"Self-Test Messages": messages, "Duration(ms)": duration} or error message
        """
        if self.resource:
            try:
                command = ":TEST:TST?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000
    
                self.log._log_command(command, duration_ms=duration, response=response.strip())
                return {"Self-Test Messages": response.strip(), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, 0, str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}


