import numpy as np

def chaleur_sensible(Ts, Ta, va, surface="eau", Cc=1.0, A=1.0, rho_a=1.293, Cp=1005.0, Ks=0.001):
    """
    Calcule le flux de chaleur sensible pour une surface d'eau libre ou de glace.
    
    Paramètres :
        Ts (float)      : Température de surface (°C)
        Ta (float)      : Température de l'air (°C)
        va (float)      : Vitesse du vent (m/s)
        surface (str)   : "eau" ou "glace"
        Cc (float)      : Coefficient empirique proche de 1 (défaut : 1.0)
        A (float)       : Surface d'échange en m² (défaut : 1.0)
        rho_a (float)   : Densité de l'air en kg/m³ (défaut : 1.293)
        Cp (float)      : Chaleur spécifique de l'air à pression constante en J/(kg·K) (défaut : 1005.0)
        Ks (float)      : Coefficient d'échange turbulent (sans unité, défaut : 0.001)
        
    Retourne :
        float : Flux de chaleur sensible en Méga-joules (MJ/jour ou MJ/m²/jour)
    """
    if surface == "eau":
        # 1. Surface libre (eau) : Convection
        # Formule : Qc = Cc * A * 0.2 * W * (Ta - Te) [en MJ/jour]
        
        # Conversion du vent va (m/s) -> W (km/h)
        W = va * 3.6
        
        # Écart de température (Ta - Te/Tw) (°C)
        delta_T = Ta - Ts
        
        # Quantité d'énergie échangée Qc directement en MJ/jour
        Qc_MJ = Cc * A * 0.2 * W * delta_T
        return Qc_MJ

    elif surface == "glace":
        # 2. Surface de glace
        # Calcul initial en W/m² : Qs_W = ρa * Cp * Ks * (Ua - Us) * (Ta - Ts) [en W/m²]
        Ua = va       # Vitesse du vent dans l'air (m/s)
        Us = 0.0      # Vitesse à la surface (m/s)
        delta_T = Ta - Ts # (°C)
        
        Qs_W = rho_a * Cp * Ks * (Ua - Us) * delta_T # en W/m²
        
        # Conversion inverse pour la glace : passage de W/m² vers MJ/m²/jour pour uniformiser avec l'eau
        Qs_MJ = Qs_W * 0.0864
        return Qs_MJ

    else:
        raise ValueError("Le paramètre surface doit être 'eau' ou 'glace'.")