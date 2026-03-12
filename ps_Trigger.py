import sys

import kbio.kbio_types as KBIO
from kbio.kbio_tech import ECC_parm
from kbio.kbio_tech import make_ecc_parm
from kbio.kbio_tech import make_ecc_parms


def trigger_parm(board_type, api, trigger_param):
    """Build Trigger In technique parameters.

    Based on the Trigger In section in the local EC-Lab Development Package PDF:
    TI(.ecc/.4/.5) with Trigger_Logic.
    """

    trigger_type = str(trigger_param.get('type', '')).strip().lower()
    if trigger_type in ('ti', 'trigger_in', 'in'):
        trigger_type = 'in'
    else:
        raise ValueError(f"Unsupported trigger type for ps_Trigger: {trigger_param.get('type')}")

    trigger_in_parms = {
        "logic": ECC_parm("Trigger_Logic", int),
    }

    match board_type:
        case KBIO.BOARD_TYPE.ESSENTIAL.value:
            tech_file = 'TI.ecc'
        case KBIO.BOARD_TYPE.PREMIUM.value:
            tech_file = 'TI4.ecc'
        case KBIO.BOARD_TYPE.DIGICORE.value:
            tech_file = 'TI5.ecc'
        case _:
            print("> Board type detection failed")
            sys.exit(-1)

    p_logic = make_ecc_parm(api, trigger_in_parms["logic"], int(trigger_param['logic']))
    ecc_parms = make_ecc_parms(api, p_logic)

    return tech_file, ecc_parms
