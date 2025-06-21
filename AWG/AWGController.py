from AWGConnection import AWG_connection
from AWGCommonCommands import AWG_common_commands
from AWGStaus import AWG_system_status
from AWGARMTRIGger import AWG_ARM_TRIGger_Controller
from AWGTriggerInput import AWG_Trigger_input
from AWGInstrument import AWG_instrument
from AWGFormat import AWG_format
from AWGMemmory import AWG_memmory
from AWGOutput import AWG_output
from AWGSamplingFrequency import AWG_sampling_frequency
from AWG_ROscillator import AWG_Reference_Oscillator
from AWGVoltageSubsystem import AWG_Voltage_Subsystem
from AWGFunctionMode import AWG_Function_Mode
from AWGFrequencyPhaseResponse import AWG_frequency_phase_response
from AWGCarrier import AWG_carrier
from AWGStableSubsyatem import AWG_stable_system
from AWGTestSubsystem import AWG_test
from AWGTraceSubsystem import AWG_trace_system


class AWG_Controller:
    def __init__(self, ip_address: str):
        self.ip_address = ip_address
        self.connection = AWG_connection(ip_address)
        self.common_commands = AWG_common_commands(ip_address)
        self.status = AWG_system_status(ip_address)
        self.arm_trig = AWG_ARM_TRIGger_Controller(ip_address)
        self.triggerInput = AWG_Trigger_input(ip_address)
        self.instrument = AWG_instrument(ip_address)
        self.format = AWG_format(ip_address)
        self.memmory = AWG_memmory(ip_address)
        self.output =AWG_output(ip_address)
        self.SamplingFrequency = AWG_sampling_frequency(ip_address)
        self.ROscillator = AWG_Reference_Oscillator(ip_address)
        self.VoltageSubsystem = AWG_Voltage_Subsystem(ip_address)
        self.FunctionMode = AWG_Function_Mode(ip_address)
        self.FrequencyPhaseResponse = AWG_frequency_phase_response(ip_address)
        self.carrier = AWG_carrier(ip_address)
        self.Stable = AWG_stable_system(ip_address)
        self.TestSubsystem = AWG_test(ip_address)
        self.TraceSubsyatem = AWG_trace_system(ip_address)

