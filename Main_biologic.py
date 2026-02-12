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


# Test parameters, to be adjusted

verbosity = 1

# In the software, you might need to have input for changing address and channel
address = "192.168.2.2"
channel = 1

binary_path = os.environ.get("ECLIB_DIR", f"C:{os.sep}EC-Lab Development Package{os.sep}lib")

force_load_firmware = True

#==============================================================================#

# helper functions
def newline():
    print()

def print_exception(e):
    print(f"{exception_brief(e, verbosity>=2)}")

def print_messages(ch):
    """Repeatedly retrieve and print messages for a given channel."""
    while True:
        # BL_GetMessage
        msg = api.GetMessage(id_, ch)
        if not msg:
            break
        print(msg)

# determine library file according to Python version (32b/64b)

if c_is_64b:
    DLL_file = "EClib64.dll"
else:
    DLL_file = "EClib.dll"

DLL_path = f"{binary_path}{os.sep}{DLL_file}"

# ==============================================================================#

try:
    newline()

    # API initialize
    api = KBIO_api(DLL_path)

    # BL_GetLibVersion
    version = api.GetLibVersion()
    print(f"> EcLib version: {version}")
    newline()

    # BL_Connect
    id_, device_info = api.Connect(address)
    print(f"> device[{address}] info :")
    print(device_info)
    newline()

    # based on board_type, determine firmware filenames
    board_type = api.GetChannelBoardType(id_, channel)
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
            print("> Board type detection failed")
            sys.exit(-1)

     # Load firmware
    print(f"> Loading {firmware_path} ...")
    # create a map from channel set
    channel_map = api.channel_map({channel})
    # BL_LoadFirmware
    api.LoadFirmware(id_, channel_map, firmware=firmware_path, fpga=fpga_path, force=force_load_firmware)
    print("> ... firmware loaded")
    newline()

    # BL_GetChannelInfos
    channel_info = api.GetChannelInfo(id_, channel)
    print(f"> Channel {channel} info :")
    print(channel_info)
    newline()

    if not channel_info.is_kernel_loaded:
        print("> kernel must be loaded in order to run the experiment")
        sys.exit(-1)

    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    #From now on code is specific to each technique because they require different parameters but the basic structure is the same.
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # ==============================================================================#
    # Loading parameter and starting technique
    # ==============================================================================#
    
    # ==============================================================================#
    # Template for setting up OCV measurement
    # ==============================================================================#
    ocv_settings= { 'technique': 'ocv', # Technique identifier
                 'duration': 10, # Duration of OCV measurement in s
                 'record_dt': 0.1, # Record potential at each time increment in s
                 'record_dE': 1, # Record potential at each potential increment in V
                 'e_range': "E_RANGE_10V"} # Potential range for OCV measurement
    
    # ==============================================================================#
    # Template for setting Chronoamperometry measurement
    # ==============================================================================#

    ca_settings= { 'technique': 'ca', # Technique identifier
                'voltage': 0.5, # Voltage applied in V vs ref
                'duration': 10, # Duration of CA measurement in s
                'vs_init': False, # Voltage step vs initial one
                'repeat_count': 1, # Repetition of measurement
                'record_dt': 0.1, # Record potential at each time increment in s
                'record_dI': 0.001, # Record potential at each potential increment in A
                'i_range': "I_RANGE_10mA", # Current range for CA measurement
                'charge': 64, # Record total charge
                'timebase': 0.000026
                   }
    
    # ==============================================================================#
    # Template for setting Cyclic Voltametry measurement
    # ==============================================================================#

    cv_settings= {'technique': 'cv', # Technique identifier
                  'Ei': 0, # Initial voltage vs OCP
                  'E1': 0.5, # 1st vertex voltage vs OCP
                  'E2': -0.5, # 2nd vertex voltage vs OCP
                  'Ef': 0, # Final voltage vs OCP
                  'scan_rate': 0.1, # Scan rate in V/s
                  'scan_number': 2, # I don't know what this do yet
                  'record_dE': 0.0005, # Record every potential step (V)
                  'N_cycles': 1, # Repeat cycles between E1 and E2
                  'average_dE': True, #Averaging voltage step True or False
                  'begin_step': 0.5, #Averaging from what part of the voltage step 0-> beginning, 1-> end
                  'end_step': 1 #Averaging from what part of the voltage step 0-> beginning, 1-> end
                   }
    
    # ==============================================================================#
    # Template for setting Trigger
    # ==============================================================================#

    trigger_settings= {'technique': 'trigger', # Technique identifier (str)
                        'type': 'out', # Type of trigger (str: 'out' for Trigger Out and 'in' for Trigger In )
                        'logic': 0, # High or low logic 0 or 1 (int)
                        'duration': 10, # Duration of trigger pulse (float in s) (Duration of pulse in only applicable for Trigger Out)
                   }

    # ==============================================================================#
    # Returning proper tech_file and ecc_parms based on specific technique.
    # Loading multiple technique by inserting the technique parameters in the measurement list
    # ==============================================================================#
    measurement_list = [cv_settings]
    tech_count = 0

    for measurement in measurement_list:

        match measurement['technique']:
            case 'ca':
                tech_file, ecc_parms= ca_parm(board_type, api, measurement)
                tech_count +=1
            
            case 'ocv':
                tech_file, ecc_parms= ocv_parm(board_type, api, measurement)
                tech_count += 1

            case 'cv':
                tech_file, ecc_parms = cv_parm(board_type, api, measurement)
                tech_count += 1

            case 'cp':
                tech_count += 1

            case _:
                print("> Invalid technique")

        # BL_LoadTechnique
        if len(measurement_list) == 1:
            api.LoadTechnique(id_, channel, tech_file, ecc_parms, first=True, last=True, display=(verbosity > 1))

        elif tech_count == 1:
            api.LoadTechnique(id_, channel, tech_file, ecc_parms, first=True, last=False, display=(verbosity > 1))

        elif tech_count == len(measurement_list):
            api.LoadTechnique(id_, channel, tech_file, ecc_parms, first=False, last=True, display=(verbosity > 1))

        else:
            api.LoadTechnique(id_, channel, tech_file, ecc_parms, first=False, last=False, display=(verbosity > 1))

    # BL_StartChannel
    api.StartChannel(id_, channel)

    # ==============================================================================#
    # experiment loop: 
    # ==============================================================================#
    filename= 'cv_test.csv'
    count=0
    current_tech= None
    print("> Measuring ", end="", flush=True)
    x=[]
    y=[]

    with open(filename, 'w') as data_file:

        while True:
            # BL_GetData
            data = api.GetData(id_, channel)
            status, tech_name = get_info_data(api, data)
            print(".", end="", flush=True)

            for output in get_experiment_data(api, data, tech_name, board_type):

                if current_tech != tech_name:
                    print(tech_name, end="", flush=True)
                    current_tech = tech_name
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
                break

            time.sleep(1)

    plt.plot(x,y)
    plt.show()

    print()
    print(f"> {count} data have been written into {filename}")
    print("> experiment done")
    newline()

    # BL_Disconnect
    api.Disconnect(id_)

except KeyboardInterrupt:
    print(".. interrupted")

except Exception as e:
    print_exception(e)