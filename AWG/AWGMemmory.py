#import awg modules
from AWGConnection import AWG_connection
from logger import awg_logger

#import other modules
import time

class AWG_memmory:
    def __init__(self, ip_address):
        self.ip_address = ip_address

        #create insatces for connection and logger classes
        self.connection = AWG_connection(ip_address)
        self.log = awg_logger()

        #select the recourse from connection class
        self.resource = self.connection.get_resource()

    def get_directory_catalog(self, directory_name: str = ""):
        """
        Query disk usage and list files/directories in the given AWG directory.

        Args:
            directory_name (str): Optional path (default: root directory)

        Returns:
            dict: {
                "Used Bytes": int,
                "Available Bytes": int,
                "Contents": List[Dict[str, Any]],
                "Duration(ms)": float
            } or {"Error": message}
        """
        if self.resource:
            try:
                command = f":MMEM:CAT? {directory_name}" if directory_name else ":MMEM:CAT?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000

                parts = [x.strip() for x in response.strip().split(",") if x.strip()]
                used = int(parts[0])
                available = int(parts[1])
                entries = parts[2:]

                contents = []
                i = 0
                while i < len(entries):
                    name = entries[i]
                    file_type = entries[i + 1] if (i + 1) < len(entries) else ""
                    file_size = entries[i + 2] if (i + 2) < len(entries) else ""

                    if name.startswith("[") and name.endswith("]"):
                        # It's a directory
                        contents.append({"Name": name[1:-1], "Type": "Directory", "Size(Bytes)": None})
                        i += 3
                    else:
                        # It's a file
                        contents.append({"Name": name, "Type": "File", "Size(Bytes)": int(file_size)})
                        i += 3

                self.log._log_command(command, duration_ms=duration, response=f"{len(contents)} items listed")
                return {
                    "Used Bytes": used,
                    "Available Bytes": available,
                    "Contents": contents,
                    "Duration(ms)": duration
                }
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def set_default_directory(self, directory_path: str = ""):
        """
        Set the default directory for mass memory file operations.

        Args:
            directory_path (str): Full path to set as default. If empty, resets to system default.

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                if directory_path:
                    command = f':MMEM:CDIR "{directory_path}"'
                else:
                    command = ":MMEM:CDIR"

                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                response = self.get_default_directory()
                self.log._log_command(command, duration_ms=duration, response=str(response))
                return {"Status": f"Default directory set to '{directory_path or 'System Default'}'", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def get_default_directory(self):
        """
        Query the currently set default directory for mass memory operations.

        Returns:
            dict: {"Default Directory": path, "Duration(ms)": ...} or {"Error": message}
        """
        if self.resource:
            try:
                command = ":MMEM:CDIR?"
                start_time = time.time()
                response = self.resource.query(command)
                duration = (time.time() - start_time) * 1000

                directory = response.strip().strip('"')
                self.log._log_command(command, duration_ms=duration, response=directory)
                return {"Default Directory": directory, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def copy_file(self, src_path: str, dest_path: str):
        """
        Copy a file or directory to a new location using the simple two-argument form.

        Args:
            src_path (str): Full path of the source file or directory.
            dest_path (str): Full path of the destination file or directory.

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = f':MMEM:COPY "{src_path}", "{dest_path}"'
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                self.log._log_command(command, duration_ms=duration, response="Copy successful")
                return {"Status": f"Copied '{src_path}' to '{dest_path}'", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def delete_file(self, file_path: str):
        """
        Delete a file from the AWG's mass memory.

        Args:
            file_path (str): Full path to the file to delete (e.g., "C:\\data.txt")

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = f':MMEM:DEL "{file_path}"'
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                self.log._log_command(command, duration_ms=duration, response="Delete successful")
                return {"Status": f"Deleted file: {file_path}", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def write_file_data(self, file_path: str, data: bytes):
        """
        Write raw data to a file on the instrument using IEEE 488.2 block format.

        Args:
            file_path (str): Full path to the file (e.g., "C:\\data.txt")
            data (bytes): Data to be written (binary or encoded text)

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                data_len = len(data)
                len_str = str(data_len)
                block_header = f"#{len(len_str)}{len_str}"
                full_payload = f':MMEM:DATA "{file_path}",'.encode() + block_header.encode() + data

                start_time = time.time()
                self.resource.write_raw(full_payload)
                duration = (time.time() - start_time) * 1000

                self.log._log_command(":MMEM:DATA", duration_ms=duration, response=f"{data_len} bytes written")
                return {"Status": f"Wrote {data_len} bytes to '{file_path}'", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(":MMEM:DATA", duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def read_file_data(self, file_path: str):
        """
        Read data from a file on the instrument using IEEE 488.2 block format.

        Args:
            file_path (str): Full path to the file (e.g., "C:\\data.txt")

        Returns:
            dict: {"Data": data (bytes), "Duration(ms)": float} or {"Error": message}
        """
        if self.resource:
            try:
                command = f':MMEM:DATA? "{file_path}"'
                start_time = time.time()
                raw_response = self.resource.read_raw()
                duration = (time.time() - start_time) * 1000

                # Parse IEEE 488.2 block header
                if raw_response[0:1] != b"#":
                    raise ValueError("Invalid block header in response")

                len_digits = int(raw_response[1:2])
                data_length = int(raw_response[2:2+len_digits])
                data_start = 2 + len_digits
                data = raw_response[data_start:data_start + data_length]

                self.log._log_command(command, duration_ms=duration, response=f"{len(data)} bytes read")
                return {"Data": data, "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}

        return {"Error": "Device not connected"}
    
    def create_directory(self, directory_path: str):
        """
        Create a new directory on the AWG's mass memory.

        Args:
            directory_path (str): Full path of the directory to create (e.g., "C:\\data_dir")

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = f':MMEM:MDIR "{directory_path}"'
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                self.log._log_command(command, duration_ms=duration, response="Directory created")
                return {"Status": f"Directory '{directory_path}' created successfully", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def move_file_or_directory(self, src_path: str, dest_path: str):
        """
        Move or rename a file/directory on the AWG's mass memory.

        Args:
            src_path (str): Full path to the source file or directory.
            dest_path (str): Full path to the destination file or directory.

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = f':MMEM:MOVE "{src_path}", "{dest_path}"'
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                self.log._log_command(command, duration_ms=duration, response="Move successful")
                return {"Status": f"Moved '{src_path}' to '{dest_path}'", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def remove_directory(self, directory_path: str):
        """
        Remove a directory and all its contents from the AWG's mass memory.

        Args:
            directory_path (str): Full path of the directory to remove (e.g., "C:\\data_dir")

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = f':MMEM:RDIR "{directory_path}"'
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                self.log._log_command(command, duration_ms=duration, response="Directory removed")
                return {"Status": f"Directory '{directory_path}' removed", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def load_instrument_state(self, file_path: str):
        """
        Load the complete instrument state from a file on the AWG.

        Args:
            file_path (str): Full path to the state file (e.g., "C:\\setup.sta")

        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = f':MMEM:LOAD:CST "{file_path}"'
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000

                self.log._log_command(command, duration_ms=duration, response="State loaded")
                return {"Status": f"Instrument state loaded from '{file_path}'", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}
    
    def store_instrument_state(self, file_path: str):
        """
        Store the current AWG instrument state to a file on the device.
    
        Args:
            file_path (str): Full path to the destination file (e.g., "C:\\backup\\setup.cst")
    
        Returns:
            dict: {"Status": ..., "Duration(ms)": ...} or {"Error": ...}
        """
        if self.resource:
            try:
                command = f':MMEM:STOR:CST "{file_path}"'
                start_time = time.time()
                self.resource.write(command)
                duration = (time.time() - start_time) * 1000
    
                self.log._log_command(command, duration_ms=duration, response="State stored")
                return {"Status": f"Instrument state stored to '{file_path}'", "Duration(ms)": duration}
            except Exception as e:
                self.log._log_command(command, duration_ms=0, response=str(e))
                return {"Error": str(e)}
        return {"Error": "Device not connected"}











