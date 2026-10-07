import numpy as np

def es_eau_goff_gratch_murray(T):
    """
    Pression de vapeur saturante au-dessus de l'eau libre (hPa).
    """
    return 6.1078 * np.exp((17.27 * T) / (T + 237.3))


def es_glace_goff_gratch_murray(T):
    """
    Pression de vapeur saturante au-dessus de la glace (hPa).
    """
    return 6.1078 * np.exp((21.875 * T) / (T + 265.5))


def chaleur_latente(Ts, Ta, va, HR, surface="eau", Pa=1013.25):
    """
    Calcule le flux de chaleur latente pour une surface d'eau libre ou de glace.
    """
    if surface == "eau":
        # Surface d'eau libre
        Kn = 8 + 0.35 * (Ts - Ta)
        es = 0.611 * np.exp((17.27 * Ta) / (Ta + 237.3))
        ea = es * (HR / 100.0)
        
        phi_l = (4.1855 / 8.64) * (1.56 * Kn + 6.08 * va) * (es - ea)
        return phi_l

    elif surface == "glace":
        # Surface de glace (Sublimation)
        rho_a = 1.293   # Densité de l'air (kg/m³)
        Ls = 2.83e6     # Chaleur latente de sublimation (J/kg)
        Kv = 0.001      # Coefficient d'échange turbulent
        Ua = va         # Vitesse du vent
        Us = 0.0        # Vitesse à la surface
        
        # Pression de vapeur saturante et réelle de l'air (en hPa)
        es_a = es_eau_goff_gratch_murray(Ta)
        ea = (HR / 100.0) * es_a
        
        # Humidité spécifique de l'air qa (kg/kg)
        qa = (0.622 * ea) / (Pa - 0.378 * ea)
        
        # Pression de vapeur saturante et humidité spécifique à la surface de la glace qs
        es_s = es_glace_goff_gratch_murray(Ts)
        qs = (0.622 * es_s) / (Pa - 0.378 * es_s)
        
        # Flux de chaleur latente de sublimation Ql (W/m²)
        Ql = rho_a * Ls * Kv * (Ua - Us) * (qa - qs)
        return Ql

    else:
        raise ValueError("Le paramètre surface doit être 'eau' ou 'glace'.")