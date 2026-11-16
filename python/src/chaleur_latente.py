import numpy as np

def es_magnus_tetens(T):
    """
    Pression de vapeur saturante au-dessus de l'eau libre (hPa).
    Paramètre :
        T (float) : Température (°C)
    Retourne :
        float : Pression (hPa)
    """
    return 6.11 * np.exp((17.27 * T) / (T + 237.3))

def chaleur_latente_article(Ts, Ta, va, vs, HR, surface="eau", Pa=1013.25):
    """
    Calcule le flux de chaleur latente selon l'approche de l'article (Aérodynamique / Sublimation),
    converti en Méga-joules (MJ/m²/jour).
    """
    if surface == "eau":
        Kn = 8 + 0.35 * (Ts - Ta)
        es = es_magnus_tetens(Ta) #hpa
        ea = es * (HR / 100.0) #hpa
        phi_l_W = (4.1855 / 8.64) * (1.56 * Kn + 6.08 * va) * (es - ea)
        return phi_l_W * 0.0864

    elif surface == "glace":
        rho_a = 1.293
        Ls = 2.83e6
        Kw = 0.001
        Ua = va
        Us = vs
        es_a = es_magnus_tetens(Ta)
        ea = (HR / 100.0) * es_a
        qa = (0.622 * ea) / (Pa - 0.378 * ea)
        a = 6.11 * np.power(10.0, (9.75 * Ts) / (Ts + 265.5))
        qs = (0.622 * a) / (Pa - 0.378 * a)
        Ql_W = rho_a * Ls * Kw * (Ua - Us) * (qa - qs)
        return Ql_W * 0.0864

    else:
        raise ValueError("Le paramètre surface doit être 'eau' ou 'glace'.")


def chaleur_latente_cequeau(Ta, Le, Fi, A, Ce=1.0, H_latente=2480.0):
    """
    Calcule la chaleur latente d'évaporation selon l'approche CEQUEAU stricte :
    - Si Ta <= 0 °C -> Le = 0 donc Qe = 0
    - Eau libre (Fi = 0) : Qe = -Ce * Le * A * H
    - Glace partielle (0 < Fi < 1) : Qe = -Ce * Le * A * (1 - Fi) * H
    - Glace complète (Fi = 1) : Qe = 0
    
    Paramètres :
        Ta (float)        : Température de l'air (°C)
        Le (float)        : Lame quotidienne évaporée, issue de CEQUEAU (m)
        Fi (float)        : Fraction de couverture glacée (0 à 1)
        A (float)         : Surface de référence de la rivière (m²)
        Ce (float)        : Coefficient empirique à calibrer (0 à 2)
        H_latente (float) : Chaleur latente volumique, fixée à 2480 MJ/m³
    Retourne :
        float : Qe (MJ/m^2/jour)
    """
    # 1. Si Ta <= 0 °C, pas d'évaporation d'eau libre (Le = 0 d'où Qe = 0)
    if Ta <= 0.0:
        return 0.0

    # 2. Application stricte des formules selon les 3 conditions de la fraction glacée Fi :
    if Fi <= 0.0:
        # Eau libre (Fi = 0)
        #Qe = -Ce * Le * A * H_latente
        Qe = -Ce * Le * H_latente
    elif 0.0 < Fi < 1.0:
        # Glace partielle (0 < Fi < 1)
        #Qe = -Ce * Le * A * (1.0 - Fi) * H_latente
        Qe = -Ce * Le * (1.0 - Fi) * H_latente
    else:
        # Glace complète (Fi = 1)
        Qe = 0.0

    return Qe