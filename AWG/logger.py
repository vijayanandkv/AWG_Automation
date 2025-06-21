import os
import time
import datetime

class awg_logger:
    def __init__(self, device_name = 'AWG'):
        self._log_file_path = None
    
    #---------------------- INITIALIZE LOG FILE ---------------------

    def _initialize_log_file(self, device_name = str):
        #Initialize the log file with time stamp
        now = datetime.datetime.now().strftime("%d%m%Y%H%M")
        file_name = f"{device_name}_{now}.txt" # set the log file name as device IP with date and tiem of file creation.
        self._log_file_path = file_name # set log file path

        with open(self._log_file_path, 'w') as f:
            f.write(f"Log file created for {device_name.upper()} at {datetime.datetime.now()} \n")

    # Append all log commands

    def _log_command(self, command: str, duration_ms: float = None, response: str = None):

        """Log SCPI  command with duration and response"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] SCPI: {command} "

        if duration_ms is not None:
            log_line += f"| Duration : {duration_ms:.2f} ms"
        if response is not None:
            log_line += f" | Response: {response}"
        log_line += "\n"

        if hasattr(self, '_log_file_path') and self._log_file_path:
            with open(self._log_file_path, 'a') as f:
                f.write(log_line)

        return log_line #For current command display in GUI