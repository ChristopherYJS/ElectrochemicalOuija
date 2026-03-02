import sys

import kbio.kbio_types as KBIO
from kbio.kbio_tech import ECC_parm
from kbio.kbio_tech import make_ecc_parm
from kbio.kbio_tech import make_ecc_parms

def trigger_parm(board_type, api, trigger_param):

    #==============================================================================#
    # Dictionary of all parameters labels needed for the technique
    # They serve to create pointer for the ecc file using the make_ecc_parm method 
    # The Label text need to be exact from the manual or it won't work!
    #==============================================================================#

    CP_parms = {
        "logic": ECC_parm("Trigger_Logic", int),
        "duration": ECC_parm("Trigger_Duration", float),
    }

    #==============================================================================#
    # Creating the ecc_parms for LoadTechnique method of api instance of kbio.kbio_api
    #==============================================================================#

    p_logic= make_ecc_parm(api, CP_parms["logic"], trigger_param['logic'])
    
    if trigger_param['type'] == 'out':
        p_duration= make_ecc_parm(api, CP_parms["duration"], trigger_param['duration'])

        match board_type:

            case KBIO.BOARD_TYPE.ESSENTIAL.value:
                tech_file = f'TO.ecc'
            case KBIO.BOARD_TYPE.PREMIUM.value:
                tech_file = f'TO4.ecc'
            case KBIO.BOARD_TYPE.DIGICORE.value:
                tech_file = f'TO5.ecc'
            case _:
                print("> Board type detection failed")
                sys.exit(-1)
    
    elif trigger_param['type'] == 'in':
        match board_type:

            case KBIO.BOARD_TYPE.ESSENTIAL.value:
                tech_file = f'TI.ecc'
            case KBIO.BOARD_TYPE.PREMIUM.value:
                tech_file = f'TI4.ecc'
            case KBIO.BOARD_TYPE.DIGICORE.value:
                tech_file = f'TI5.ecc'
            case _:
                print("> Board type detection failed")
                sys.exit(-1)

    # make the technique parameter array
    ecc_parms = make_ecc_parms(api, p_logic, p_duration)

    try:
        return tech_file, ecc_parms

    except:
        print('Issue with ...')
