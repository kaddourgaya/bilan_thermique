# src/radiation.py

import numpy as np

def rayonnement_ondes_courtes(sr_in: float, sr_out: float) -> float:
    """
    Rayonnement net à ondes courtes φsr (W/m²)
    φsr = SW_In − SW_Out
    Mesure Apogee SN500SS
    
    Paramètres :
        sr_in (float)  : Rayonnement onde courte incident (W/m²)
        sr_out (float) : Rayonnement onde courte réfléchi (W/m²)
    Retourne :
        float : Rayonnement net ondes courtes (W/m²)
    """
    return sr_in - sr_out


def rayonnement_ondes_longues(lr_in: float, lr_out: float) -> float:
    """
    Rayonnement net à ondes longues φlr (W/m²)
    φlr = LW_In − LW_Out
    Mesure Apogee SN500SS
    
    Paramètres :
        lr_in (float)  : Rayonnement onde longue incident (W/m²)
        lr_out (float) : Rayonnement onde longue émis/réfléchi (W/m²)
    Retourne :
        float : Rayonnement net ondes longues (W/m²)
    """
    return lr_in - lr_out

def es_goff_gratch_eau(T: float) -> float:
    """
    Équation (21) : Pression de vapeur saturante par rapport à l'eau libre (Pa)
    selon Goff et Gratch (1946) / Ding et al. (2026)[cite: 10].
    
    Paramètre :
        T (float) : Température de l'eau (°C)
    Retourne :
        float : Pression de vapeur saturante es (Pa)
    """
    # Conversion °C -> K
    T_K = T + 273.15
    
    terme1 = -18.1972839 * (373.16 / T_K)
    terme2 = 5.02808 * np.log(373.16 / T_K)
    terme3 = -20242.1852 * np.exp(-26.1205253 * (T_K / 373.16))
    terme4 = 58.0691913 * np.exp(-8.039282 * (373.16 / T_K))
    
    return 7.95357242e10 * np.exp(terme1 + terme2 + terme3 + terme4)


def es_goff_gratch_glace(T: float) -> float:
    """
    Équation (22) : Pression de vapeur saturante par rapport à la glace (Pa)
    selon Goff et Gratch (1946) / Ding et al. (2026)
    
    Paramètre :
        T (float) : Température de la glace (°C)
    Retourne :
        float : Pression de vapeur saturante es (Pa)
    """
    # Conversion °C -> K
    T_K = T + 273.15
    
    terme1 = -20.947031 * (373.16 / T_K)
    terme2 = -3.56654 * np.log(373.16 / T_K)
    terme3 = -2.01889049 / (273.16 / T_K)
    
    return 5.75185606e10 * np.exp(terme1 + terme2 + terme3)

def _calcul_flux_lr_unitaire(Ts: float, Ta: float, HR: float, C: float, es_Pa: float, ek: float) -> float:
    """
    Fonction interne calculant les étapes 3 à 6 pour une surface donnée :
    - Conversion des températures Ts et Ta de °C en Kelvin (+ 273.15)[cite: 10]
    - Équation (20) : ea = es * HR / 100 [Pa][cite: 10]
    - Équation (19) : εa = 1.08 * [1 - exp(-ea * Ta / 2016)] [sans unité][cite: 10]
    - Équation (18) : φlr = 0.97 * σ * [Ts⁴ - εa * (1 + ek * C²) * Ta⁴] [W/m²][cite: 10]
    """
    sigma = 5.67e-8  # Constante de Stefan-Boltzmann (W·m⁻²·K⁻⁴)
    
    # Conversion °C -> K en interne
    Ts_K = Ts + 273.15
    Ta_K = Ta + 273.15
    
    # Étape 3 : Pression réelle de vapeur ea (Pa) - Équation (20)
    ea = es_Pa * (HR / 100.0)
    
    # Étape 4 : Émissivité atmosphérique εa (sans unité) - Équation (19)
    epsilon_a = 1.08 * (1.0 - np.exp(-ea * np.exp (Ta_K / 2016.0)))
    
    # Étape 5/6 : Rayonnement net à ondes longues φlr (W/m²) - Équation (18)
    # Normalisation de la nébulosité C en fraction (0 à 1) si fournie en % (> 1)
    C_frac = C / 100.0 #if C > 1.0 else C

    phi_lr = 0.97 * sigma * ((Ts_K**4) - epsilon_a * (1.0 + ek * (C_frac**2)) * (Ta_K**4))
    
    return phi_lr

def rayonnement_ondes_longues_ding(
    Tw: float,
    Tis: float,
    Ta: float,
    HR: float,
    C: float,
    Fi: float,
    ek: float = 1.0
) -> tuple[float, float, float]:
    """
    Calcule le rayonnement net à ondes longues φlr (W/m²) selon Ding et al. (2026)
    en appliquant les 3 conditions de couverture glacée (Fi) :
    - Condition 1 (Fi = 0)     : Eau libre -> es via éq. (21) avec Tw
    - Condition 2 (Fi = 1)     : Glace complète -> es via éq. (22) avec Tis
    - Condition 3 (0 < Fi < 1) : Couverture partielle -> pondération (1 - Fi)*φlr,w + Fi*φlr,i
    
    Paramètres :
        Tw (float)  : Température de surface de l'eau (°C)
        Tis (float) : Température de surface de la glace (°C)
        Ta (float)  : Température de l'air (°C)
        HR (float)  : Humidité relative (%)
        C (float)   : Nébulosité (% de 0 à 100, ou fraction de 0 à 1)
        Fi (float)  : Fraction de couverture glacée (0 à 1)
        ek (float)  : Coefficient empirique sans unité (défaut : 1.0)
        
    Retourne :
        tuple[float, float, float] : (phi_lr_w, phi_lr_i, phi_lr_total) en W/m²
    """
    # Normalisation de la nébulosité C en fraction (0 à 1) si fournie en % (> 1)
    C_frac = C / 100.0 #if C > 1.0 else C

    # Condition 1 : Eau libre (Fi <= 0)
    if Fi <= 0.0:
        es_w = es_goff_gratch_eau(Tw)
        phi_lr_w = _calcul_flux_lr_unitaire(Tw, Ta, HR, C_frac, es_w, ek)
        phi_lr_i = 0.0

    # Condition 2 : Couverture complète de glace (Fi >= 1)
    elif Fi >= 1.0:
        es_i = es_goff_gratch_glace(Tis)
        phi_lr_w = 0.0
        phi_lr_i = _calcul_flux_lr_unitaire(Tis, Ta, HR, C_frac, es_i, ek)

    # Condition 3 : Couverture partielle (0 < Fi < 1)
    else:
        es_w = es_goff_gratch_eau(Tw)
        es_i = es_goff_gratch_glace(Tis)
        
        phi_lr_w = _calcul_flux_lr_unitaire(Tw, Ta, HR, C_frac, es_w, ek)
        phi_lr_i = _calcul_flux_lr_unitaire(Tis, Ta, HR, C_frac, es_i, ek)
        
    return phi_lr_w, phi_lr_i