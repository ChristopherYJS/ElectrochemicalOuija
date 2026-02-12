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

from misc_PrintException import print_ex

from PySide6.QtCore import Signal,QObject

class Biologic(QObject):
    logMsg=Signal(str)
    logEx=Signal(Exception)
    raiseEx=Signal()
    def __init__(self, address,binary_path,channel):
        super().__init__()
        self.address=address
        self.binary_path=binary_path
        self.channel=channel

        self.force_load_firmware=True
        if c_is_64b:
            DLL_file = "EClib64.dll"
        else:
            DLL_file = "EClib.dll"

        self.DLL_path = f"{binary_path}{os.sep}{DLL_file}"

    def connectDevice(self):
        try:
            # API initialize
            api = KBIO_api(self.DLL_path)
            # BL_GetLibVersion
            version = api.GetLibVersion()
            self.logMsg.emit(f"> EcLib version: {version}")
            # BL_Connect
            id_, device_info = api.Connect(self.address)
            self.logMsg.emit(f"> device[{self.address}] info :")
            self.logMsg.emit(f"{device_info}")
            # based on board_type, determine firmware filenames
            board_type = api.GetChannelBoardType(id_, self.channel)
            match board_type:
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
                    self.logMsg.emit("> Board type detection failed")
                    self.raiseEx.emit()

            # Load firmware
            self.logMsg.emit(f"> Loading {firmware_path} ...")
            # create a map from channel set
            channel_map = api.channel_map({self.channel})
            # BL_LoadFirmware
            api.LoadFirmware(id_, channel_map, firmware=firmware_path, fpga=fpga_path, force=self.force_load_firmware)
            self.logMsg.emit("> ... firmware loaded")

            # BL_GetChannelInfos
            channel_info = api.GetChannelInfo(id_, self.channel)
            self.logMsg.emit(f"> Channel {self.channel} info :")
            self.logMsg.emit(channel_info)

            if not channel_info.is_kernel_loaded:
                self.logMsg.emit("> kernel must be loaded in order to run the experiment")
                self.raiseEx.emit()
        except Exception as ex:
            self.logEx.emit(ex)
