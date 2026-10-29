import numpy as np

def chaleur_sensible(Ts, Ta, va, surface="eau", Cc=1.0, A=1.0, rho_a=1.293, Cp=1005.0, Ks=0.001):
    """
    Calcule le flux de chaleur sensible (en W/m²) pour une surface d'eau libre ou de glace.
    
    Paramètres :
        Ts (float) : Température de surface (°C ou K ; Te/Tw pour l'eau, Tis/Ts pour la glace)
        Ta (float) : Température de l'air (°C ou K)
        va (float) : Vitesse du vent (m/s)
        surface (str) : "eau" ou "glace"
        Cc (float) : Coefficient empirique proche de 1 (défaut : 1.0)
        A (float) : Surface d'échange en m² (défaut : 1.0)
        rho_a (float) : Densité de l'air en kg/m³ (défaut : 1.293)
        Cp (float) : Chaleur spécifique de l'air à pression constante en J/(kg·K) (défaut : 1005.0)
        Ks (float) : Coefficient d'échange turbulent (défaut : 0.001)
        
    Retourne :
        float : Flux de chaleur sensible harmonisé en W/m²
    """
    if surface == "eau":
        #Ici normalement ça doit rester dans le Méga jouls
        # 1. Surface libre (eau) : Convection
        # Formule : Qc = Cc * A * 0.2 * W * (Ta - Te)  [en MJ/jour]
        
        # Conversion du vent va (m/s) -> W (km/h)
        W = va * 3.6
        
        # Écart de température (Ta - Te/Tw)
        delta_T = Ta - Ts
        
        # Quantité d'énergie échangée Qc (MJ/jour)
        Qc_MJ = Cc * A * 0.2 * W * delta_T
        
        # Harmonisation vers W/m² :
        # 1 MJ = 10^6 J, 1 jour = 86 400 s
        # Flux (W/m²) = (Qc_MJ * 1e6) / (86400 * A)
        phi_s = (Qc_MJ * 1e6) / (86400.0 * A)
        return phi_s

    elif surface == "glace":
        # ici je dois la convertir en Méga jouls
        # 2. Surface de glace
        # Formule : Qs = ρa * Cp * Ks * (Ua - Us) * (Ta - Ts)  [en W/m²]
        Ua = va       # Vitesse du vent dans l'air (m/s)
        Us = 0.0      # Vitesse à la surface (m/s)
        delta_T = Ta - Ts
        
        Qs = rho_a * Cp * Ks * (Ua - Us) * delta_T
        return Qs

    else:
        raise ValueError("Le paramètre surface doit être 'eau' ou 'glace'.")