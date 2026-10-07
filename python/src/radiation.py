# src/radiation.py

import numpy as np

def rayonnement_ondes_courtes(sr_in: float, sr_out: float) -> float:
    """
    Rayonnement net à ondes courtes φsr (W/m²)
    φsr = SW_In − SW_Out
    Mesure Apogee SN500SS
    """
    return sr_in - sr_out


def rayonnement_ondes_longues(lr_in: float, lr_out: float) -> float:
    """
    Rayonnement net à ondes longues φlr (W/m²)
    φlr = LW_In − LW_Out
    Mesure Apogee SN500SS
    """
    return lr_in - lr_out


def rayonnement_ondes_longues_ding(
    Ts: float, 
    Ta: float, 
    HR: float, 
    C: float, 
    es_func, 
    ek: float = 1.0
) -> float:
    """
    Rayonnement net à ondes longues φlr (W/m²) 
    selon Ding et al. (2026), équations (18), (19) et (20).
    φlr = 0.97 * sigma * [ Tv^4 − εₐ (1 + ek * C^2) Ta^4 ]
    """
    sigma = 5.67e-8  # Constante de Stefan-Boltzmann (W/(m^2*K^4))
    
    # Conversion des températures en Kelvin / à vérifier dans cequeau 
    Tv_K = Ts + 273.16
    Ta_K = Ta + 273.16
    
    # Pression de vapeur saturante (en Pa) via la fonction adéquate (eau ou glace)
    es = es_func(Ta)
    
    # Pression de vapeur réelle (Équation 20) : ea = es * HR / 100
    ea = es * HR / 100.0
    
    # Conversion de ea en hPa pour l'équation 19
    ea_hpa = ea / 100.0
    
    # Émissivité atmosphérique (Équation 19)
    epsilon_a = 1.08 * (1.0 - np.exp(-ea_hpa * Ta_K / 2016.0))
    
    # Radiation de grande longueur d'onde (Équation 18)
    phi_lr = 0.97 * sigma * (Tv_K**4 - epsilon_a * (1.0 + ek * (C**2)) * Ta_K**4)
    
    return phi_lr