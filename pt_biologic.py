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
    signalChannels=Signal(list)
    def __init__(self, address,binary_path,channel):
        super().__init__()
        self.recordTimer=QTimer()
        self.recordTimer.setInterval(1000)
        self.recordTimer.timeout.connect(self.recordData)
        self.address=address
        self.binary_path=binary_path
        self.channel=channel
        self.api = None
        self.id_ = None
        self.is_running = False

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
        # based on board_type, determine firmware filenames
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
        # Load firmware
        self.signalLog.emit(f"> Loading {firmware_path} ...")
        # create a map from channel set
        channel_map = self.api.channel_map({self.channel})
        print(channel_map)
        # BL_LoadFirmware
        self.api.LoadFirmware(self.id_, channel_map, firmware=firmware_path, fpga=fpga_path, force=self.force_load_firmware)
        self.signalLog.emit("> ... firmware loaded")

        # BL_GetChannelInfos
        channel_info = self.api.GetChannelInfo(self.id_, self.channel)
        self.signalLog.emit(f"> Channel {self.channel} info :")
        self.signalLog.emit(f"{channel_info}")

        if not channel_info.is_kernel_loaded:
            self.signalLog.emit("> kernel must be loaded in order to run the experiment, potentiostat thread terminated.")
            self.signalFinished.emit()
            return
        
        # Get available current ranges for this device
        self.current_ranges = self._get_enum_range(KBIO.I_RANGE, channel_info.MinIRange, channel_info.MaxIRange)+["I_RANGE_AUTO"]
        
        # Get available bandwidth options (min is always BW_1)
        self.bandwidths = self._get_enum_range(KBIO.BANDWIDTH, 1, channel_info.MaxBandwidth)
        
        # Get all potential ranges (no device limits)
        self.potential_ranges = self._get_all_enum_options(KBIO.E_RANGE)
        
        # Emit signals to main window for display
        self.signalConnected.emit([self.channel,self.current_ranges,self.potential_ranges,self.bandwidths])

    @errorDeco(signal='self.signalLog')
    def runSequence(self,sequence):
        #check if potentiostat is connected and kernel is loaded
        if not hasattr(self, "api") or not self.api:
            self.signalLog.emit("> Device not connected. Please connect to the device first.")
            return
        else:
            verbosity = 1
            tech_count = 0
            for measurement in sequence:
                match measurement['technique']:
                    case 'ca':
                        tech_file, ecc_parms = ca_parm(self.board_type, self.api, measurement)
                        tech_count +=1
                    case 'ocv':
                        tech_file, ecc_parms = ocv_parm(self.board_type, self.api, measurement)
                        tech_count += 1
                    case 'cv':
                        tech_file, ecc_parms = cv_parm(self.board_type, self.api, measurement)
                        tech_count += 1
                    case 'cp':
                        tech_file, ecc_parms = cp_parm(self.board_type, self.api, measurement)
                        tech_count += 1
                    case _:
                        self.signalLog.emit(f"Technique: {measurement} at Step:{tech_count} is not an valid technique")
                # BL_LoadTechnique
                if len(sequence) == 1:
                    self.api.LoadTechnique(self.id_, self.channel, tech_file, ecc_parms, first=True, last=True, display=(verbosity > 1))
                elif tech_count == 1:
                    self.api.LoadTechnique(self.id_, self.channel, tech_file, ecc_parms, first=True, last=False, display=(verbosity > 1))
                elif tech_count == len(sequence):
                    self.api.LoadTechnique(self.id_, self.channel, tech_file, ecc_parms, first=False, last=True, display=(verbosity > 1))
                else:
                    self.api.LoadTechnique(self.id_, self.channel, tech_file, ecc_parms, first=False, last=False, display=(verbosity > 1))
            
            # Prompt user for save location and filename
            self.filename = self._get_save_filename()
            if not self.filename:
                self.signalLog.emit("> Data file save cancelled. Experiment not started.")
                return
            
            # BL_StartChannel
            self.api.StartChannel(self.id_, self.channel)
            if self.recordTimer.isActive():
                self.recordTimer.stop()
            self.recordTimer.start()
            self.is_running = True
            self.current_tech=None
            self.signalLog.emit(f"> Experiment started on channel {self.channel}.")

    @errorDeco(signal='self.signalLog')
    def recordData(self):
        data = self.api.GetData(self.id_, self.channel)
        print(data)
        status, tech_name = get_info_data(self.api, data)
        
        for output in get_experiment_data(self.api, data, tech_name, self.board_type):
            self.writeData(output, tech_name)
            self.signalData.emit(tech_name, output)

        if status == "STOP":
            self.recordTimer.stop()
            self.is_running = False
            self.signalLog.emit(f"\nExperiment finished. Data recorded in {self.filename} series.")

    @errorDeco(signal='self.signalLog')
    def stopExperiment(self, disconnect: bool = False):
        if self.recordTimer.isActive():
            self.recordTimer.stop()

        if self.api and self.id_ is not None and self.is_running:
            self.api.StopChannel(self.id_, self.channel)
            self.signalLog.emit(f"> Experiment stopped on channel {self.channel}.")

        self.is_running = False

        if disconnect and self.api and self.id_ is not None:
            self.api.Disconnect(self.id_)
            self.signalLog.emit(f"> Disconnected from device[{self.address}].")
            self.api = None
            self.id_ = None
            self.signalFinished.emit()
    
    def _get_save_filename(self) -> str:

        default_name = f"{time.strftime('%Y%m%d')}-result.csv"
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
    
    def writeData(self, output, tech_name: str):
        if not hasattr(self, "filename") or not self.filename:
            return

        if not hasattr(self, "current_tech"):
            self.current_tech = None

        if isinstance(output, dict):
            if self.current_tech != tech_name:
                self.current_tech = tech_name
                data_keys = list(output.keys())
                data_keys.append('Technique')
                with open(self.filename, 'a', encoding='utf-8') as data_file:
                    data_file.write(','.join(data_keys) + '\n')
            values = output.values()
        elif isinstance(output, (list, tuple)):
            values = output
        else:
            values = [output]

        data_line = ','.join(str(item) for item in values)
        data_line += f',{tech_name}\n'
        with open(self.filename, 'a', encoding='utf-8') as data_file:
            data_file.write(data_line)