import numpy as np


# ============================================================
# 1. Eq. 21 — Surface EAU
# ============================================================

def es_eau_goff_gratch_murray(Tc: float) -> float:
    Tk = Tc + 273.16

    return (
        7.95357242e10
        * np.exp(
            -18.1972839 * (373.16 / Tk)
            + 5.02808 * np.log(373.16 / Tk)
            - 20242.1852 * np.exp(-26.1205253 * Tk / 373.16)
            + 58.0691913 * np.exp(-8.039282 * (373.16 / Tk))
        )
    )


# ============================================================
# 2. Eq. 22 — Surface GLACE
# ============================================================

def es_glace_goff_gratch_murray(Tc: float) -> float:
    Tk = Tc + 273.16

    return (
        5.75185606e10
        * (
            -20.947013 * (373.16 / Tk)
            - 3.56654 * np.log(373.16 / Tk)
            - 2.01889049 * (273.16 / Tk)
        )
    )


# ============================================================
# 3. Chaleur latente — Rimsha–Donchenko (1957)
# ============================================================

def chaleur_latente(
    Ts: float,
    Ta: float,
    va: float,
    HR: float,
    surface: str
) -> float:

    Kn = 8.0 + 0.35 * (Ts - Ta)

    if surface == "eau":
        es = es_eau_goff_gratch_murray(Ts)
        ea_sat = es_eau_goff_gratch_murray(Ta)

    elif surface == "glace":
        es = es_glace_goff_gratch_murray(Ts)
        ea_sat = es_glace_goff_gratch_murray(Ta)

        print("----- DEBUG GLACE -----")
        print("Ts :", Ts)
        print("Ta :", Ta)
        print("HR :", HR)
        print("es glace :", es)
        print("ea_sat glace :", ea_sat)

    else:
        raise ValueError("surface doit être 'eau' ou 'glace'")

    ea = ea_sat * HR / 100.0

    if surface == "glace":
        print("ea glace :", ea)
        print("es - ea :", es - ea)
        print("----------------------")

    phi_l = (
        4.1855 / 8.64
        * (1.56 * Kn + 6.08 * va)
        * (es - ea)
    )

    return phi_l


# ============================================================
# 4. Chaleur latente avec fraction de glace Fi
# ============================================================

def chaleur_latente_totale(
    Tw: float,
    Tis: float,
    Ta: float,
    va: float,
    HR: float,
    Fi: float
) -> float:

    if Fi < 0.0 or Fi > 1.0:
        raise ValueError("Fi doit être compris entre 0 et 1.")

    # --------------------------------------------------------
    # Fi = 0 : surface entièrement en eau
    # --------------------------------------------------------

    if Fi == 0.0:
        return chaleur_latente(
            Ts=Tw,
            Ta=Ta,
            va=va,
            HR=HR,
            surface="eau"
        )

    # --------------------------------------------------------
    # Partie eau
    # --------------------------------------------------------

    phi_eau = chaleur_latente(
        Ts=Tw,
        Ta=Ta,
        va=va,
        HR=HR,
        surface="eau"
    )

    # --------------------------------------------------------
    # Partie glace
    # --------------------------------------------------------

    phi_glace = chaleur_latente(
        Ts=Tis,
        Ta=Ta,
        va=va,
        HR=HR,
        surface="glace"
    )

    # --------------------------------------------------------
    # Pondération par les fractions de surface
    # --------------------------------------------------------

    phi_l = (
        (1.0 - Fi) * phi_eau
        + Fi * phi_glace
    )

    return phi_l