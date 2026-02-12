import sys
from dataclasses import dataclass

import kbio.kbio_types as KBIO
from kbio.kbio_tech import ECC_parm
from kbio.kbio_tech import make_ecc_parm
from kbio.kbio_tech import make_ecc_parms

def cv_parm(board_type, api):

    #==============================================================================#
    #Each technique has a specific file and they depend on the potentiostat board
    # They all have the same syntax: the technique name + a number '{technique_name}{digit}.ecc'
    #==============================================================================#
    match board_type:

        case KBIO.BOARD_TYPE.ESSENTIAL.value:
            tech_file = f'cv.ecc'
        case KBIO.BOARD_TYPE.PREMIUM.value:
            tech_file = f'cv4.ecc'
        case KBIO.BOARD_TYPE.DIGICORE.value:
            tech_file = f'cv5.ecc'
        case _:
            print("> Board type detection failed")
            sys.exit(-1)

    #==============================================================================#
    # Dictionary of all parameters labels needed for the technique
    # They serve to create pointer for the ecc file using the make_ecc_parm method 
    # The Label text need to be exact from the manual or it won't work!
    #==============================================================================#