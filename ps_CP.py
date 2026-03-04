import sys

import kbio.kbio_types as KBIO
from kbio.kbio_tech import ECC_parm
from kbio.kbio_tech import make_ecc_parm
from kbio.kbio_tech import make_ecc_parms

def cp_parm(board_type, api, cp_param):

    #==============================================================================#
    #Each technique has a specific file and they depend on the potentiostat board
    # They all have the same syntax: the technique name + a number '{technique_name}{digit}.ecc'
    #==============================================================================#
    tech_file = None
    match board_type:
        case KBIO.BOARD_TYPE.ESSENTIAL.value:
            tech_file = f'cp.ecc'
        case KBIO.BOARD_TYPE.PREMIUM.value:
            tech_file = f'cp.ecc'
        case KBIO.BOARD_TYPE.DIGICORE.value:
            tech_file = f'cp.ecc'
        case _:
            print("> Board type detection failed")
            sys.exit(-1)

    #==============================================================================#
    # Dictionary of all parameters labels needed for the technique
    # They serve to create pointer for the ecc file using the make_ecc_parm method 
    # The Label text need to be exact from the manual or it won't work!
    #==============================================================================#

    CP_parms = {
    "current_step": ECC_parm("Current_step", float),
    "step_duration": ECC_parm("Duration_step", float),
    "vs_init": ECC_parm("vs_initial", bool),
    "nb_steps": ECC_parm("Step_number", int),
    "record_dt": ECC_parm("Record_every_dT", float),
    "record_dE": ECC_parm("Record_every_dE", float),
    "repeat": ECC_parm("N_Cycles", int),
    "I_range": ECC_parm("I_Range", int),
    }

    #==============================================================================#
    # Creating the ecc_parms for LoadTechnique method of api instance of kbio.kbio_api
    #==============================================================================#

    p_current_step = make_ecc_parm(api, CP_parms["current_step"], cp_param['current'])
    p_step_duration = make_ecc_parm(api, CP_parms["step_duration"], cp_param['duration'])
    p_vs_init = make_ecc_parm(api, CP_parms["vs_init"], cp_param['vs_init'])

    p_nb_steps = make_ecc_parm(api, CP_parms["nb_steps"], 0)

    p_record_dt = make_ecc_parm(api, CP_parms["record_dt"], cp_param['record_dt'])
    p_record_dE = make_ecc_parm(api, CP_parms["record_dE"], cp_param['record_dE'])

    p_repeat = make_ecc_parm(api, CP_parms["repeat"], cp_param['repeat_count'])

    i_range = cp_param.get('i_range', None)
    if isinstance(i_range, str):
        i_range_value = KBIO.I_RANGE[i_range].value if i_range in KBIO.I_RANGE.__members__ else KBIO.I_RANGE.I_RANGE_AUTO.value
    else:
        i_range_value = getattr(i_range, 'value', KBIO.I_RANGE.I_RANGE_AUTO.value)
    p_I_range = make_ecc_parm(api, CP_parms["I_range"], i_range_value)

    ecc_parms = make_ecc_parms(api, p_current_step, p_step_duration, p_vs_init, p_nb_steps, p_record_dt, p_record_dE, p_I_range, p_repeat)

    if tech_file:
        if ecc_parms:
            return tech_file, ecc_parms
    else:
        print('Issues with defining parameters')