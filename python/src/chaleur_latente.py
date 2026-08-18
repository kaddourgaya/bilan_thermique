import numpy as np

def es_eau_goff_gratch_murray(T: float) -> float:
    """
    Pression vapeur saturante es(T) pour surface EAU (Pa)
    Eq. (21) Ding et al. (2026) – Goff-Gratch-Murray
    T en Kelvin (TwK = Tw + 273.16)
    """
    TwK = T + 273.16

    term1 = 7.95357242e1
    part1 = 18.1972839 * (TwK - 273.16) / 373.16
    part2 = - 20242.1852 / TwK
    part3 = 26.1205253 * (TwK / 373.16)
    part4 = 58.0691913 * (TwK / 373.16)**2
    part5 = - 8.039282 * (TwK / 373.16)**3
    part6 = 5.02808 * np.log(TwK / 373.16)

    return term1 * np.exp(part1 + part2 + part3 + part4 + part5 + part6)


def es_glace_goff_gratch_murray(T: float) -> float:
    """
    Pression vapeur saturante es(T) pour surface GLACE (Pa)
    Eq. (22) Ding et al. (2026) – Goff-Gratch-Murray
    T en Kelvin (TisK = Tis + 273.16)
    """
    Tk = T + 273.16

    term1 = 5.75185606e10
    part1 = 20.947013 * (Tk - 273.16) / 373.16
    part2 = 3.56654 * np.log(Tk / 373.16)
    part3 = 2.01889049 * (273.16 / Tk)

    return term1 * np.exp(part1 + part2 + part3)


def chaleur_latente(Ts: float, Ta: float, va: float, HR: float, surface: str) -> float:
    """
    Chaleur latente φl (W/m²)
    Rimsha-Donchenko (1957) – Eq. (24) Ding et al. (2026)
    φl = (4.1855 / 8.64) * (1.56 * kn + 6.08 * va) * (es - ea)
    es, ea en Pa (comme dans Ding 2026)
    surface = "eau" ou "glace"
    """
    kn = 8.0 + 0.35 * (Ts - Ta)

    # es(Ts) selon type de surface
    if surface == "eau":
        es = es_eau_goff_gratch_murray(Ts)      # Pa
    else:
        es = es_glace_goff_gratch_murray(Ts)    # Pa

    # ea(Ta) avec humidité relative
    ea = es_eau_goff_gratch_murray(Ta) * HR / 100.0  # Pa

    return (4.1855 / 8.64) * (1.56 * kn + 6.08 * va) * (es - ea)
