#import awg modules
from AWGConnection import AWG_connection
from logger import awg_logger
import numpy as np

#import other modules
import time

class AWG_trace_system:
    def __init__(self, ip_address):
        self.ip_address = ip_address

        #create insatces for connection and logger classes
        self.connection = AWG_connection(ip_address)
        self.log = awg_logger()

        #select the recourse from connection class
        self.resource = self.connection.get_resource()

    def set_trace_memory_mode(self, channel: int, mode: str):
        """
        Set the memory mode (INTernal or EXTended) for the specified channel and confirm via query.

        Args:
            channel (int): Channel number (1 to 4)
            mode (str): "INT", "EXT", or full form "INTernal" or "EXTended"""


        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be 1, 2, 3, or 4."}

            mode_map = {
                "INT": "INT", "EXT": "EXT", "NONE": "NONE"
            }

            mode_upper = mode.strip().upper()
            if mode_upper not in mode_map:
                return {"Error": "Mode must be 'INT' or 'EXT' (or full forms)"}

            final_mode = mode_map[mode_upper]
            command = f":TRAC{channel}:MMOD {final_mode}"
            query_command = f":TRAC{channel}:MMOD?"

            try:
                start_time = time.time()
                self.resource.write(command)
                response = self.resource.query(query_command).strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {
                    "Set": final_mode,
                    "Confirmed": response,
                    "Duration(ms)": duration
                }
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_trace_memory_mode(self, channel: int):
        """
        Query the current memory mode of the specified channel (1–4).

        Args:
            channel (int): Channel number (1 to 4)

        Returns:
            dict: {"Query": <response>, "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Invalid channel. Must be 1, 2, 3, or 4."}

            command = f":TRAC{channel}:MMOD?"
            try:
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {"Query": response, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def define_waveform_segment(self, channel: int, segment_id: int, length: int, init_value: int = None):
        """
        Define a waveform memory segment on the given channel.

        Args:
            channel (int): Channel number (1–4)
            segment_id (int): Segment ID to define
            length (int): Length of the segment in samples (excluding marker samples)
            init_value (int, optional): If provided, initializes all samples to this DAC value.

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Channel must be 1, 2, 3, or 4"}
            try:
                if init_value is not None:
                    command = f":TRAC{channel}:DEF {segment_id},{length},{init_value}"
                else:
                    command = f":TRAC{channel}:DEF {segment_id},{length}"

                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response="OK")

                return {
                    "Status": f"Defined segment {segment_id} on channel {channel}",
                    "Duration(ms)": duration
                }
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}

        return {"Error": "Device not connected"}
    
    def define_new_waveform_segment(self, channel: int, length: int, init_value: int = None):
        """
        Define a new waveform segment on the specified channel and return the new segment ID.

        Args:
            channel (int): Channel number (1–4)
            length (int): Length of the segment in samples (excluding marker samples)
            init_value (int, optional): Optional DAC init value to fill the segment with.

        Returns:
            dict: {"SegmentID": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Channel must be 1, 2, 3, or 4"}
            try:
                command = f":TRAC{channel}:DEF:NEW? {length}"
                if init_value is not None:
                    command += f",{init_value}"

                start_time = time.time()
                segment_id = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=segment_id)

                return {
                    "SegmentID": int(segment_id),
                    "Duration(ms)": duration
                }
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def define_write_only_segment(self, channel: int, segment_id: int, length: int, init_value: int = None):
        """
        Define a write-only waveform segment on the specified channel.

        Args:
            channel (int): Channel number (1–4)
            segment_id (int): ID of the segment to define
            length (int): Segment length in samples (excluding markers)
            init_value (int, optional): Optional DAC initialization value

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Channel must be 1–4"}
            try:
                command = f":TRAC{channel}:DEF:WONL {segment_id},{length}"
                if init_value is not None:
                    command += f",{init_value}"

                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response="OK")

                return {"Status": f"Write-only segment {segment_id} defined on channel {channel}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def define_write_only_segment_new(self, channel: int, length: int, init_value: int = None):
        """
        Create a new write-only waveform segment on the specified channel and return the assigned segment ID.

        Args:
            channel (int): Channel number (1–4)
            length (int): Segment length in samples (excluding marker samples)
            init_value (int, optional): Optional DAC initialization value

        Returns:
            dict: {"SegmentID": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            if channel not in [1, 2, 3, 4]:
                return {"Error": "Channel must be 1–4"}
            try:
                command = f":TRAC{channel}:DEF:WONL:NEW? {length}"
                if init_value is not None:
                    command += f",{init_value}"

                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000

                self.log._log_command(command, duration_ms=duration, response=response)
                return {"SegmentID": int(response), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def write_waveform_data(self, channel: int, segment_id: int, offset: int, samples: list[float]):
        """
        Write numeric waveform data to the specified memory segment.

        Args:
            channel (int): Channel number (1–4)
            segment_id (int): Segment ID
            offset (int): Offset in samples from segment start
            samples (list of float): List of waveform data samples to write

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                if channel not in [1, 2, 3, 4]:
                    return {"Error": "Invalid channel number. Must be 1–4"}
                sample_str = ",".join(str(s) for s in samples)
                command = f":TRAC{channel}:DATA {segment_id},{offset},{sample_str}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response="OK")
                return {"Status": f"{len(samples)} samples written to segment {segment_id}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def read_waveform_data(self, channel: int, segment_id: int, offset: int, length: int):
        """
        Query waveform data from a segment.

        Args:
            channel (int): Channel number (1–4)
            segment_id (int): Segment ID to read from
            offset (int): Offset in samples from segment start
            length (int): Number of samples to read

        Returns:
            dict: {"Samples": [...], "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                if channel not in [1, 2, 3, 4]:
                    return {"Error": "Invalid channel number. Must be 1–4"}
                command = f":TRAC{channel}:DATA? {segment_id},{offset},{length}"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response="<<data omitted>>")
                samples = [float(x) for x in response.split(",")]
                return {"Samples": samples, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def read_waveform_data_binary(self, channel: int, segment_id: int, offset: int, length: int):
        """
        Query waveform data from a segment using IEEE binary block format.

        Args:
            channel (int): Channel number (1–4)
            segment_id (int): Segment ID to read from
            offset (int): Offset from the start of the segment in samples
            length (int): Number of samples to read

        Returns:
            dict: {"Samples": [...], "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                if channel not in [1, 2, 3, 4]:
                    return {"Error": "Invalid channel number. Must be 1–4"}
                command = f":TRAC{channel}:DATA:BLOC? {segment_id},{offset},{length}"
                start_time = time.time()
                self.resource.write(command)
                raw = self.resource.read_raw()
                duration = (time.time() - start_time) * 1000

                # Parse IEEE binary block format
                if raw[0:1] != b'#':
                    raise ValueError("Unexpected response format (missing IEEE block header)")

                header_len = int(raw[1:2])
                num_digits = int(raw[2:2 + header_len])
                data_start = 2 + header_len
                data_bytes = raw[data_start:data_start + num_digits]

                samples = np.frombuffer(data_bytes, dtype='>f4').tolist()  # '>f4' for big-endian float32

                self.log._log_command(command, duration_ms=duration, response=f"<<{len(samples)} binary samples>>")
                return {"Samples": samples, "Duration(ms)": duration}

            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}

        return {"Error": "Device not connected"}
    
    def import_waveform_file(self,
                         channel: int,
                         segment_id: int,
                         file_path: str,
                         file_type: str,
                         data_type: str,
                         marker_flag: str,
                         padding: str = None,
                         init_value: int = None,
                         ignore_header: bool = None):
        """
        Import waveform data from a file to the specified segment in the AWG.

        Args:
            channel (int): Channel number (1–4).
            segment_id (int): Target segment ID.
            file_path (str): Full path to the waveform file.
            file_type (str): File format. One of ['TXT','BIN','BIN8','IQBIN','BIN6030','BIN5110','LICensed','MAT89600','DSA90000','CSV']
            data_type (str): One of ['IONLy', 'QONLy', 'BOTH']
            marker_flag (str): 'ON', 'OFF', '1', or '0'
            padding (str, optional): Either 'ALENgth' or 'FILL'
            init_value (int, optional): Initialization value if FILL is used
            ignore_header (bool, optional): If True, ignore header params in file

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                if channel not in [1, 2, 3, 4]:
                    return {"Error": "Channel must be between 1 and 4"}

                file_path_escaped = f'"{file_path}"'  # Wrap in quotes if needed
                command = f":TRAC{channel}:IMP {segment_id},{file_path_escaped},{file_type},{data_type},{marker_flag}"

                if padding:
                    command += f",{padding}"
                    if padding.upper() == "FILL":
                        if init_value is not None:
                            command += f",{init_value}"
                        else:
                            command += ",0"  # default init_value
                        if ignore_header is not None:
                            command += f",{int(ignore_header)}"

                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response="OK")
                return {"Status": f"Waveform imported to segment {segment_id} on channel {channel}", "Duration(ms)": duration}

            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}

        return {"Error": "Device not connected"}
    
    def set_import_resample_mode(self, channel: int, mode: str):
        """
        Set the resampling mode for importing LICensed waveform files.

        Args:
            channel (int): Channel number (1–4).
            mode (str): Resampling mode. One of ['TIMing', 'KSRate', 'KWLength', 'PADDing', 'TRUNcate', 'REPeat'].

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                mode = mode.upper()
                if mode not in ["TIM", "KSR", "KWL", "PADD", "TRUN", "REP"]:
                    return {"Error": f"Invalid mode: {mode}"}

                command = f":TRAC{channel}:IMP:RES {mode}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=str(self.get_import_resample_mode(channel)))
                return {"Status": f"Set resampling mode to {mode} on channel {channel}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_import_resample_mode(self, channel: int):
        """
        Query the current resampling mode for LICensed waveform file import.

        Args:
            channel (int): Channel number (1–4).

        Returns:
            dict: {"ResampleMode": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = f":TRAC{channel}:IMP:RES?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {"ResampleMode": response, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_import_resample_waveform_length(self, channel: int, length: int):
        """
        Set the target waveform length for LICensed file import using resample mode KWLength.

        Args:
            channel (int): Channel number (1–4).
            length (int): Target waveform length (number of samples).

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = f":TRAC{channel}:IMP:RES:WLEN {length}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=str(self.get_import_resample_waveform_length(channel)))
                return {
                    "Status": f"Waveform length {length} set for channel {channel}",
                    "Duration(ms)": duration
                }
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_import_resample_waveform_length(self, channel: int):
        """
        Query the target waveform length for LICensed file import using resample mode KWLength.

        Args:
            channel (int): Channel number (1–4).

        Returns:
            dict: {"WaveformLength": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = f":TRAC{channel}:IMP:RES:WLEN?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {"WaveformLength": int(response), "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_import_scaling(self, channel: int, state: bool):
        """
        Enable or disable scaling for waveform file import.

        Args:
            channel (int): Channel number (1–4).
            state (bool): True to enable scaling (ON), False to disable (OFF).

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                state_str = "ON" if state else "OFF"
                command = f":TRAC{channel}:IMP:SCAL {state_str}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=str(self.get_import_scaling(self, channel)))
                return {"Status": f"Scaling set to {state_str} for channel {channel}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_import_scaling(self, channel: int):
        """
        Query whether scaling is enabled for waveform file import.

        Args:
            channel (int): Channel number (1–4).

        Returns:
            dict: {"ScalingState": "ON" or "OFF", "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = f":TRAC{channel}:IMP:SCAL?"
                start_time = time.time()
                response = self.resource.query(command).strip().upper()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {"ScalingState": response, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def delete_waveform_segment(self, channel: int, segment_id: int):
        """
        Delete a waveform memory segment from the specified channel.

        Args:
            channel (int): Channel number (1–4).
            segment_id (int): ID of the segment to delete.

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = f":TRAC{channel}:DEL {segment_id}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=f"Deleted segement {segment_id}")
                return {"Status": f"Segment {segment_id} deleted on channel {channel}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def delete_all_waveform_segments(self, channel: int):
        """
        Delete all waveform memory segments from the specified channel.

        Args:
            channel (int): Channel number (1–4).

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = f":TRAC{channel}:DEL:ALL"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=f"All segments in channel {channel} deleted")
                return {"Status": f"All segments deleted on channel {channel}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_segment_catalog(self, channel: int):
        """
        Query the catalog of waveform memory segments for a specified channel.

        Args:
            channel (int): Channel number (1–4).

        Returns:
            dict: {
                "Segments": List of tuples (segment_id, length),
                "Raw": str (raw SCPI response),
                "Duration(ms)": float
            } or {"Error": ...}
        """
        if self.resource:
            try:
                command = f":TRAC{channel}:CAT?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)

                values = list(map(int, response.split(",")))
                segments = [(values[i], values[i+1]) for i in range(0, len(values), 2)]

                return {"Segments": segments, "Raw": response, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_waveform_memory_info(self, channel: int):
        """
        Query available waveform memory on a specified channel.

        Args:
            channel (int): Channel number (1–4).

        Returns:
            dict: {
                "Bytes_Available": int,
                "Bytes_In_Use": int,
                "Contiguous_Bytes": int,
                "Raw": str,
                "Duration(ms)": float
            } or {"Error": ...}
        """
        if self.resource:
            try:
                command = f":TRAC{channel}:FREE?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)

                parts = list(map(int, response.split(",")))
                return {
                    "Bytes_Available": parts[0],
                    "Bytes_In_Use": parts[1],
                    "Contiguous_Bytes": parts[2],
                    "Raw": response,
                    "Duration(ms)": duration
                }
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_segment_name(self, channel: int, segment_id: int, name: str):
        """
        Assign a name to a waveform memory segment.

        Args:
            channel (int): Channel number (1–4).
            segment_id (int): ID of the segment.
            name (str): Name to assign (max 32 characters).

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                if len(name) > 32:
                    return {"Error": "Name must be 32 characters or fewer."}
                command = f':TRAC{channel}:NAME {segment_id},"{name}"'
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=str(self.get_segment_name(channel, segment_id)))
                return {
                    "Status": f"Name '{name}' set for segment {segment_id} on channel {channel}",
                    "Duration(ms)": duration
                }
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_segment_name(self, channel: int, segment_id: int):
        """
        Query the name of a waveform memory segment.

        Args:
            channel (int): Channel number (1–4).
            segment_id (int): ID of the segment.

        Returns:
            dict: {"Segment_ID": ..., "Name": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = f":TRAC{channel}:NAME? {segment_id}"
                start_time = time.time()
                response = self.resource.query(command).strip().strip('"')
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {
                    "Segment_ID": segment_id,
                    "Name": response,
                    "Duration(ms)": duration
                }
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_segment_comment(self, channel: int, segment_id: int, comment: str):
        """
        Assign a comment to a waveform memory segment.

        Args:
            channel (int): Channel number (1–4).
            segment_id (int): Segment ID.
            comment (str): Comment text (max 256 characters).

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                if len(comment) > 256:
                    return {"Error": "Comment must be 256 characters or fewer."}
                command = f':TRAC{channel}:COMM {segment_id},"{comment}"'
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=str(self.get_segment_comment(channel,segment_id)))
                return {
                    "Status": f"Comment set for segment {segment_id} on channel {channel}",
                    "Duration(ms)": duration
                }
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_segment_comment(self, channel: int, segment_id: int):
        """
        Query the comment of a waveform memory segment.

        Args:
            channel (int): Channel number (1–4).
            segment_id (int): Segment ID.

        Returns:
            dict: {"Segment_ID": ..., "Comment": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = f":TRAC{channel}:COMM? {segment_id}"
                start_time = time.time()
                response = self.resource.query(command).strip().strip('"')
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {
                    "Segment_ID": segment_id,
                    "Comment": response,
                    "Duration(ms)": duration
                }
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_segment_selection(self, channel: int, segment_id: int):
        """
        Set the output segment for the specified channel in arbitrary function mode.

        Args:
            channel (int): Channel number (1–4).
            segment_id (int): Segment ID to be selected.

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = f":TRAC{channel}:SEL {segment_id}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=str(self.get_segment_selection(channel)))
                return {
                    "Status": f"Segment {segment_id} selected for channel {channel}",
                    "Duration(ms)": duration
                }
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_segment_selection(self, channel: int):
        """
        Query the selected segment for the specified channel.

        Args:
            channel (int): Channel number (1–4).

        Returns:
            dict: {"Selected_Segment": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = f":TRAC{channel}:SEL?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {
                    "Selected_Segment": int(response),
                    "Duration(ms)": duration
                }
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_segment_advancement_mode(self, channel: int, mode: str):
        """
        Set the advancement mode for the selected segment on a channel.

        Args:
            channel (int): Channel number (1–4).
            mode (str): Advancement mode. Must be one of: "AUTO", "COND", "REP", "SING".

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        valid_modes = ["AUTO", "COND", "REP", "SING"]
        if mode.upper() not in valid_modes:
            return {"Error": f"Invalid mode '{mode}'. Must be one of {valid_modes}"}

        if self.resource:
            try:
                command = f":TRAC{channel}:ADV {mode.upper()}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=str(self.get_segment_advancement_mode(channel)))
                return {
                    "Status": f"Advancement mode set to {mode.upper()} on channel {channel}",
                    "Duration(ms)": duration
                }
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_segment_advancement_mode(self, channel: int):
        """
        Query the advancement mode for the selected segment on a channel.

        Args:
            channel (int): Channel number (1–4).

        Returns:
            dict: {"Advancement_Mode": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = f":TRAC{channel}:ADV?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {
                    "Advancement_Mode": response,
                    "Duration(ms)": duration
                }
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_segment_loop_count(self, channel: int, count: int):
        """
        Set the loop count for the selected segment on the specified channel.

        Args:
            channel (int): Channel number (1–4).
            count (int): Number of repetitions (1 to 4G-1).

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if count < 1 or count > (4_000_000_000 - 1):
            return {"Error": "Loop count must be in range 1 to 4G-1 (i.e., 1 to 3,999,999,999)"}

        if self.resource:
            try:
                command = f":TRAC{channel}:COUN {count}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=str(self.get_segment_loop_count(channel)))
                return {
                    "Status": f"Loop count set to {count} on channel {channel}",
                    "Duration(ms)": duration
                }
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_segment_loop_count_limit(self, channel: int, limit_type: str):
        """
        Query the MINimum or MAXimum loop count for the selected segment on the specified channel.

        Args:
            channel (int): Channel number (1–4).
            limit_type (str): Either 'MINimum' or 'MAXimum' (case-insensitive).

        Returns:
            dict: {"Loop_Count_Limit": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if limit_type.upper() not in ["MIN", "MAX"]:
            return {"Error": "limit_type must be either 'MINimum' or 'MAXimum'"}

        if self.resource:
            try:
                limit_arg = limit_type.upper()
                command = f":TRAC{channel}:COUN? {limit_arg}"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {
                    "Loop_Count_Limit": int(response),
                    "Duration(ms)": duration
                }
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_segment_loop_count(self, channel: int):
        """
        Query the loop count for the selected segment on the specified channel.

        Args:
            channel (int): Channel number (1–4).

        Returns:
            dict: {"Loop_Count": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = f":TRAC{channel}:COUN?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {
                    "Loop_Count": int(response),
                    "Duration(ms)": duration
                }
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_marker_state(self, channel: int, state: str | int):
        """
        Set the marker state for the selected segment on a given channel.

        Args:
            channel (int): Channel number (1–4).
            state (str|int): 'ON', 'OFF', 1, or 0.

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        valid_states = {"ON", "OFF", 1, 0}
        if state not in valid_states:
            return {"Error": "State must be one of: 'ON', 'OFF', 1, 0"}

        if self.resource:
            try:
                command = f":TRAC{channel}:MARK {state}"
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=str(self.get_marker_state(channel)))
                return {"Status": f"Marker set to {state} on channel {channel}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}

        return {"Error": "Device not connected"}
    
    def get_marker_state(self, channel: int):
        """
        Query the marker state for the selected segment on a given channel.

        Args:
            channel (int): Channel number (1–4).

        Returns:
            dict: {"Marker_State": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = f":TRAC{channel}:MARK?"
                start_time = time.time()
                response = self.resource.query(command).strip()
                duration = (time.time() - start_time) * 1000
                self.log._log_command(command, duration_ms=duration, response=response)
                return {"Marker_State": response, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}

        return {"Error": "Device not connected"}

































