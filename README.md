# AWG_Automation

A modular Python package to automate and control the **Keysight M8195A Arbitrary Waveform Generator** using **SCPI commands via VISA** interface.

This package provides a clean, object-oriented interface to all AWG subsystems such as output, sampling frequency, memory, waveform generation, triggering, system status, and more.

## 📦 Features

- Full SCPI command abstraction for Keysight M8195A
- Modular design: each subsystem has its own Python class
- A unified `AWG_Controller` class that integrates all functionality
- Supports waveform creation, sequencing, triggering, voltage control, and monitoring
- Designed for lab automation and GUI integration


## 🚀 Installation

### From GitHub

```bash
pip install git+https://github.com/vijayanandkv/AWG_Automation.git
from AWG import AWG_Controller

# Create controller instance (connect using VISA address)
awg = AWG_Controller("TCPIP::192.168.1.100::INSTR")

# Example: Turn on channel 1 output
awg.output.set_output_on(channel=1)

# Set sampling rate
awg.sampling_frequency.set_sample_rate(6e9)

# Generate a simple waveform or segment (user-defined)
# awg.memory.load_waveform(...)  # (example method based on your modules)

# Disconnect
awg.connection.close()
###
dependencies
pyvisa

numpy
###
matplotlib


#to Install

pip install pyvisa numpy matplotlib

#for local usage

git clone https://github.com/vijayanandkv/AWG_Automation.git
cd AWG_Automation
pip install -e .



---

✅ You can now paste this directly into a `README.md` file in your GitHub repo.

Let me know if you also want:
- A `setup.py` to make the project pip-installable
- Examples of waveform generation
- How to publish it to PyPI later (optional)


