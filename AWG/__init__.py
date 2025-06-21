# AWG/__init__.py

# Main interface
from .AWGController import AWG_Controller

# Internal subsystem modules (optional to expose individually)
from .AWGConnection import AWG_connection
from .AWGCommonCommands import AWG_common_commands
from .AWGStaus import AWG_system_status
from .AWGARMTRIGger import AWG_ARM_TRIGger_Controller
from .AWGTriggerInput import AWG_Trigger_input
from .AWGInstrument import AWG_instrument
from .AWGFormat import AWG_format
from .AWGMemmory import AWG_memmory
from .AWGOutput import AWG_output
from .AWGSamplingFrequency import AWG_sampling_frequency
from .AWG_ROscillator import AWG_Reference_Oscillator
from .AWGVoltageSubsystem import AWG_Voltage_Subsystem
from .AWGFunctionMode import AWG_Function_Mode
from .AWGFrequencyPhaseResponse import AWG_frequency_phase_response
from .AWGCarrier import AWG_carrier
from .AWGStableSubsyatem import AWG_stable_system
from .AWGTestSubsystem import AWG_test
from .AWGTraceSubsystem import AWG_trace_system

# Limit public API to just the controller
__all__ = ["AWG_Controller"]
