import sys
from dataclasses import dataclass

import kbio.kbio_types as KBIO
from kbio.kbio_tech import ECC_parm
from kbio.kbio_tech import make_ecc_parm
from kbio.kbio_tech import make_ecc_parms

def cp_parm(board_type, api):

    #==============================================================================#
    #Each technique has a specific file and they depend on the potentiostat board
    # They all have the same syntax: the technique name + a number '{technique_name}{digit}.ecc'
    #==============================================================================#
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
    # Defining parameters values
    # In the final code they should be assigned the associated value from the UI
    #==============================================================================#

    repeat_count = 2
    record_dt = 0.1  # seconds
    record_dE = 0.1  # Volts
    i_range = "I_RANGE_10mA"

    @dataclass
    class current_step:
        current: float
        duration: float
        vs_init: bool = False

    steps = [
    current_step(0.001, 2),  # 1mA during 2s
    current_step(0.002, 1),  # 2mA during 1s
    current_step(0.0005, 3, True),  # 0.5mA delta during 3s
    ]

    #==============================================================================#
    # Creating the ecc_parms for LoadTechnique method of api instance of kbio.kbio_api
    #==============================================================================#

    p_steps = list()

    for idx, step in enumerate(steps):
        parm = make_ecc_parm(api, CP_parms["current_step"], step.current, idx)
        p_steps.append(parm)
        parm = make_ecc_parm(api, CP_parms["step_duration"], step.duration, idx)
        p_steps.append(parm)
        parm = make_ecc_parm(api, CP_parms["vs_init"], step.vs_init, idx)
        p_steps.append(parm)

    # number of steps is one less than len(steps)
    p_nb_steps = make_ecc_parm(api, CP_parms["nb_steps"], idx)

    # record parameters
    p_record_dt = make_ecc_parm(api, CP_parms["record_dt"], record_dt)
    p_record_dE = make_ecc_parm(api, CP_parms["record_dE"], record_dE)

    # repeating factor
    p_repeat = make_ecc_parm(api, CP_parms["repeat"], repeat_count)
    p_I_range = make_ecc_parm(api, CP_parms["I_range"], KBIO.I_RANGE[i_range].value)

    ecc_parms = make_ecc_parms(api, *p_steps, p_nb_steps, p_record_dt, p_record_dE, p_I_range, p_repeat)

    return tech_file, ecc_parms