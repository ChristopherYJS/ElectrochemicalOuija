from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class AxisOption:
    key: str
    label: str
    source: str
    transform: str = "identity"


def _identity(value: float) -> float:
    return value


def _log10(value: float) -> float:
    if value <= 0:
        raise ValueError("log10 transform requires a positive value")
    return math.log10(value)


def _log10_abs(value: float) -> float:
    abs_value = abs(value)
    if abs_value <= 0:
        raise ValueError("log10_abs transform requires a non-zero value")
    return math.log10(abs_value)


TRANSFORMS: dict[str, Callable[[float], float]] = {
    "identity": _identity,
    "log10": _log10,
    "log10_abs": _log10_abs,
}


PLOT_AXIS_OPTIONS: dict[str, dict[str, list[AxisOption]]] = {
    "CA": {
        "x": [
            AxisOption("time", "Time (s)", "t"),
            AxisOption("log_time", "log10(Time)", "t", "log10"),
            AxisOption("potential", "Potential (V)", "Ewe"),
            AxisOption("current", "Current (A)", "Iwe"),
            AxisOption("log_current", "log10(|Current|)", "Iwe", "log10_abs"),
        ],
        "y": [
            AxisOption("current", "Current (A)", "Iwe"),
            AxisOption("log_current", "log10(|Current|)", "Iwe", "log10_abs"),
            AxisOption("potential", "Potential (V)", "Ewe"),
            AxisOption("time", "Time (s)", "t"),
            AxisOption("log_time", "log10(Time)", "t", "log10"),
        ],
    },
    "CV": {
        "x": [
            AxisOption("potential", "Potential (V)", "Ewe"),
            AxisOption("time", "Time (s)", "t"),
            AxisOption("log_time", "log10(Time)", "t", "log10"),
        ],
        "y": [
            AxisOption("current", "Current (A)", "Iwe"),
            AxisOption("log_current", "log10(|Current|)", "Iwe", "log10_abs"),
            AxisOption("potential", "Potential (V)", "Ewe"),
        ],
    },
    "CP": {
        "x": [
            AxisOption("time", "Time (s)", "t"),
            AxisOption("log_time", "log10(Time)", "t", "log10"),
            AxisOption("current", "Current (A)", "Iwe"),
            AxisOption("log_current", "log10(|Current|)", "Iwe", "log10_abs"),
        ],
        "y": [
            AxisOption("potential", "Potential (V)", "Ewe"),
            AxisOption("time", "Time (s)", "t"),
            AxisOption("log_time", "log10(Time)", "t", "log10"),
        ],
    },
    "EIS": {
        "x": [
            AxisOption("frequency", "Frequency (Hz)", "freq"),
            AxisOption("log_frequency", "log10(Frequency)", "freq", "log10"),
            AxisOption("z_real", "Z' (Ohm)", "z_real"),
        ],
        "y": [
            AxisOption("minus_z_imag", "-Z'' (Ohm)", "z_imag_neg"),
            AxisOption("z_magnitude", "|Z| (Ohm)", "z_abs"),
            AxisOption("phase", "Phase (deg)", "phase_deg"),
        ],
    },
}


TECHNIQUE_ALIASES: dict[str, str] = {
    "ca": "CA",
    "cv": "CV",
    "cp": "CP",
    "eis": "EIS",
    "CA": "CA",
    "CV": "CV",
    "CP": "CP",
    "EIS": "EIS",
}


def normalize_technique_name(name: str) -> str:
    return TECHNIQUE_ALIASES.get(name, name.upper())


def get_axis_options(technique: str) -> dict[str, list[AxisOption]]:
    return PLOT_AXIS_OPTIONS.get(normalize_technique_name(technique), {"x": [], "y": []})


def apply_axis_transform(transform: str, value: float) -> float:
    fn = TRANSFORMS.get(transform, _identity)
    return fn(value)
