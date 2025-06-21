#import awg modules
from AWGConnection import AWG_connection
from logger import awg_logger

#import other modules
import time

class AWG_format:
    def __init__(self, ip_address):
        self.ip_address = ip_address

        #create insatces for connection and logger classes
        self.connection = AWG_connection(ip_address)
        self.log = awg_logger()

        #select the recourse from connection class
        self.resource = self.connection.get_resource()

    def set_byte_order(self, order: str):
        """
        Set the byte order for binary data transfers.

        Args:
            order (str): 'NORMal' (big endian) or 'SWAPped' (little endian)

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        valid_orders = ["NORMal", "SWAPped"]
        if order not in valid_orders:
            return {"Error": f"Invalid byte order '{order}'. Must be one of {valid_orders}"}

        if self.resource:
            try:
                command = f":FORM:BORD {order}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                response = self.get_byte_order()
                self.log._log_command(command, duration_ms=duration, response=str(response))
                return {"Status": f"Byte order set to {order}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_byte_order(self):
        """
        Query the current byte order setting for binary data transfers.
    
        Returns:
            dict: {"Byte Order": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = ":FORM:BORD?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000
    
                byte_order = response.strip()
                self.log._log_command(command, duration_ms=duration, response=byte_order)
                return {"Byte Order": byte_order, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}

