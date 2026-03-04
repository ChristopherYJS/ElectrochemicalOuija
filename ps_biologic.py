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

from ps_CA import ca_parm
from ps_OCV import ocv_parm
from ps_CP import cp_parm
from ps_CV import cv_parm

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
        self.timer_record = {}  # dict of channel: QTimer
        self.address=address
        self.binary_path=binary_path
        self.api = None
        self.id_ = None
        self.channel_is_running = {}
        self.channel_params = {}
        self.filename_user = None

        self.force_load_firmware=True
        if c_is_64b:
            dll_file = "EClib64.dll"
        else:
            dll_file = "EClib.dll"

        self.dll_path = f"{binary_path}{os.sep}{dll_file}"

    @errorDeco(signal='self.signalLog')
    def connectDevice(self):
        # API initialize
        self.api = KBIO_api(self.dll_path)
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
            self.timer_record[ch] = timer
        
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
    def runSequence(self, sequences, filename_user):
        verbosity = 1
        self.filename_user=filename_user
        #check if potentiostat is connected and kernel is loaded
        if not hasattr(self, "api") or not self.api:
            self.signalLog.emit("> Device not connected. Please connect to the device first.")
            return
        # Check which channel(s) to run on
        channels=list(sequences.keys())

        if not channels:
            self.signalLog.emit("> No channels selected.")
            return

        loaded_channels = []
        for ch in channels:
            sequence_ch = sequences.get(ch, [])
            if not sequence_ch:
                self.signalLog.emit(f"> CH {ch}: no techniques to load, skipping.")
                continue

            tech_to_load = []
            for tech_params in sequence_ch:
                if not isinstance(tech_params, dict):
                    self.signalLog.emit(f"> CH {ch}: invalid technique parameter object: {tech_params}.")
                    return

                technique = str(tech_params.get('technique', '')).lower()
                match technique:
                    case 'ca':
                        tech_file, ecc_parms = ca_parm(self.board_type, self.api, tech_params)
                    case 'ocv':
                        tech_file, ecc_parms = ocv_parm(self.board_type, self.api, tech_params)
                    case 'cv':
                        tech_file, ecc_parms = cv_parm(self.board_type, self.api, tech_params)
                    case 'cp':
                        tech_file, ecc_parms = cp_parm(self.board_type, self.api, tech_params)
                    case _:
                        self.signalLog.emit(f"> CH {ch}: technique {tech_params.get('technique')} is not valid, skipping.")
                        continue
                tech_to_load.append((tech_file, ecc_parms))

            if not tech_to_load:
                self.signalLog.emit(f"> CH {ch}: no valid techniques to load, skipping.")
                continue

            for index, (tech_file, ecc_parms) in enumerate(tech_to_load):
                first = index == 0
                last = index == len(tech_to_load) - 1
                self.api.LoadTechnique(self.id_, ch, tech_file, ecc_parms, first=first, last=last, display=(verbosity > 1))

            self.channel_params[ch] = sequence_ch
            loaded_channels.append(ch)

        if not loaded_channels:
            self.signalLog.emit("> No channels loaded with valid techniques.")
            return

        if len(loaded_channels) == 1:
            ch = loaded_channels[0]
            self.api.StartChannel(self.id_, ch)
            if self.timer_record[ch].isActive():
                self.timer_record[ch].stop()
            self.timer_record[ch].start()
        else:
            channel_map = self.api.channel_map(set(loaded_channels))
            self.api.StartChannels(self.id_, channel_map)
            for ch in loaded_channels:
                if self.timer_record[ch].isActive():
                    self.timer_record[ch].stop()
                self.timer_record[ch].start()

        self.channel = loaded_channels[0]
        for ch in loaded_channels:
            self.channel_is_running[ch] = True

    @errorDeco(signal='self.signalLog')
    def recordData(self, channel):
        data = self.api.GetData(self.id_, channel)
        current_values, data_info, _ = data
        tech_index=data_info.TechniqueIndex

        sequence_ch = self.channel_params.get(channel, None)
        if not sequence_ch:
            self.signalLog.emit(f"> CH {channel}: no loaded sequence .")
            return

        if tech_index <= 0 or tech_index > len(sequence_ch):
            self.signalLog.emit(f"> CH {channel}: technique index {tech_index} out of range (1..{len(sequence_ch)}).")
            return

        tech_params = sequence_ch[tech_index - 1]
        loop = tech_params.get('loop', [])
        exp_name = tech_params.get('name', 'step')
        
        filename=f'{self.filename_user}_CH{channel}_loop{loop}_{exp_name}.csv'
        status, tech_name = get_info_data(self.api, data)
        
        for output in get_experiment_data(self.api, data, tech_name, self.board_type):
            self._writeData(output, filename)

        if status == "STOP":
            self.timer_record[channel].stop()
            self.channel_is_running[channel] = False
            self.signalLog.emit(f"\nExperiment finished. Data recorded in {self.filename_user} series.")

    @errorDeco(signal='self.signalLog')
    def stopExperiment(self, channels):
        for ch in channels:
            if ch in self.timer_record and self.timer_record[ch].isActive() and isinstance(self.api, KBIO_api) and self.id_ is not None:
                self.api.StopChannel(self.id_, ch)
                self.timer_record[ch].stop()
                self.signalLog.emit(f"> Channel {ch} recording stopped.")
                self.channel_is_running[ch] = False
            
    @errorDeco(signal='self.signalLog')
    def disconnectDevice(self):
        if hasattr(self, "api") and isinstance(self.api, KBIO_api) and self.id_ is not None:
            self.api.Disconnect(self.id_)
            self.signalLog.emit("> Device disconnected.")
            self.signalFinished.emit()

    ##=====================================================================================##
    # Helper functions
    ##=====================================================================================##

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
    
    def _writeData(self, output, filename: str):
        if isinstance(output, dict):
            values = output.values()
        elif isinstance(output, (list, tuple)):
            values = output
        else:
            values = [output]

        data_line = ','.join(str(item) for item in values) + '\n'
        with open(filename, 'a', encoding='utf-8') as data_file:
            data_file.write(data_line)

    