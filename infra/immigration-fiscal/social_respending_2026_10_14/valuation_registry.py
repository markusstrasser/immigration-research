"""One mortality basis and discount rate across every channel in a joint stack."""
from __future__ import annotations
from pathlib import Path
from functools import lru_cache
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "crime_victim_cost_2026_09_23"))
import vsl_standard as V

CHANNELS = frozenset(("crime", "pm25", "road_crash"))


@lru_cache(maxsize=1)
def verified_vsl():
    # Raw evidence is read-only during a run. Verify its full source set once,
    # rather than rehashing the same primary files in every factorial cell.
    V.check_pins()
    return V.dot_vsl()


def mortality_registry(basis, rate, declarations):
    vsl = verified_vsl()
    if basis not in ("dot_uniform", "dot_life_years"):
        raise ValueError("[BLOCKED] unknown mortality valuation basis")
    rate = float(rate)
    if rate not in (0., .03) or (basis == "dot_uniform" and rate != 0.):
        raise ValueError("[BLOCKED] unsupported mortality discount rate")
    if set(declarations) != CHANNELS:
        raise ValueError("[BLOCKED] joint stack needs crime, PM and crash mortality declarations")
    for channel, declaration in declarations.items():
        if declaration["valuation"] != basis or float(declaration["real_discount_rate"]) != rate:
            raise ValueError(f"[BLOCKED] mixed mortality valuation in {channel}")
    channels = {channel:dict(valuation=declaration["valuation"],real_discount_rate=float(declaration["real_discount_rate"]))
                for channel,declaration in declarations.items()}
    return dict(valuation=basis, real_discount_rate=rate, channels=channels,
                uniform_vsl_usd=vsl if basis == "dot_uniform" else None,
                nonmortality="retained on each channel's declared resource/WTP basis")
