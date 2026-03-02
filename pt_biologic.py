#####################################################################
# This document is a part of the BioLogic OEM Package and is
# protected by the terms of the OEM Package licence as well as
# other intellectual property rights owned by BioLogic SAS.
# This document may only be used for non-commercial purposes
# such as for the integration of BioLogic equipment to larger
# technical solutions manufactured  and/or delivered to end-users.
#####################################################################

import os
import time

import kbio.kbio_types as KBIO
from kbio.c_utils import c_is_64b
from kbio.kbio_api import KBIO_api
from kbio.kbio_tech import get_experiment_data
from kbio.kbio_tech import get_info_data

from CA_biologic import ca_parm
from OCV_biologic import ocv_parm
from CP_biologic import cp_parm
from CV_biologic import cv_parm

from PySide6.QtCore import Signal,QObject,QTimer
from PySide6.QtWidgets import QFileDialog

from misc_handleException import errorDeco

class Biologic(QObject):
    signalLog=Signal(str) 
    signalData=Signal(str, object)
    signalConnected=Signal(list)
    signalFinished=Signal()
    signalChannelOption=Signal(list)
    def __init__(self,address,binary_path):
        super().__init__()
        self.recordTimers = {}  # dict of channel: QTimer
        self.address=address
        self.binary_path=binary_path
        self.api = None
        self.id_ = None
        self.is_running = False
        self.sequence=None
        self.sequence_by_channel = {}
        self.active_channels = set()

        self.force_load_firmware=True
        if c_is_64b:
            DLL_file = "EClib64.dll"
        else:
            DLL_file = "EClib.dll"

        self.DLL_path = f"{binary_path}{os.sep}{DLL_file}"

    @errorDeco(signal='self.signalLog')
    def connectDevice(self):
        # API initialize
        self.api = KBIO_api(self.DLL_path)
        # BL_GetLibVersion
        version = self.api.GetLibVersion()
        self.signalLog.emit(f"> EcLib version: {version}")
        # BL_Connect
        self.id_, device_info = self.api.Connect(self.address)
        self.signalLog.emit(f"> device[{self.address}] info :")
        self.signalLog.emit(f"{device_info}")
        
        # Get all available channels
        self.channels = list(self.api.GetChannelsPlugged(self.id_))
        if not self.channels:
            self.signalLog.emit("> No channels available on the device.")
            self.signalFinished.emit()
            return
        self.signalLog.emit(f"> Available channels: {self.channels}")
        self.signalChannelOption.emit(self.channels)
        
        # Create timers for each channel
        for ch in self.channels:
            timer = QTimer()
            timer.setInterval(1000)
            timer.timeout.connect(lambda ch=ch: self.recordData(ch))
            self.recordTimers[ch] = timer
        
        # Use the first channel as default
        self.channel = self.channels[0]
        
        # based on board_type, determine firmware filenames (assume same for all channels)
        self.board_type = self.api.GetChannelBoardType(self.id_, self.channel)
        match self.board_type:
            case KBIO.BOARD_TYPE.ESSENTIAL.value:
                firmware_path = "kernel.bin"
                fpga_path = "Vmp_ii_0437_a6.xlx"
            case KBIO.BOARD_TYPE.PREMIUM.value:
                firmware_path = "kernel4.bin"
                fpga_path = "vmp_iv_0395_aa.xlx"
            case KBIO.BOARD_TYPE.DIGICORE.value:
                firmware_path = "kernel.bin"
                fpga_path = ""
            case _:
                self.signalLog.emit("> Board type detection failed, potentiostat thread terminated.")
                self.signalFinished.emit()
                return
        # Load firmware for all available channels
        self.signalLog.emit(f"> Loading {firmware_path} for channels {self.channels} ...")
        channel_map = self.api.channel_map(set(self.channels))
        self.api.LoadFirmware(self.id_, channel_map, firmware=firmware_path, fpga=fpga_path, force=self.force_load_firmware)
        self.signalLog.emit("> ... firmware loaded")

        # Get options for each channel
        self.channels_options = []
        for ch in self.channels:
            channel_info = self.api.GetChannelInfo(self.id_, ch)
            self.signalLog.emit(f"> Channel {ch} info :")
            self.signalLog.emit(f"{channel_info}")
            
            if not channel_info.is_kernel_loaded:
                self.signalLog.emit(f"> Channel {ch}: kernel must be loaded, skipping.")
                continue
            
            # Get available current ranges
            current_ranges = self._get_enum_range(KBIO.I_RANGE, channel_info.MinIRange, channel_info.MaxIRange) + ["I_RANGE_AUTO"]
            # Get available bandwidth options
            bandwidths = self._get_enum_range(KBIO.BANDWIDTH, 1, channel_info.MaxBandwidth)
            # Get all potential ranges
            potential_ranges = self._get_all_enum_options(KBIO.E_RANGE)
            
            self.channels_options.append([ch, current_ranges, potential_ranges, bandwidths])
        
        if not self.channels_options:
            self.signalLog.emit("> No valid channels with loaded kernel.")
            self.signalFinished.emit()
            return
        
        # Emit options for all channels
        self.signalConnected.emit(self.channels_options)

    @errorDeco(signal='self.signalLog')
    def runSequence(self, sequence, channels, filename_user=None):
        #check if potentiostat is connected and kernel is loaded
        if not hasattr(self, "api") or not self.api:
            self.signalLog.emit("> Device not connected. Please connect to the device first.")
            return
        if isinstance(channels, int):
            run_channels = [channels]
        elif isinstance(channels, (list, tuple, set)):
            run_channels = sorted(set(channels))
        else:
            self.signalLog.emit("> Invalid channel selection.")
            return

        if not run_channels:
            self.signalLog.emit("> No channels selected.")
            return

        if isinstance(sequence, dict):
            sequence_by_channel = {ch: sequence.get(ch, []) for ch in run_channels}
        else:
            sequence_by_channel = {ch: sequence for ch in run_channels}

        self.sequence_by_channel = {}
        loaded_channels = []
        verbosity = 1

        for ch in run_channels:
            sequence_ch = sequence_by_channel.get(ch, [])
            if not sequence_ch:
                self.signalLog.emit(f"> CH {ch}: no techniques to load, skipping.")
                continue

            tech_to_load = []
            for measurement in sequence_ch:
                if isinstance(measurement, dict):
                    measurement_param = measurement
                elif hasattr(measurement, "outputParam") and callable(measurement.outputParam):
                    measurement_param = measurement.outputParam()
                else:
                    self.signalLog.emit(f"> CH {ch}: invalid measurement item {measurement}, skipping.")
                    continue

                technique = str(measurement_param.get('technique', '')).lower()
                match technique:
                    case 'ca':
                        tech_file, ecc_parms = ca_parm(self.board_type, self.api, measurement_param)
                    case 'ocv':
                        tech_file, ecc_parms = ocv_parm(self.board_type, self.api, measurement_param)
                    case 'cv':
                        tech_file, ecc_parms = cv_parm(self.board_type, self.api, measurement_param)
                    case 'cp':
                        tech_file, ecc_parms = cp_parm(self.board_type, self.api, measurement_param)
                    case _:
                        self.signalLog.emit(f"> CH {ch}: technique {measurement_param.get('technique')} is not valid, skipping.")
                        continue
                tech_to_load.append((tech_file, ecc_parms))

            if not tech_to_load:
                self.signalLog.emit(f"> CH {ch}: no valid techniques to load, skipping.")
                continue

            for index, (tech_file, ecc_parms) in enumerate(tech_to_load):
                first = index == 0
                last = index == len(tech_to_load) - 1
                self.api.LoadTechnique(self.id_, ch, tech_file, ecc_parms, first=first, last=last, display=(verbosity > 1))

            self.sequence_by_channel[ch] = sequence_ch
            loaded_channels.append(ch)

        if not loaded_channels:
            self.signalLog.emit("> No channel could be prepared. Experiment not started.")
            return

        self.filenameUser = filename_user if filename_user else self._getUserFilename()
        if not self.filenameUser:
            self.signalLog.emit("> Data file save cancelled. Experiment not started.")
            return

        if len(loaded_channels) == 1:
            ch = loaded_channels[0]
            self.api.StartChannel(self.id_, ch)
            if self.recordTimers[ch].isActive():
                self.recordTimers[ch].stop()
            self.recordTimers[ch].start()
            self.signalLog.emit(f"> Experiment started on channel {ch}.")
        else:
            channel_map = self.api.channel_map(set(loaded_channels))
            self.api.StartChannels(self.id_, channel_map)
            for ch in loaded_channels:
                if self.recordTimers[ch].isActive():
                    self.recordTimers[ch].stop()
                self.recordTimers[ch].start()
            self.signalLog.emit(f"> Experiment started on channels {loaded_channels}.")

        self.sequence = self.sequence_by_channel.get(loaded_channels[0], [])
        self.channel = loaded_channels[0]
        self.active_channels = set(loaded_channels)
        self.is_running = True

    @errorDeco(signal='self.signalLog')
    def recordData(self, channel):
        data = self.api.GetData(self.id_, channel)
        current_values, data_info, _ = data
        techIndex=data_info.TechniqueIndex

        sequence_ch = self.sequence_by_channel.get(channel, self.sequence)
        step_data = sequence_ch[techIndex - 1] if sequence_ch and techIndex - 1 < len(sequence_ch) else None

        if isinstance(step_data, dict):
            loop = step_data.get('loop', [])
            expName = step_data.get('name', 'step')
        else:
            loop = getattr(step_data, 'loop', []) if step_data is not None else []
            expName = getattr(step_data, 'name', 'step') if step_data is not None else 'step'

        filename=f'{self.filenameUser}_CH{channel}_loop{loop}_{expName}.csv'
        status, tech_name = get_info_data(self.api, data)
        
        for output in get_experiment_data(self.api, data, tech_name, self.board_type):
            self.writeData(output, filename)
            self.signalData.emit(tech_name, output)

        if status == "STOP":
            self.recordTimers[channel].stop()
            if channel in self.active_channels:
                self.active_channels.remove(channel)
            if not self.active_channels:
                self.is_running = False
                self.signalLog.emit(f"\nExperiment finished. Data recorded in {self.filenameUser} series.")
            else:
                self.signalLog.emit(f"> Channel {channel} finished. Remaining channels: {sorted(self.active_channels)}")

    @errorDeco(signal='self.signalLog')
    def stopExperiment(self, disconnect: bool = False):
        for ch, timer in self.recordTimers.items():
            if timer.isActive():
                timer.stop()

        if self.api and self.id_ is not None and self.is_running:
            for ch in self.channels:
                self.api.StopChannel(self.id_, ch)
            self.signalLog.emit(f"> Experiments stopped on all channels.")
            self.is_running = False

        if disconnect and self.api and self.id_ is not None:
            self.api.Disconnect(self.id_)
            self.signalLog.emit(f"> Disconnected from device[{self.address}].")
            self.api = None
            self.id_ = None
            self.signalFinished.emit()
    
    def _getUserFilename(self) -> str:

        default_name = f"{time.strftime('%Y%m%d')}.csv"
        filename, _ = QFileDialog.getSaveFileName(
            None,
            "Save Experiment Data",
            default_name,
            "CSV Files (*.csv);;All Files (*.*)"
        )
        return filename
    
    def _get_enum_range(self, enum_class, min_value: int, max_value: int) -> list:
        """
        Extract available enum options within a specified range.
        Args:
            enum_class: The enum class (e.g., KBIO.I_RANGE, KBIO.BANDWIDTH)
            min_value: Minimum value allowed
            max_value: Maximum value allowed
        Returns:
            List of enum values within the specified range
        """
        available = []
        for item in enum_class:
            if min_value <= item.value <= max_value:
                available.append(item)
        return available
    
    def _get_all_enum_options(self, enum_class) -> list:
        """
        Get all options from an enum class (excluding special values like KEEP).
        Args:
            enum_class: The enum class (e.g., KBIO.E_RANGE)
        Returns:
            List of all enum values (excluding negative values)
        """
        available = []
        for item in enum_class:
            if item.value >= 0:
                available.append(item)
        return available
    
    def writeData(self, output, filename: str):
        if isinstance(output, dict):
            values = output.values()
        elif isinstance(output, (list, tuple)):
            values = output
        else:
            values = [output]

        data_line = ','.join(str(item) for item in values) + '\n'
        with open(filename, 'a', encoding='utf-8') as data_file:
            data_file.write(data_line)