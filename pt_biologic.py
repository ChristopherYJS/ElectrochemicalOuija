#####################################################################
# This document is a part of the BioLogic OEM Package and is
# protected by the terms of the OEM Package licence as well as
# other intellectual property rights owned by BioLogic SAS.
# This document may only be used for non-commercial purposes
# such as for the integration of BioLogic equipment to larger
# technical solutions manufactured  and/or delivered to end-users.
#####################################################################

import os
import sys
import time

import matplotlib.pyplot as plt
import numpy as np

import kbio.kbio_types as KBIO
from kbio.c_utils import c_is_64b
from kbio.kbio_api import KBIO_api
from kbio.kbio_tech import get_experiment_data
from kbio.kbio_tech import get_info_data
from kbio.utils import exception_brief

from CA_biologic import ca_parm
from OCV_biologic import ocv_parm
from CP_biologic import cp_parm
from CV_biologic import cv_parm

from PySide6.QtCore import Signal,QObject,QTimer

from misc_handleException import errorDeco

class Biologic(QObject):
    signalLog=Signal(str)
    def __init__(self, address,binary_path,channel):
        super().__init__()
        self.recordTimer=QTimer()
        self.recordTimer.setInterval(1000)
        self.recordTimer.timeout.connect(self.recordData)
        self.address=address
        self.binary_path=binary_path
        self.channel=channel

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
                self.signalLog.emit("> Board type detection failed")
        # Load firmware
        self.signalLog.emit(f"> Loading {firmware_path} ...")
        # create a map from channel set
        channel_map = self.api.channel_map({self.channel})
        # BL_LoadFirmware
        self.api.LoadFirmware(self.id_, channel_map, firmware=firmware_path, fpga=fpga_path, force=self.force_load_firmware)
        self.signalLog.emit("> ... firmware loaded")

        # BL_GetChannelInfos
        channel_info = self.api.GetChannelInfo(self.id_, self.channel)
        self.signalLog.emit(f"> Channel {self.channel} info :")
        self.signalLog.emit(channel_info)

        if not channel_info.is_kernel_loaded:
            self.signalLog.emit("> kernel must be loaded in order to run the experiment")

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
                        self.logMsg.emit(f"Technique: {measurement} at Step:{tech_count} is not an valid technique")
                # BL_LoadTechnique
                if len(sequence) == 1:
                    self.api.LoadTechnique(self.id_, self.channel, tech_file, ecc_parms, first=True, last=True, display=(verbosity > 1))
                elif tech_count == 1:
                    self.api.LoadTechnique(self.id_, self.channel, tech_file, ecc_parms, first=True, last=False, display=(verbosity > 1))
                elif tech_count == len(sequence):
                    self.api.LoadTechnique(self.id_, self.channel, tech_file, ecc_parms, first=False, last=True, display=(verbosity > 1))
                else:
                    self.api.LoadTechnique(self.id_, self.channel, tech_file, ecc_parms, first=False, last=False, display=(verbosity > 1))
            # BL_StartChannel
            self.api.StartChannel(self.id_, self.channel)
            # Defaut filename with timestamp ******to be changed with user input in the future
            self.filename=f"{time.strftime('%Y%m%d')}-result.csv"
            self.current_tech=None

    @errorDeco(signal='self.signalLog')
    def recordData(self):
        with open(self.filename, 'w') as data_file:
            data = self.api.GetData(self.id_, self.channel)
            status, tech_name = get_info_data(self.api, data)
            print(".", end="", flush=True)

            for output in get_experiment_data(self.api, data, tech_name, self.board_type):

                if self.current_tech != tech_name:
                    print(tech_name, end="", flush=True)
                    self.current_tech = tech_name
                    data_keys = list(output.keys())
                    data_keys.append('Technique')
                    data_file.write(','.join(data_keys) + '\n')

                x.append(output['Ewe'])
                y.append(output['Iwe'])
                data_line= ','.join(str(item) for item in output.values())
                data_line+= f',{tech_name}'
                data_line+= '\n'
                data_file.write(data_line)
                count+=1

            if status == "STOP":
                    self.recordTimer.stop()
                    self.logMsg.emit(f"\nExperiment finished. Data recorded in {self.filename}")
    def writeData(self):
        pass