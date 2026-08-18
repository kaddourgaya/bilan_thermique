import math

def epaisseur_glace_croissance(alpha_h: float, AFDD: float) -> float:
    """
    Croissance thermique de la glace (m)
    Stefan (1889) + Michel (1971)
    η = αh * sqrt(AFDD)
    """
    return alpha_h * math.sqrt(AFDD)

def epaisseur_glace_fonte(eta_max: float, A: float, ATDD: float) -> float:
    """
    Fonte thermique de la glace (m)
    Bilello (1980)
    η = ηmax - A * ATDD
    """
    return max(0, eta_max - A * ATDD)

def choisir_hi(Fi: float, Ta: float, hi_mesure: float, hi_croissance: float, hi_fonte: float) -> float:
    """
    Choix de l'épaisseur de glace hi selon Fi et Ta.
    - Fi = 0 → hi = 0 (fin printemps / début été)
    - Fi > 0 & Ta < 0 → croissance (fin automne / début hiver)
    - Fi > 0 & Ta > 0 → fonte (début printemps)
    """
    if Fi <= 0:
        return 0
    if Ta < 0:
        return hi_croissance
    return hi_fonte

def temperature_surface_glace(ka: float, ki: float, hi: float, ha: float, Ta: float) -> float:
    """
    Température surface glace Tis (°C)
    Lian & Zhao (2011)
    Tis = (ka * hi) / (ka * hi + ki * ha) * Ta
    """
    return (ka * hi) / (ka * hi + ki * ha) * Ta
