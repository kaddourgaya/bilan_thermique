import numpy as np

def es_eau_goff_gratch_murray(T):
    """
    Pression de vapeur saturante au-dessus de l'eau libre (hPa).
    Paramètre :
        T (float) : Température (°C)
    Retourne :
        float : Pression (hPa)
    """
    return 6.1078 * np.exp((17.27 * T) / (T + 237.3))


def es_glace_goff_gratch_murray(T):
    """
    Pression de vapeur saturante au-dessus de la glace (hPa).
    Paramètre :
        T (float) : Température (°C)
    Retourne :
        float : Pression (hPa)
    """
    return 6.1078 * np.exp((21.875 * T) / (T + 265.5))


def chaleur_latente(Ts, Ta, va, HR, surface="eau", Pa=1013.25):
    """
    Calcule le flux de chaleur latente pour une surface d'eau libre ou de glace,
    converti en Méga-joules (MJ/m²/jour) pour assurer la cohérence avec CEQUEAU.
    
    Paramètres :
        Ts (float)      : Température de surface (°C)
        Ta (float)      : Température de l'air (°C)
        va (float)      : Vitesse du vent (m/s)
        HR (float)      : Humidité relative (%)
        surface (str)   : "eau" ou "glace"
        Pa (float)      : Pression atmosphérique (hPa)
    Retourne :
        float : Flux de chaleur latente converti en MJ/m²/jour
    """
    if surface == "eau":
        # Surface d'eau libre
        Kn = 8 + 0.35 * (Ts - Ta) # Ta et Ts en °C, Kn sans unité
        es = 0.611 * np.exp((17.27 * Ta) / (Ta + 237.3)) # en kPa
        ea = es * (HR / 100.0) # en kPa
        
        # Flux initial en W/m² selon la formule aérodynamique
        phi_l_W = (4.1855 / 8.64) * (1.56 * Kn + 6.08 * va) * (es - ea) # en W/m²
        
        # Conversion de W/m² vers Méga-joules par jour (MJ/m²/jour)
        # 1 W = 1 J/s -> 1 W/m² * 86400 s/jour = 86400 J/m²/jour = 0.0864 MJ/m²/jour
        phi_l = phi_l_W * 0.0864
        return phi_l

    elif surface == "glace":
        # Surface de glace (Sublimation)
        rho_a = 1.293   # Densité de l'air (kg/m³)
        Ls = 2.83e6     # Chaleur latente de sublimation (J/kg)
        Kv = 0.001      # Coefficient d'échange turbulent (sans unité)
        Ua = va         # Vitesse du vent dans l'air (m/s)
        Us = 0.0        # Vitesse à la surface (m/s)
        
        # Pression de vapeur saturante et réelle de l'air (en hPa)
        es_a = es_eau_goff_gratch_murray(Ta)
        ea = (HR / 100.0) * es_a
        
        # Humidité spécifique de l'air qa (kg/kg)
        qa = (0.622 * ea) / (Pa - 0.378 * ea)
        
        # Correction de q_s pour la glace en utilisant l'équation exacte du document de référence :
        # q_s = [0.622 * (6.11 * 10^(9.75 * Ts / (Ts + 265.5)))] / [Pa - 0.378 * (...)]
        es_s = 6.11 * np.power(10.0, (9.75 * Ts) / (Ts + 265.5)) # Pression de saturation de la glace (hPa)
        qs = (0.622 * es_s) / (Pa - 0.378 * es_s) # Humidité spécifique à la surface de la glace (kg/kg)
        
        # Flux de chaleur latente de sublimation initial en W/m²
        Ql_W = rho_a * Ls * Kv * (Ua - Us) * (qa - qs) # en W/m²
        
        # Conversion du flux de W/m² vers Méga-joules par jour (MJ/m²/jour)
        Ql = Ql_W * 0.0864
        return Ql

    else:
        raise ValueError("Le paramètre surface doit être 'eau' ou 'glace'.")