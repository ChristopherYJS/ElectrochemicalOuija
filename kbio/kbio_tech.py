""" Bio-Logic OEM package python API.

This module contains support functions when building technique parameters,
and decoding experiment records.

"""

from dataclasses import dataclass

import kbio.kbio_types as KBIO
from kbio.tech_types import TECH_ID


@dataclass
class ECC_parm:
    """ECC param template"""

    label: str
    type_: type


#####################################################################
# This document is a part of the BioLogic OEM Package and is
# protected by the terms of the OEM Package licence as well as
# other intellectual property rights owned by BioLogic SAS.
# This document may only be used for non-commercial purposes
# such as for the integration of BioLogic equipment to larger
# technical solutions manufactured  and/or delivered to end-users.
#####################################################################
"""
functions to build the technique ECC parameters (structure+contents)
"""


def make_ecc_parm(api, ecc_parm, value=0, index=0):
    """Given an ECC_parm template, create and return an EccParam, with its value and optional index."""
    parm = KBIO.EccParam()
    # BL_Define<xxx>Parameter
    # .. value is converted to its proper type, which DefineParameter will use
    api.DefineParameter(ecc_parm.label, ecc_parm.type_(value), index, parm)
    return parm


def make_ecc_parms(api, *ecc_parm_list):
    """Create an EccParam array from an EccParam list, and return an EccParams refering to it."""
    nb_parms = len(ecc_parm_list)
    parms_array = KBIO.ECC_PARM_ARRAY(nb_parms)

    for i, parm in enumerate(ecc_parm_list):
        parms_array[i] = parm

    parms = KBIO.EccParams(nb_parms, parms_array)
    return parms


# function to handle records from a running experiment
def get_info_data(api, data, print=False):
    """Unpack the info data, decode it according to the technique, display it,
    then return the experiment status"""

    current_values, data_info, _ = data

    status = KBIO.PROG_STATE(current_values.State).name
    tech_name = TECH_ID(data_info.TechniqueID).name

    if print:
        # synthetic info for current record
        info = {
            "tb": current_values.TimeBase,
            "ix": data_info.TechniqueIndex,
            "tech": tech_name,
            "proc": data_info.ProcessIndex,
            "loop": data_info.loop,
            "skip": data_info.IRQskipped,
        }
        print("> data info :")
        print(info)
    return status, tech_name


def _decode_time_seconds(time_base, word0, word1):
    """Decode BioLogic timestamp words into seconds.

    The OEM buffer provides two 32-bit words for timestamp. Depending on
    board/firmware binding, the order can appear as (high, low) or (low, high),
    and ctypes words may be signed. This helper normalizes words to uint32 and
    chooses a consistent tick count.
    """

    w0 = int(word0) & 0xFFFFFFFF
    w1 = int(word1) & 0xFFFFFFFF

    ticks_hl = (w0 << 32) | w1
    ticks_lh = (w1 << 32) | w0

    if w0 == 0 and w1 != 0:
        ticks = ticks_hl
    elif w1 == 0 and w0 != 0:
        ticks = ticks_lh
    else:
        ticks = min(ticks_hl, ticks_lh)

    return float(time_base) * ticks


def get_experiment_data(api, data, tech_name, board_type):
    """Unpack the experiment data, decode it according to the technique, display it,
    then return the experiment status"""

    current_values, data_info, data_record = data

    ix = 0

    for _ in range(data_info.NbRows):
        if tech_name == "OCV":
            # progress through record
            inx = ix + data_info.NbCols

            # extract timestamp and one row
            t_high, t_low, *row = data_record[ix:inx]

            nb_words = len(row)
            if nb_words == 1:
                vmp3 = False
            elif nb_words == 2:
                vmp3 = True
            else:
                raise RuntimeError(f"{tech_name} : unexpected record length ({nb_words})")

            t = _decode_time_seconds(current_values.TimeBase, t_high, t_low)

            # Ewe is a float
            Ewe = api.ConvertChannelNumericIntoSingle(row[0], board_type)

            parsed_row = {"t": t, "Ewe": Ewe}

            if vmp3:
                # Ece is a float
                Ece = api.ConvertChannelNumericIntoSingle(row[1], board_type)
                parsed_row["Ece"] = Ece

        elif tech_name == "CP":
            inx = ix + data_info.NbCols
            t_high, t_low, *row = data_record[ix:inx]

            nb_words = len(row)
            if nb_words != 3:
                raise RuntimeError(f"{tech_name} : unexpected record length ({nb_words})")

            # Ewe is a float
            Ewe = api.ConvertChannelNumericIntoSingle(row[0], board_type)

            # current is a float
            Iwe = api.ConvertChannelNumericIntoSingle(row[1], board_type)

            # technique cycle is an integer
            cycle = row[2]

            t = _decode_time_seconds(current_values.TimeBase, t_high, t_low)

            parsed_row = {"t": t, "Ewe": Ewe, "Iwe": Iwe, "cycle": cycle}

        elif tech_name == "CA":
            inx = ix + data_info.NbCols
            t_high, t_low, *row = data_record[ix:inx]

            nb_words = len(row)
            if nb_words != 3:
                raise RuntimeError(f"{tech_name} : unexpected record length ({nb_words})")

            # Ewe is a float
            Ewe = api.ConvertChannelNumericIntoSingle(row[0], board_type)

            # current is a float
            Iwe = api.ConvertChannelNumericIntoSingle(row[1], board_type)

            # technique cycle is an integer
            cycle = row[2]

            t = _decode_time_seconds(current_values.TimeBase, t_high, t_low)

            parsed_row = {"t": t, "Ewe": Ewe, "Iwe": Iwe, "cycle": cycle}

        elif tech_name == "CV":
            inx = ix + data_info.NbCols
            t_high, t_low, *row = data_record[ix:inx]

            nb_words = len(row)
            if nb_words == 1:
                vmp3 = False
            elif nb_words == 2:
                vmp3 = True
            else:
                raise RuntimeError(f"{tech_name} : unexpected record length ({nb_words})")
            
            t = _decode_time_seconds(current_values.TimeBase, t_high, t_low)

            if vmp3:
                Ec= api.ConvertChannelNumericIntoSingle(row[0], board_type)
                I= api.ConvertChannelNumericIntoSingle(row[1], board_type)
                Ewe= api.ConvertChannelNumericIntoSingle(row[2], board_type)
                cycle=api.ConvertChannelNumericIntoSingle(row[3], board_type)
                parsed_row = {"t": t, "Ec": Ec, "I": I, "Ewe": Ewe, "cycle": cycle}
            else:
                I= api.ConvertChannelNumericIntoSingle(row[0], board_type)
                Ewe= api.ConvertChannelNumericIntoSingle(row[1], board_type)
                cycle=api.ConvertChannelNumericIntoSingle(row[2], board_type)
                parsed_row = {"t": t, "I": I, "Ewe": Ewe, "cycle": cycle}

        elif tech_name == "EIS":
            inx = ix + data_info.NbCols
            words = data_record[ix:inx]

            def _to_float(word):
                return api.ConvertChannelNumericIntoSingle(word, board_type)

            # PEIS data formats depend on ProcessIndex (per local EC-Lab Dev Package PDF).
            # - Process 0: time-domain samples: t_high, t_low, Ewe, I (, optional step)
            # - Process 1: frequency-domain points: freq, |Ewe|, |I|, Phase, Zwe, Ewe, I, ...
            parsed_row = {
                "process": int(data_info.ProcessIndex),
                "t": "",
                "Ewe": "",
                "I": "",
                "step": "",
                "freq": "",
                "abs_Ewe": "",
                "abs_I": "",
                "phase": "",
                "Zwe": "",
                "abs_Ece": "",
                "abs_Ice": "",
                "phase_ce": "",
                "Zce": "",
                "raw": "",
            }

            if data_info.ProcessIndex == 0:
                if len(words) < 4:
                    parsed_row["raw"] = ' '.join(f"0x{int(w) & 0xFFFFFFFF:08X}" for w in words)
                else:
                    t_high, t_low, *row = words
                    t = _decode_time_seconds(current_values.TimeBase, t_high, t_low)
                    try:
                        Ewe = _to_float(row[0])
                        Iwe = _to_float(row[1])
                        parsed_row["t"] = t
                        parsed_row["Ewe"] = Ewe
                        parsed_row["I"] = Iwe
                        if len(row) >= 3:
                            parsed_row["step"] = int(row[2])
                        if len(row) > 3:
                            parsed_row["raw"] = str(row[3:])
                    except Exception:
                        parsed_row["t"] = t
                        parsed_row["raw"] = str(row)

            elif data_info.ProcessIndex == 1:
                # Frequency-domain point. Not all series include the same columns (VMP3 adds Ece/Ice/Zce).
                # Decode the common leading fields when present.
                try:
                    if len(words) >= 1:
                        parsed_row["freq"] = _to_float(words[0])
                    if len(words) >= 2:
                        parsed_row["abs_Ewe"] = _to_float(words[1])
                    if len(words) >= 3:
                        parsed_row["abs_I"] = _to_float(words[2])
                    if len(words) >= 4:
                        parsed_row["phase"] = _to_float(words[3])
                    if len(words) >= 5:
                        parsed_row["Zwe"] = _to_float(words[4])
                    if len(words) >= 6:
                        parsed_row["Ewe"] = _to_float(words[5])
                    if len(words) >= 7:
                        parsed_row["I"] = _to_float(words[6])

                    # If additional columns exist, keep them (and decode common VMP3 extras when possible).
                    # PDF shows VMP3 can include: |Ece|, |Ice|, Phase, Zce
                    if len(words) >= 12:
                        parsed_row["abs_Ece"] = _to_float(words[8])
                        parsed_row["abs_Ice"] = _to_float(words[9])
                        parsed_row["phase_ce"] = _to_float(words[10])
                        parsed_row["Zce"] = _to_float(words[11])
                    if len(words) > 7:
                        parsed_row["raw"] = str(words[7:])
                except Exception:
                    parsed_row["raw"] = str(words)
        else:
            # besides the previous known techniques, this is provided
            # to show a raw dump of the record
            inx = ix + data_info.NbCols
            row = data_record[ix:inx]
            parsed_row = [f"0x{word:08X}" for word in row]

        yield parsed_row

        ix = inx
