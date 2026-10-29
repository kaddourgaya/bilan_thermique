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
    
    Paramètres :
        Ts (float) : Température de surface (°C)
        Ta (float) : Température de l'air (°C)
        HR (float) : Humidité relative (%)
        C (float)  : Couverture nuageuse (sans unité, 0 à 1)
        es_func    : Fonction de calcul de pression de vapeur saturante
        ek (float) : Coefficient empirique d'émissivité nuageuse (sans unité)
    Retourne :
        float : Rayonnement net ondes longues en W/m² (avec possibilité de conversion en MJ)
    """
    sigma = 5.67e-8  # Constante de Stefan-Boltzmann (W/(m^2*K^4))
    
    # Conversion des températures en Kelvin / à vérifier dans cequeau 
    Tv_K = Ts + 273.16
    Ta_K = Ta + 273.16
       
    # Pression de vapeur saturante (en Pa) via la fonction adéquate (eau ou glace)
    es = 0.611 * np.exp((17.27 * Ta) / (Ta + 237.3)) # Ta en degré Celsius
    # es = es_func(Ta)
    
    # Pression de vapeur réelle (Équation 20) : ea = es * HR / 100 [kPa ou hPa selon l'échelle]
    ea = es * HR / 100.0
    
    # Émissivité atmosphérique (Équation 19)
    epsilon_a = 1.08 * (1.0 - np.exp(-ea * Ta_K / 2016.0))
    
    # Radiation de grande longueur d'onde (Équation 18)
    phi_lr = 0.97 * sigma * (Tv_K**4 - epsilon_a * (1.0 + ek * (C**2)) * Ta_K**4)
    # phi_lr = 0.97 * sigma * (Tv_K**4 - epsilon_a * (1.0 + ek * ((C / 100) **2)) * Ta_K**4)
    
    # Intégration des conditions selon le Fi (Lien avec le fichier glace et le bilan global) :
    # Les flux sont comparés en W/m² (mesurés vs calculés), mais pour calculer les bilans thermiques 
    # de type CEQUEAU, ils doivent être convertis en Méga-joules (MJ).
    # Équation de conversion : Énergie (J) = Puissance (W) × Temps (s)
    # De Watt-heure vers Méga-jouls : MJ = Wh * 0.0036  (pour un pas de temps horaire)
    # De Watt-jour vers Méga-jouls  : MJ = Wj * 0.0864  (pour un pas de temps journalier)
 
    return phi_lr