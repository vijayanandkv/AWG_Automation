#import awg modules
from AWGConnection import AWG_connection
from logger import awg_logger

#import other modules
import time

class AWG_frequency_phase_response:
    def __init__(self, ip_address):
        self.ip_address = ip_address

        #create insatces for connection and logger classes
        self.connection = AWG_connection(ip_address)
        self.log = awg_logger()

        #select the recourse from connection class
        self.resource = self.connection.get_resource()

    def get_channel_characteristics(self, channel: int, amplitude: float = None, sample_frequency: float = None):
        """
        Query the frequency and phase response data for the specified channel.

        Args:
            channel (int): Channel number (1–4)
            amplitude (float, optional): Output amplitude in volts.
            sample_frequency (float, optional): Sample frequency in Hz.

        Returns:
            dict: Parsed frequency, magnitude, and phase triplets or raw data string and duration.
        """
        if channel not in [1, 2, 3, 4]:
            return {"Error": "Invalid channel. Must be 1, 2, 3, or 4."}

        if self.resource:
            try:
                # Build command with optional parameters
                command = f":CHAR{channel}?"
                if amplitude is not None and sample_frequency is not None:
                    command = f":CHAR{channel}? {amplitude},{sample_frequency}"
                elif amplitude is not None:
                    command = f":CHAR{channel}? {amplitude}"

                # Send command and measure time
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response.strip())

                # Parse response into structured format
                try:
                    values = list(map(float, response.strip().split(',')))
                    data = [
                        {
                            "Frequency (Hz)": values[i],
                            "Magnitude (linear)": values[i + 1],
                            "Phase (rad)": values[i + 2]
                        }
                        for i in range(0, len(values), 3)
                    ]
                    return {
                        "Channel": channel,
                        "Data": data,
                        "Duration(ms)": duration
                    }
                except Exception:
                    # In case the response is malformed
                    return {
                        "Channel": channel,
                        "Raw Response": response.strip(),
                        "Duration(ms)": duration
                    }

            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}

        return {"Error": "Device not connected"}
