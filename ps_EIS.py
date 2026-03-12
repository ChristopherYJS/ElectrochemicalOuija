import sys

import kbio.kbio_types as KBIO
from kbio.kbio_tech import ECC_parm
from kbio.kbio_tech import make_ecc_parm
from kbio.kbio_tech import make_ecc_parms


def eis_parm(board_type, api, eis_param):
    """Build parameters for PEIS (potentio EIS).

    Notes:
    - Parameter *labels* must match the OEM package exactly.
    - This implementation is based on the label names found in the local
      "EC-Lab Development Package" PDF in this repo.
    """

    # Each technique has a specific file and they depend on the potentiostat board.
    tech_file = None
    match board_type:
        case KBIO.BOARD_TYPE.ESSENTIAL.value:
            tech_file = "peis.ecc"
        case KBIO.BOARD_TYPE.PREMIUM.value:
            tech_file = "peis4.ecc"
        case KBIO.BOARD_TYPE.DIGICORE.value:
            tech_file = "peis5.ecc"
        case _:
            print("> Board type detection failed")
            sys.exit(-1)

    # Labels per EC-Lab Development Package (PEIS parameters)
    EIS_parms = {
        # DC step / settling
        "vs_initial": ECC_parm("vs_initial", bool),
        "initial_voltage_step": ECC_parm("Initial_Voltage_step", float),
        "duration_step": ECC_parm("Duration_step", float),
        "step_number": ECC_parm("Step_number", int),
        # record criteria
        "record_dt": ECC_parm("Record_every_dT", float),
        "record_dI": ECC_parm("Record_every_dI", float),
        # frequency sweep
        "final_frequency": ECC_parm("Final_frequency", float),
        "initial_frequency": ECC_parm("Initial_frequency", float),
        "sweep": ECC_parm("sweep", bool),
        "amplitude_voltage": ECC_parm("Amplitude_Voltage", float),
        "frequency_number": ECC_parm("Frequency_number", int),
        "average_n_times": ECC_parm("Average_N_times", int),
        # non-stationary handling
        "correction": ECC_parm("Correction", bool),
        "wait_for_steady": ECC_parm("Wait_for_steady", int),
    }

    # Map our UI/model keys -> PEIS ECC params
    dc_potential = eis_param.get("potential", 0.0)
    duration = eis_param.get("duration", 0.0)

    record_dt = eis_param.get("record_dt", eis_param.get("sample_time", 0.0))
    record_dI = eis_param.get("record_dI", eis_param.get("sample_current", 0.0))

    freq_init = eis_param.get("freq_init", eis_param.get("initial_frequency", 100000.0))
    freq_final = eis_param.get("freq_final", eis_param.get("final_frequency", 0.01))
    sweep_linear = bool(eis_param.get("sweep_linear", False))
    amplitude = eis_param.get("amplitude", 0.01)
    freq_number = int(eis_param.get("freq_number", eis_param.get("frequency_number", 50)))
    average = int(eis_param.get("average", 1))
    correction = bool(eis_param.get("correction", False))
    wait_for_steady = int(eis_param.get("correction_periods", eis_param.get("wait_for_steady", 0)) or 0)

    # DC step / settling
    p_vs_initial = make_ecc_parm(api, EIS_parms["vs_initial"], False)
    p_initial_voltage_step = make_ecc_parm(api, EIS_parms["initial_voltage_step"], dc_potential)
    p_duration_step = make_ecc_parm(api, EIS_parms["duration_step"], duration)

    # This UI currently supports a single DC step
    p_step_number = make_ecc_parm(api, EIS_parms["step_number"], 0)

    # record criteria
    p_record_dt = make_ecc_parm(api, EIS_parms["record_dt"], record_dt)
    p_record_dI = make_ecc_parm(api, EIS_parms["record_dI"], record_dI)

    # frequency sweep
    p_final_frequency = make_ecc_parm(api, EIS_parms["final_frequency"], freq_final)
    p_initial_frequency = make_ecc_parm(api, EIS_parms["initial_frequency"], freq_init)
    p_sweep = make_ecc_parm(api, EIS_parms["sweep"], sweep_linear)
    p_amplitude_voltage = make_ecc_parm(api, EIS_parms["amplitude_voltage"], amplitude)
    p_frequency_number = make_ecc_parm(api, EIS_parms["frequency_number"], freq_number)
    p_average_n_times = make_ecc_parm(api, EIS_parms["average_n_times"], average)

    # non-stationary handling
    p_correction = make_ecc_parm(api, EIS_parms["correction"], correction)
    p_wait_for_steady = make_ecc_parm(api, EIS_parms["wait_for_steady"], wait_for_steady)

    ecc_parms = make_ecc_parms(
        api,
        p_vs_initial,
        p_initial_voltage_step,
        p_duration_step,
        p_step_number,
        p_record_dt,
        p_record_dI,
        p_final_frequency,
        p_initial_frequency,
        p_sweep,
        p_amplitude_voltage,
        p_frequency_number,
        p_average_n_times,
        p_correction,
        p_wait_for_steady,
    )

    return tech_file, ecc_parms
