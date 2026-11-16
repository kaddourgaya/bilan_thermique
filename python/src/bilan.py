def flux_net(phi_aw: float, phi_ai: float, Fi: float) -> float:
    """
    Bilan thermique net φn MJ/m²/jour
    Trois conditions :
    - Fi = 0   → chenal ouvert       → φn = φaw
    - 0 < Fi < 1 → partiellement glacé → φn = φaw(1-Fi) + φai*Fi
    - Fi = 1   → entièrement glacé   → φn = φai
    """
    if Fi <= 0:
        return phi_aw
    elif Fi >= 1:
        return phi_ai
    else:
        return phi_aw * (1 - Fi) + phi_ai * Fi


#Relation entre énergie et température
#Te = E / (V × C)
#Te : température de l’eau (°C) ; E : énergie thermique par rapport à 0 °C (MJ) (Gaya c le bilan thermique journaliere qu’on va déterminer je t explique apres); V : volume d’eau (m³) ; C : capacité thermique volumique de l’eau (MJ·m⁻³·°C⁻¹).
#On utilise C = 4,186 MJ·m⁻³·°C⁻¹.